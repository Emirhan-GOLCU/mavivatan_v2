import sys
import json
import serial
import webbrowser
import os
import math
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QTextEdit, QComboBox,
                               QLabel, QLineEdit, QListWidget, QGroupBox, QGridLayout)
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QTimer, QPointF


# --- LİDAR RADAR WIDGET'I ---
class LidarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)
        self.lidar_data = []

    def update_data(self, data):
        self.lidar_data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(15, 15, 15))

        center = self.rect().center()
        scale = 15

        painter.setPen(QPen(QColor(40, 40, 40), 1))
        for r in range(1, 6):
            painter.drawEllipse(center, r * 30, r * 30)

        painter.setPen(QPen(Qt.green, 3))
        for angle, dist in self.lidar_data:
            rad = math.radians(angle - 90)
            x = center.x() + dist * scale * math.cos(rad)
            y = center.y() + dist * scale * math.sin(rad)
            painter.drawPoint(QPointF(x, y))


# --- ANA ARAYÜZ ---
class YKIMerkez(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAVİ VATAN YKİ - Taktik Ekranı")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #1a1a1a; color: #e0e0e0; font-family: 'Segoe UI', Arial;")

        # RFD900x Seri Port
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1)
        except:
            self.ser = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # --- ÜST PANEL: TELEMETRİ VE SENSÖRLER ---
        top_group = QGroupBox("İDA Canlı Sensör Verileri (Şartname)")
        top_group.setStyleSheet("QGroupBox { border: 1px solid #444; border-radius: 5px; font-weight: bold; }")
        top_layout = QHBoxLayout()

        self.lbl_battery = QLabel("🔋 Batarya: %84 (14.2V)")
        self.lbl_battery.setStyleSheet("color: #00ff00; font-size: 14px;")

        self.lbl_heading = QLabel("🧭 Pusula: 275° (Batı)")
        self.lbl_heading.setStyleSheet("color: #00bfff; font-size: 14px;")

        self.lbl_signal = QLabel("📡 RF Sinyali: %92")
        self.lbl_signal.setStyleSheet("color: #00ff00; font-size: 14px;")

        self.lbl_status = QLabel("BAĞLANTI: KOPUK" if not self.ser else "BAĞLANTI: AKTİF")
        self.lbl_status.setStyleSheet(
            "color: red; font-size: 14px; font-weight: bold;" if not self.ser else "color: lime; font-size: 14px; font-weight: bold;")

        top_layout.addWidget(self.lbl_battery)
        top_layout.addWidget(self.lbl_heading)
        top_layout.addWidget(self.lbl_signal)
        top_layout.addWidget(self.lbl_status)
        top_group.setLayout(top_layout)
        main_layout.addWidget(top_group)

        # --- ORTA BÖLÜM (Sol: Lidar, Orta: GPS, Sağ: Kontroller) ---
        middle_layout = QHBoxLayout()

        # SOL: LİDAR
        lidar_group = QGroupBox("360° Çevre Farkındalığı (Lidar)")
        lidar_layout = QVBoxLayout()
        self.lidar_view = LidarWidget()
        lidar_layout.addWidget(self.lidar_view)
        lidar_group.setLayout(lidar_layout)
        middle_layout.addWidget(lidar_group, 1)

        # ORTA: GPS VE HARİTA
        gps_group = QGroupBox("Operasyon Rotaları (GPS)")
        gps_layout = QVBoxLayout()

        self.lat_input = QLineEdit();
        self.lat_input.setPlaceholderText("Enlem (Örn: 40.6940)")
        self.lon_input = QLineEdit();
        self.lon_input.setPlaceholderText("Boylam (Örn: 29.5080)")
        gps_layout.addWidget(self.lat_input)
        gps_layout.addWidget(self.lon_input)

        btn_add = QPushButton("📍 Noktayı Listeye Ekle")
        btn_add.setStyleSheet("background-color: #333; padding: 10px;")
        btn_add.clicked.connect(self.add_coordinate)
        gps_layout.addWidget(btn_add)

        self.coord_list = QListWidget()
        gps_layout.addWidget(self.coord_list)

        btn_map = QPushButton("🗺️ Rota Haritasını Aç")
        btn_map.setStyleSheet("background-color: #00509e; padding: 10px; font-weight: bold;")
        btn_map.clicked.connect(self.open_map)
        gps_layout.addWidget(btn_map)

        gps_group.setLayout(gps_layout)
        middle_layout.addWidget(gps_group, 1)

        # SAĞ: KONTROL BUTONLARI VE LOG
        ctrl_group = QGroupBox("Taktik Komutlar")
        ctrl_layout = QVBoxLayout()

        btn_start = QPushButton("🚀 TAM OTONOM BAŞLAT")
        btn_start.setStyleSheet("background-color: #2e7d32; padding: 15px; font-weight: bold; font-size: 14px;")
        btn_start.clicked.connect(self.send_mission)
        ctrl_layout.addWidget(btn_start)

        btn_rtl = QPushButton("🏠 EVE DÖN (RTL)")
        btn_rtl.setStyleSheet("background-color: #d84315; padding: 15px; font-weight: bold; font-size: 14px;")
        btn_rtl.clicked.connect(self.send_rtl)
        ctrl_layout.addWidget(btn_rtl)

        btn_kill = QPushButton("🛑 ACİL DURDURMA")
        btn_kill.setStyleSheet("background-color: #b71c1c; padding: 15px; font-weight: bold; font-size: 14px;")
        btn_kill.clicked.connect(self.send_kill_switch)
        ctrl_layout.addWidget(btn_kill)

        self.log_screen = QTextEdit()
        self.log_screen.setReadOnly(True)
        self.log_screen.setStyleSheet("background-color: #000; color: #0f0; font-family: monospace;")
        ctrl_layout.addWidget(self.log_screen)

        ctrl_group.setLayout(ctrl_layout)
        middle_layout.addWidget(ctrl_group, 1)

        main_layout.addLayout(middle_layout)

        container = QWidget();
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Lidar Simülasyonu
        self.timer = QTimer()
        self.timer.timeout.connect(self.sim_lidar)
        self.timer.start(100)

    # --- FONKSİYONLAR ---
    def add_coordinate(self):
        if self.lat_input.text() and self.lon_input.text():
            self.coord_list.addItem(f"{self.lat_input.text()}, {self.lon_input.text()}")
            self.lat_input.clear();
            self.lon_input.clear()

    def open_map(self):
        import folium
        # Eklenen ilk koordinata haritayı ortala, yoksa Altınova'ya ortala
        start_loc = [40.6940, 29.5080]
        if self.coord_list.count() > 0:
            first_coord = self.coord_list.item(0).text().split(",")
            start_loc = [float(first_coord[0]), float(first_coord[1])]

        m = folium.Map(location=start_loc, zoom_start=16, tiles='CartoDB dark_matter')

        # Eklenen tüm noktaları haritaya çiz
        points = []
        for i in range(self.coord_list.count()):
            lat, lon = map(float, self.coord_list.item(i).text().split(","))
            points.append((lat, lon))
            folium.Marker([lat, lon], popup=f"Hedef {i + 1}", icon=folium.Icon(color='red', icon='info-sign')).add_to(m)

        if len(points) > 1:
            folium.PolyLine(points, color="blue", weight=2.5, opacity=0.8).add_to(m)

        dosya_yolu = os.path.abspath('rota_haritasi.html')
        m.save(dosya_yolu)
        webbrowser.open(f'file://{dosya_yolu}')
        self.log_screen.append("🗺️ Harita güncellendi ve tarayıcıda açıldı.")

    def sim_lidar(self):
        import random
        fake_data = [(i, random.uniform(3, 8)) for i in range(0, 360, 10)]
        self.lidar_view.update_data(fake_data)

    def send_mission(self):
        coords = [self.coord_list.item(i).text() for i in range(self.coord_list.count())]
        data = {"command": "GOREV_BUTCESI_BASLAT", "waypoints": coords}
        self.send_data(data)

    def send_rtl(self):
        self.send_data({"command": "EVE_DON_RTL"})

    def send_kill_switch(self):
        self.send_data({"command": "ACIL_DURDURMA"})

    def send_data(self, data_dict):
        msg = json.dumps(data_dict)
        if self.ser:
            self.ser.write((msg + "\n").encode())
        self.log_screen.append(f"📤 {msg}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YKIMerkez()
    window.show()
    sys.exit(app.exec())