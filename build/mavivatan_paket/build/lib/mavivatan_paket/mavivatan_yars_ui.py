import sys
import os
import math
import folium
import cv2
import numpy as np
import serial

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, NavSatFix, Image
from std_msgs.msg import String
from geometry_msgs.msg import Vector3, Twist  # PID değerleri için gerekli
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QTabWidget, QLabel, QTextEdit, QPushButton, QSlider, QGroupBox, QLineEdit, QListWidget)
from PySide6.QtCore import Qt, QThread, Signal, QPointF
from PySide6.QtGui import QFont, QPalette, QColor, QPainter, QPen, QImage, QPixmap
from cv_bridge import CvBridge
from PySide6.QtWidgets import QProgressBar
# --- 1. RADAR WIDGET ---
class CostMapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)
        self.lidar_data = []  # Normal engeller: [(aci, mesafe)]
        self.yolo_data = []  # Şamandıralar: [(aci, mesafe, renk)]

    def update_map(self, lidar, yolo):
        self.lidar_data = lidar
        self.yolo_data = yolo
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Arka Plan
        painter.fillRect(self.rect(), QColor(15, 15, 15))
        center = self.rect().center()
        scale = 15  # 1 metre = 15 piksel

        # 1. Mesafe Halkaları (Radar Görünümü)
        painter.setPen(QPen(QColor(40, 40, 40), 1, Qt.DashLine))
        for r in range(1, 6):  # 1m, 2m, 3m...
            painter.drawEllipse(center, r * 30, r * 30)

        # 2. Genel Lidar Noktaları (Sıradan Engeller - İnce Yeşil)
        painter.setPen(QPen(QColor(0, 255, 0, 150), 3))
        for angle, dist in self.lidar_data:
            rad = math.radians(angle - 90)  # 0 dereceyi "ön", yani yukarı almak için -90
            x = center.x() + dist * scale * math.cos(rad)
            y = center.y() + dist * scale * math.sin(rad)
            painter.drawPoint(QPointF(x, y))

        # 3. YOLO ile Eşleşen Şamandıralar (Renkli ve Büyük)
        for angle, dist, renk in self.yolo_data:
            rad = math.radians(angle - 90)
            x = center.x() + dist * scale * math.cos(rad)
            y = center.y() + dist * scale * math.sin(rad)

            # Renge göre fırça seçimi
            if "kirmizi" in renk.lower():
                color = QColor(255, 0, 0)
            elif "sari" in renk.lower():
                color = QColor(255, 255, 0)
            elif "yesil" in renk.lower():
                color = QColor(0, 255, 0)
            else:
                color = QColor(255, 255, 255)

            painter.setBrush(color)
            painter.setPen(QPen(Qt.white, 1))
            painter.drawEllipse(QPointF(x, y), 8, 8)  # Şamandırayı 8px kalınlığında çiz

        # 4. İDA'nın Kendisi (Merkezdeki Mavi Tekne İkonu)
        painter.setBrush(QColor(0, 200, 255))
        painter.drawPolygon([
            QPointF(center.x(), center.y() - 10),
            QPointF(center.x() - 6, center.y() + 8),
            QPointF(center.x() + 6, center.y() + 8)
        ])


class RosWorker(QThread):
    costmap_signal = Signal(list, list) # Lidar listesi, YOLO listesi
    log_signal = Signal(str)
    gps_signal = Signal(float, float)
    image_signal = Signal(QImage)
    motor_signal = Signal(float, float)  # linear_x, angular_z
    def __init__(self):
        super().__init__()
        rclpy.init()
        self.node = Node('yki_arayuz_node')
        self.br = CvBridge()
        self.pid_pub = self.node.create_publisher(Vector3, '/pid_ayarlari', 10)
        self.iha_hedef_pub = self.node.create_publisher(String, '/iha_onayli_hedef', 10)
        self.son_yolo_verileri = [] # YOLO'dan gelenleri hafızada tutacağız
        self.kamera_fov = 110.0     # ZED kamerasının yatay görüş açısı (Derece)
        self.kamera_genislik = 640.0 # Görüntünün piksel genişliği
        # YOLO'nun kutu çizdiği görüntüyü dinliyoruz
        self.node.create_subscription(Image, '/yolo_debug_goruntu', self.image_callback, 10)
        # Otonomi yazılımından veya YOLO'dan çıkan hız/yön komutlarını dinliyoruz
        self.node.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        # Abonelikler
        self.node.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)
        self.node.create_subscription(String, '/yolo_tespit_ozeti', self.yolo_callback, 10) # YOLO JSON kanalı
        # ... diğer abonelikler (gps, log vs.) ...
        self.son_mesaj_zamani = time.time()
        self.baglanti_kopuk_mu = False

        # Saniyede bir bağlantıyı kontrol eden zamanlayıcı
        self.timer = self.node.create_timer(1.0, self.baglanti_kontrol)
    def image_callback(self, data):
        try:
            cv_img = self.br.imgmsg_to_cv2(data, "bgr8")
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_img.shape
            bytes_per_line = ch * w
            # Qt'nin çökmemesi için .copy() yapmak şarttır!
            q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
            self.image_signal.emit(q_img)
        except Exception as e:
            pass

    def baglanti_kontrol(self):
        gecen_sure = time.time() - self.son_mesaj_zamani
        if gecen_sure > 3.0 and not self.baglanti_kopuk_mu:
            self.baglanti_kopuk_mu = True
            self.log_signal.emit("⚠️ KRİTİK: İDA İLE TELEMETRİ BAĞLANTISI KOPTU! (3 saniyedir veri yok)")
        elif gecen_sure <= 3.0 and self.baglanti_kopuk_mu:
            self.baglanti_kopuk_mu = False
            self.log_signal.emit("✅ TELEMETRİ BAĞLANTISI YENİDEN SAĞLANDI.")
    def cmd_vel_callback(self, msg):
        self.motor_signal.emit(msg.linear.x, msg.angular.z)

    def yolo_callback(self, msg):
        # Yolo düğümü şöyle bir JSON atmalı: [{"renk": "kirmizi", "x": 320}, {"renk": "yesil", "x": 500}]
        self.son_mesaj_zamani = time.time()
        try:
            import json
            self.son_yolo_verileri = json.loads(msg.data)
        except:
            pass
    def pid_yayinla(self, p, i, d):
        msg = Vector3()
        msg.x = float(p)
        msg.y = float(i)
        msg.z = float(d)
        self.pid_pub.publish(msg)

    def iha_hedef_yayinla(self, hedef_verisi_str):
        msg = String()
        msg.data = hedef_verisi_str
        self.iha_hedef_pub.publish(msg)

    def lidar_callback(self, msg):
        genel_engeller = []
        samandiralar = []

        # 1. Lidar verilerini işle
        for i, dist in enumerate(msg.ranges):
            if 0.1 < dist < 10.0:
                # Lidar'ın kendi açısından -180 ile +180 formatına veya 0-360 formatına göre düzeltme yapıyoruz.
                # (Rplidar genelde 0 dereceyi arka veya ön verir, donanıma göre offset eklenebilir)
                aci_derece = float(i)
                genel_engeller.append((aci_derece, dist))

        # 2. YOLO Füzyonu (Açı Eşleştirme)
        for obje in self.son_yolo_verileri:
            piksel_x = obje["x"]
            renk = obje["renk"]

            # Pikseli dereceye çevir (Kamera merkezini 0 derece kabul ediyoruz)
            merkezden_sapma_piksel = piksel_x - (self.kamera_genislik / 2.0)
            sapma_derecesi = (merkezden_sapma_piksel / self.kamera_genislik) * self.kamera_fov

            # Kameranın 0 derecesi (ön), Lidar'ın 0 derecesi (ön) ise açı doğrudan eşleşir.
            # Eksi açılar (sol) için 360'a tamamlıyoruz.
            hedef_aci_lidar = (sapma_derecesi + 360) % 360

            # Lidar verisindeki o açıya denk gelen (veya en yakın olan) mesafeyi bul
            try:
                indeks = int(hedef_aci_lidar) % len(msg.ranges)
                gercek_mesafe = msg.ranges[indeks]

                # Eğer o açıda geçerli bir Lidar ölçümü varsa, haritaya şamandıra olarak ekle
                if 0.1 < gercek_mesafe < 10.0:
                    samandiralar.append((hedef_aci_lidar, gercek_mesafe, renk))
            except IndexError:
                pass

        # Arayüze fırlat
        self.costmap_signal.emit(genel_engeller, samandiralar)
    def log_callback(self, msg):
        self.log_signal.emit(msg.data)

    def gps_callback(self, msg):
        self.gps_signal.emit(msg.latitude, msg.longitude)

    def run(self):
        rclpy.spin(self.node)


# --- 3. ANA ARAYÜZ ---
class MaviVatanControlCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAVİ VATAN - Yer Kontrol İstasyonu v2.1")
        self.resize(1200, 800)
        self.set_dark_theme()

        # --- 1. RF BAĞLANTISI (Pals ve Komutlar İçin Şart) ---
        try:
            # Jetson'da veya PC'de antenin takılı olduğu portu otomatik açar
            import serial
            self.ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1)
            print("✅ RF Anten Bağlantısı Başarılı.")
        except Exception as e:
            self.ser = None
            print(f"⚠️ Anten Bulunamadı (Simülasyon Modu): {e}")

        # --- 2. ARAYÜZ YERLEŞİMİ (Layout) ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Üst Bilgi Paneli
        self.top_panel = QHBoxLayout()
        self.add_status_indicator("BATARYA", 85, "%")
        self.add_status_indicator("SİNYAL", -65, "dBm")
        self.add_status_indicator("HIZ", 0.0, "m/s")
        self.main_layout.addLayout(self.top_panel)

        # Sekme Yapısı
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.tab_mission = QWidget()
        self.tab_pid = QWidget()
        self.tab_logs = QWidget()
        self.tab_iha = QWidget()

        self.tabs.addTab(self.tab_mission, "OPERASYON EKRANI")
        self.tabs.addTab(self.tab_pid, "PID VE FİLTRE AYARLARI")
        self.tabs.addTab(self.tab_logs, "SİSTEM LOGLARI")
        self.tabs.addTab(self.tab_iha, "🚁 İHA KOORDİNASYON")

        # Sekme İçeriklerini Doldur
        self.init_mission_tab()
        self.init_pid_tab()
        self.init_logs_tab()
        self.init_iha_tab()

        # --- 3. ROS 2 HABERLEŞME ZİNCİRİ ---
        self.ros_thread = RosWorker()
        # Sinyal Bağlantıları (Arka plan -> Arayüz)
        self.ros_thread.costmap_signal.connect(self.update_costmap)
        self.ros_thread.log_signal.connect(self.update_log)
        self.ros_thread.gps_signal.connect(self.guncelle_gps_hud)

        self.ros_thread.image_signal.connect(self.guncelle_kamera_ekrani)
        self.ros_thread.motor_signal.connect(self.guncelle_motor_paneli)
        self.ros_thread.start()
    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(25, 25, 25))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(18, 18, 18))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)

    def add_status_indicator(self, label, value, unit):
        group = QGroupBox(label)
        vbox = QVBoxLayout()
        lbl = QLabel(f"{value} {unit}")
        lbl.setFont(QFont("Consolas", 14, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("color: #00ff00;")
        vbox.addWidget(lbl)
        group.setLayout(vbox)
        self.top_panel.addWidget(group)

    def update_costmap(self, lidar_data, yolo_data):
        self.costmap_view.update_map(lidar_data, yolo_data)

    def init_mission_tab(self):
        layout = QHBoxLayout(self.tab_mission)

        # --- SOL PANEL: HUD VE COSTMAP ---
        left_side = QVBoxLayout()
        self.gps_hud = QLabel()
        self.gps_hud.setStyleSheet(
            "background-color: #0a0a0a; color: #00ffff; border: 1px solid #00ffff; font-family: Consolas; font-size: 16px;")
        self.gps_hud.setAlignment(Qt.AlignCenter)
        self.guncelle_gps_hud(40.6940, 29.5080)
        left_side.addWidget(self.gps_hud)

        btn_harita_ac = QPushButton("🗺️ DETAYLI HARİTAYI TARAYICIDA AÇ")
        btn_harita_ac.setStyleSheet("background-color: #005577; color: white; font-weight: bold;")
        btn_harita_ac.clicked.connect(self.haritayi_disarda_ac)
        left_side.addWidget(btn_harita_ac)

        self.costmap_view = CostMapWidget()
        left_side.addWidget(self.costmap_view)
        layout.addLayout(left_side, 2)
        cam_motor_side = QVBoxLayout()
        # 1. Canlı Kamera
        cam_motor_side.addWidget(QLabel("📷 YOLO CANLI VİZYON"))
        self.lbl_kamera = QLabel("Kamera Verisi Bekleniyor...")
        self.lbl_kamera.setMinimumSize(480, 270)
        self.lbl_kamera.setStyleSheet("background-color: #000; border: 2px solid cyan;")
        self.lbl_kamera.setAlignment(Qt.AlignCenter)
        cam_motor_side.addWidget(self.lbl_kamera)
        # 2. Motor PWM Durumu
        motor_group = QGroupBox("⚙️ MOTOR PWM ve OTONOMİ ÇIKTISI")
        motor_layout = QVBoxLayout()

        self.lbl_cmd_vel = QLabel("Otonomi: İleri: 0.0 m/s | Dönüş: 0.0 rad/s")
        self.lbl_cmd_vel.setStyleSheet("color: yellow; font-weight:bold;")
        motor_layout.addWidget(self.lbl_cmd_vel)

        pwm_h_layout = QHBoxLayout()
        # Sol Motor Bar
        v_sol = QVBoxLayout()
        self.bar_sol = QProgressBar()
        self.bar_sol.setRange(1000, 2000)
        self.bar_sol.setValue(1500)
        self.bar_sol.setTextVisible(True)
        self.bar_sol.setFormat("SOL: %v PWM")
        v_sol.addWidget(self.bar_sol)

        # Sağ Motor Bar
        v_sag = QVBoxLayout()
        self.bar_sag = QProgressBar()
        self.bar_sag.setRange(1000, 2000)
        self.bar_sag.setValue(1500)
        self.bar_sag.setTextVisible(True)
        self.bar_sag.setFormat("SAĞ: %v PWM")
        v_sag.addWidget(self.bar_sag)

        pwm_h_layout.addLayout(v_sol)
        pwm_h_layout.addLayout(v_sag)
        motor_layout.addLayout(pwm_h_layout)
        motor_group.setLayout(motor_layout)

        cam_motor_side.addWidget(motor_group)
        layout.addLayout(cam_motor_side, 3)
        # --- ORTA PANEL: GÖREV 1 GPS ROTALARI ---
        mid_side = QVBoxLayout()
        mid_side.addWidget(QLabel("📍 Görev 1 Rotaları (Kanal Girişine Kadar):"))

        inputs_layout = QHBoxLayout()
        self.lat_input = QLineEdit()
        self.lat_input.setPlaceholderText("Enlem (Örn: 40.6940)")
        self.lon_input = QLineEdit()
        self.lon_input.setPlaceholderText("Boylam (Örn: 29.5080)")
        inputs_layout.addWidget(self.lat_input)
        inputs_layout.addWidget(self.lon_input)
        mid_side.addLayout(inputs_layout)

        btn_add = QPushButton("Listeye Ekle")
        btn_add.clicked.connect(self.add_coordinate)
        mid_side.addWidget(btn_add)

        self.coord_list = QListWidget()
        self.coord_list.setStyleSheet("background-color: #111; color: #0f0;")
        mid_side.addWidget(self.coord_list)
        layout.addLayout(mid_side, 1)

        # --- SAĞ PANEL: GÖREV 3 HEDEFİ VE BUTONLAR ---
        right_side = QVBoxLayout()
        right_side.addWidget(QLabel("🎯 Görev 3: Kamikaze Başlangıç Noktası:"))
        self.kamikaze_target_input = QLineEdit()
        self.kamikaze_target_input.setPlaceholderText("Örn: 40.6950, 29.5090")
        self.kamikaze_target_input.setStyleSheet("color: #ffaa00; font-weight: bold;")
        right_side.addWidget(self.kamikaze_target_input)

        right_side.addStretch()

        btn_arm = QPushButton("ARM / DISARM")
        btn_arm.setStyleSheet("background-color: #a00; height: 50px; font-weight: bold;")
        right_side.addWidget(btn_arm)

        btn_start = QPushButton("🚀 GÖREVİ BAŞLAT")
        btn_start.setStyleSheet("background-color: #005500; height: 50px; font-weight: bold;")
        btn_start.clicked.connect(self.send_mission)  # BAĞLANTI EKLENDİ
        right_side.addWidget(btn_start)

        btn_rtl = QPushButton("🏠 EVE DÖN (RTL)")
        btn_rtl.setStyleSheet("background-color: #d84315; height: 50px; font-weight: bold;")
        btn_rtl.clicked.connect(self.send_rtl)  # BAĞLANTIYI BURAYA EKLEDİK
        right_side.addWidget(btn_rtl)

        layout.addLayout(right_side, 1)

    # --- EKSİK YARDIMCI FONKSİYONLAR (Sınıfın içine ekle) ---
    def add_coordinate(self):
        if self.lat_input.text() and self.lon_input.text():
            self.coord_list.addItem(f"{self.lat_input.text()},{self.lon_input.text()}")
            self.lat_input.clear()
            self.lon_input.clear()

    def send_data(self, data_dict):
        msg = json.dumps(data_dict)
        # Eğer RFD900 açık değilse sadece loga bas, çökmeyi engelle
        if hasattr(self, 'ser') and self.ser:
            try:
                self.ser.write((msg + "\n").encode())
            except Exception as e:
                self.update_log(f"⚠️ RF Gönderim Hatası: {e}")
        self.update_log(f"📤 YKİ KOMUTU: {msg}")

    def guncelle_gps_hud(self, lat, lon):
        metin = f"\n[ MAVİ VATAN SEYRÜSEFER SİSTEMİ ]\n---------------------------------\nLATITUDE  (ENLEM)  : {lat:.6f} N\nLONGITUDE (BOYLAM) : {lon:.6f} E\n\nDurum: GNSS KİLİDİ AKTİF 🛰️\n"
        self.gps_hud.setText(metin)

    def haritayi_disarda_ac(self):
        import webbrowser
        m = folium.Map(location=[40.6940, 29.5080], zoom_start=18, tiles='CartoDB dark_matter')
        map_path = os.path.abspath('ida_aktif_harita.html')
        m.save(map_path)
        webbrowser.open(f"file://{map_path}")

    def init_pid_tab(self):
        layout = QVBoxLayout(self.tab_pid)
        steering_group = QGroupBox("Dümen PID Ayarları (Hassas Kontrol)")
        grid = QVBoxLayout()

        # --- VARSAYILAN BAŞLANGIÇ DEĞERLERİ ---
        self.val_p, self.val_i, self.val_d = 0.40, 0.05, 0.15  # Burayı istediğin gibi değiştirebilirsin

        # Slider ve Etiketleri Oluşturma
        self.slider_p = QSlider(Qt.Horizontal);
        self.slider_p.setRange(0, 100)
        self.slider_i = QSlider(Qt.Horizontal);
        self.slider_i.setRange(0, 100)
        self.slider_d = QSlider(Qt.Horizontal);
        self.slider_d.setRange(0, 100)

        # Değerleri gösteren rakam etiketleri
        self.lbl_p = QLabel(str(self.val_p))
        self.lbl_i = QLabel(str(self.val_i))
        self.lbl_d = QLabel(str(self.val_d))

        # Başlangıç pozisyonlarını ayarla
        self.slider_p.setValue(int(self.val_p * 100))
        self.slider_i.setValue(int(self.val_i * 100))
        self.slider_d.setValue(int(self.val_d * 100))

        # Slider kaydırıldığında rakamların değişmesi için bağlantılar
        self.slider_p.valueChanged.connect(lambda v: self.lbl_p.setText(f"{v / 100.0:.2f}"))
        self.slider_i.valueChanged.connect(lambda v: self.lbl_i.setText(f"{v / 100.0:.2f}"))
        self.slider_d.valueChanged.connect(lambda v: self.lbl_d.setText(f"{v / 100.0:.2f}"))

        # Arayüze yerleştirme
        for ad, slider, label in [("Kp", self.slider_p, self.lbl_p),
                                  ("Ki", self.slider_i, self.lbl_i),
                                  ("Kd", self.slider_d, self.lbl_d)]:
            h = QHBoxLayout()
            h.addWidget(QLabel(f"<b>{ad}:</b>"), 1)
            h.addWidget(slider, 5)
            label.setStyleSheet("color: #00ffff; font-weight: bold; min-width: 40px;")
            h.addWidget(label, 1)
            grid.addLayout(h)

        btn = QPushButton("🚀 YENİ PID DEĞERLERİNİ İDA'YA GÖNDER")
        btn.setStyleSheet("background-color: #005500; color: white; font-weight: bold; height: 45px; margin-top: 10px;")
        btn.clicked.connect(self.pid_gonder_tetikle)
        grid.addWidget(btn)

        steering_group.setLayout(grid)
        layout.addWidget(steering_group)
        layout.addStretch()

    def pid_gonder_tetikle(self):
        # Slider'lardan güncel değerleri oku
        p = self.slider_p.value() / 100.0
        i = self.slider_i.value() / 100.0
        d = self.slider_d.value() / 100.0

        # ROS üzerinden İDA'ya fırlat
        self.ros_thread.pid_yayinla(p, i, d)

        # Log ekranına ve terminale yaz
        mesaj = f"PID Komutu Gönderildi >> Kp: {p:.2f} | Ki: {i:.2f} | Kd: {d:.2f}"
        self.update_log(mesaj)

    def init_logs_tab(self):
        layout = QVBoxLayout(self.tab_logs)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: black; color: #0f0; font-family: Consolas;")
        layout.addWidget(self.log_output)

        # --- LOG KAYIT BUTONU ---
        self.btn_save_logs = QPushButton("💾 TÜM LOGLARI KAYDET (.TXT)")
        self.btn_save_logs.setStyleSheet("background-color: #444; color: white; height: 35px; font-weight: bold;")
        self.btn_save_logs.clicked.connect(self.save_logs_to_file)
        layout.addWidget(self.btn_save_logs)

        self.log_output.append("[SYSTEM] Log Kayıt Sistemi Aktif.")

    def save_logs_to_file(self):
        import datetime
        try:
            # Masaüstüne veya proje klasörüne tarihli dosya oluşturur
            zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            dosya_adi = f"mavivatan_log_{zaman}.txt"

            with open(dosya_adi, "w", encoding="utf-8") as f:
                f.write(self.log_output.toPlainText())

            self.update_log(f"LOGLAR BAŞARIYLA KAYDEDİLDİ: {dosya_adi}")
        except Exception as e:
            print(f"Log kaydetme hatası: {e}")



    def update_log(self, text): self.log_output.append(f"[İDA]: {text}")

    def init_iha_tab(self):
        layout = QHBoxLayout(self.tab_iha)

        # --- SOL PANEL: İHA Canlı Telemetri ---
        sol_panel = QGroupBox("📡 İHA Telemetri (Manuel Uçuş)")
        sol_layout = QVBoxLayout()

        self.lbl_iha_irtifa = QLabel("İrtifa: 15.2 m")
        self.lbl_iha_irtifa.setStyleSheet("color: cyan; font-size: 20px; font-weight: bold;")

        # Bu değerleri şimdilik statik (sabit) giriyoruz. Sonra İHA'dan gelen veriye bağlayabiliriz.
        self.lbl_iha_enlem = QLabel("40.69400")
        self.lbl_iha_enlem.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        self.lbl_iha_boylam = QLabel("29.50800")
        self.lbl_iha_boylam.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        sol_layout.addWidget(self.lbl_iha_irtifa)
        sol_layout.addWidget(QLabel("Anlık Enlem:"))
        sol_layout.addWidget(self.lbl_iha_enlem)
        sol_layout.addWidget(QLabel("Anlık Boylam:"))
        sol_layout.addWidget(self.lbl_iha_boylam)
        sol_layout.addStretch()
        sol_panel.setLayout(sol_layout)
        layout.addWidget(sol_panel, 1)

        # --- SAĞ PANEL: İDA Kamikaze Yönlendirme ---
        sag_panel = QGroupBox("🎯 İDA Hedef Atama ve Renk Onayı")
        sag_layout = QVBoxLayout()

        # Renk Onay Göstergesi
        self.lbl_hedef_renk = QLabel("TESPİT EDİLEN RENK: KIRMIZI")
        self.lbl_hedef_renk.setStyleSheet(
            "background-color: #550000; color: #ff0000; font-weight: bold; padding: 10px; font-size: 16px; border: 2px solid red;")
        self.lbl_hedef_renk.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(self.lbl_hedef_renk)

        # O Kritik Kırmızı Buton
        btn_hedef_ata = QPushButton("🚀 İHA KONUMUNU İDA'YA SALDIRI HEDEFİ OLARAK GÖNDER")
        btn_hedef_ata.setStyleSheet(
            "background-color: #cc0000; color: white; height: 70px; font-weight: bold; font-size: 13px; border-radius: 5px;")
        btn_hedef_ata.clicked.connect(self.iha_hedef_rengini_idaya_gonder)
        sag_layout.addWidget(btn_hedef_ata)

        sag_layout.addStretch()
        sag_panel.setLayout(sag_layout)
        layout.addWidget(sag_panel, 2)

    def send_mission(self):
        # Görev 1 noktaları (Listbox'taki tüm noktalar)
        task1_points = [self.coord_list.item(i).text() for i in range(self.coord_list.count())]

        # Görev 3 noktası (Arayüzde ayrı bir kutuda tuttuğumuz tek koordinat)
        task3_point = self.kamikaze_target_input.text()

        data = {
            "command": "GOREV_BUTCESI_BASLAT",
            "task1_waypoints": task1_points,
            "task3_waypoint": task3_point
        }
        self.send_data(data)
    def iha_hedef_rengini_idaya_gonder(self):
        # Label'daki tam metni alıyoruz (Örn: "TESPİT EDİLEN RENK: SARI")
        renk_tam_metin = self.lbl_hedef_renk.text()

        # Sadece rengi çekmek için metni iki noktadan (:) bölüyoruz
        # Strip() ile sağdaki soldaki boşlukları siliyoruz
        renk = renk_tam_metin.split(":")[-1].strip()

        # ROS üzerinden İDA otonomisine rengi fırlat
        self.ros_thread.iha_hedef_yayinla(renk)

        # Log ekranına bilgi bas
        self.update_log(f"💥 İHA İSTİHBARATI İDA'YA AKTARILDI: Denizde Aranacak Renk -> {renk}")

    def send_rtl(self):
            # RTL (Return to Launch) komutunu paketle ve gönder
            data = {"command": "EVE_DON_RTL"}
            self.send_data(data)

    def guncelle_kamera_ekrani(self, q_img):
        # Görüntüyü QLabel boyutuna sığdırıp bas
        pixmap = QPixmap.fromImage(q_img)
        self.lbl_kamera.setPixmap(pixmap.scaled(self.lbl_kamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def guncelle_motor_paneli(self, linear, angular):
        # YZ'den gelen cmd_vel verisini göster
        self.lbl_cmd_vel.setText(f"Otonomi: İleri: {linear:.2f} | Dönüş: {angular:.2f}")

        # Matematiksel Dönüşüm (Skid Steering / Diferansiyel Sürüş için basit model)
        # 1500 PWM = Dur, 2000 = Tam İleri, 1000 = Tam Geri
        sol_pwm = int(1500 + (linear - angular) * 500)
        sag_pwm = int(1500 + (linear + angular) * 500)

        # Sınırları aşmasını engelle (1000 ile 2000 arasına hapseden güvenlik kilidi)
        sol_pwm = max(1000, min(2000, sol_pwm))
        sag_pwm = max(1000, min(2000, sag_pwm))

        self.bar_sol.setValue(sol_pwm)
        self.bar_sag.setValue(sag_pwm)

        # Renklendirme (Hareket varsa bar yeşil, duruyorsa gri, geri gidiyorsa kırmızı olsun)
        def stil_belirle(pwm):
            if pwm > 1550:
                return "QProgressBar::chunk {background-color: #00ff00;}"
            elif pwm < 1450:
                return "QProgressBar::chunk {background-color: #ff0000;}"
            else:
                return "QProgressBar::chunk {background-color: #555555;}"

        self.bar_sol.setStyleSheet(stil_belirle(sol_pwm))
        self.bar_sag.setStyleSheet(stil_belirle(sag_pwm))
def main(args=None):
    QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
    app = QApplication(sys.argv)
    window = MaviVatanControlCenter()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()