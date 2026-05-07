import cv2
import json
import time
import sys
import numpy as np
from multiprocessing import Process, Queue, shared_memory
import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from cv_bridge import CvBridge
from geometry_msgs.msg import Point
from ultralytics import YOLO
from sensor_msgs.msg import CompressedImage
# --- KAMERA VE BELLEK AYARLARI ---
G_GENISLIK = 640
G_YUKSEKLIK = 480
G_KANAL = 3
G_BOYUT = G_GENISLIK * G_YUKSEKLIK * G_KANAL
G_SEKIL = (G_YUKSEKLIK, G_GENISLIK, G_KANAL)


# --- 1. SAF PYTHON YOLO SÜRECİ (OKUYUCU) ---
def yolo_hedef_tespiti_sureci(shm_adi, sinyal_q, kapi_q, hedef_q, ozet_q, debug_q, mod_q, renk_q):
    print("🚀 YOLO TensorRT Motoru Yükleniyor...")
    model = YOLO('TNA.engine', task='detect')
    print("✅ YOLO Başarıyla Yüklendi! Çift Tamponlama (Double-Buffer) Aktif.")

    # 1. Paylaşımlı Belleğe (RAM) İSMİYLE bağlanıyoruz
    mevcut_shm = shared_memory.SharedMemory(name=shm_adi)

    # 2. RAM'deki alanı İKİYE BÖLÜYORUZ (Buffer 0 ve Buffer 1)
    tampon_0 = np.ndarray(G_SEKIL, dtype=np.uint8, buffer=mevcut_shm.buf, offset=0)
    tampon_1 = np.ndarray(G_SEKIL, dtype=np.uint8, buffer=mevcut_shm.buf, offset=G_BOYUT)

    guncel_mod = "IHA_BEKLENIYOR"
    aranan_renk = None

    while True:
        if not mod_q.empty(): guncel_mod = mod_q.get_nowait()
        if not renk_q.empty(): aranan_renk = renk_q.get_nowait()

        # Telsizden (Queue) sinyal gelene kadar bekle
        if sinyal_q.empty():
            time.sleep(0.005)
            continue

        # Kameranın hangi tampona yazdığını öğren
        okunacak_indeks = sinyal_q.get()

        # 3. Kameranın yazdığı GÜNCEL tampondan kopyayı saniyesinde al
        # (Kopyalama çok hızlı bittiği için kamera o sırada diğer tampona yazmaya gidebilir)
        if okunacak_indeks == 0:
            cv_image = tampon_0.copy()
        else:
            cv_image = tampon_1.copy()

        # YOLO Çıkarımı
        results = model.track(cv_image, imgsz=1024, persist=True, tracker="bytetrack.yaml", verbose=False, conf=0.2)

        kirmizi_dubalar = []
        yesil_dubalar = []
        ozet_listesi = []

        for r in results:
            if not debug_q.full():
                debug_q.put(r.plot())

            for box in r.boxes:
                cls = int(box.cls[0])
                isim = model.names[cls].lower()
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0

                if guncel_mod == "GOREV_2_ENGEL_KACIS":
                    if "kirmizi" in isim or "red" in isim:
                        kirmizi_dubalar.append({'x': mx, 'y': my, 'alan': (x2 - x1) * (y2 - y1)})
                        ozet_listesi.append({"renk": "kirmizi", "x": float(mx)})
                    elif "yesil" in isim or "green" in isim:
                        yesil_dubalar.append({'x': mx, 'y': my, 'alan': (x2 - x1) * (y2 - y1)})
                        ozet_listesi.append({"renk": "yesil", "x": float(mx)})

                elif guncel_mod == "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR" and aranan_renk:
                    if aranan_renk.lower() in isim:
                        hedef_q.put({'x': mx, 'y': my, 'z': float(x2 - x1)})
                        ozet_listesi.append({"renk": aranan_renk, "x": float(mx)})

        if ozet_listesi:
            ozet_q.put(json.dumps(ozet_listesi))

        if guncel_mod == "GOREV_2_ENGEL_KACIS":
            orta_x = None
            if kirmizi_dubalar and yesil_dubalar:
                orta_x = (max(kirmizi_dubalar, key=lambda d: d['alan'])['x'] +
                          max(yesil_dubalar, key=lambda d: d['alan'])['x']) / 2.0
            elif kirmizi_dubalar:
                orta_x = max(kirmizi_dubalar, key=lambda d: d['alan'])['x'] + 250.0
            elif yesil_dubalar:
                orta_x = max(yesil_dubalar, key=lambda d: d['alan'])['x'] - 250.0

            if orta_x is not None:
                kapi_q.put({'x': orta_x, 'y': 240.0, 'z': 0.0})


# --- 2. ROS KÖPRÜSÜ (YAZICI) ---
# --- 2. ROS KÖPRÜSÜ (YAZICI) ---
class YoloRosBridge(Node):
    def __init__(self, shm_adi, sinyal_q, kapi_q, hedef_q, debug_q, ozet_q, mod_q):
        super().__init__('yolo_bridge_node')
        self.br = CvBridge()

        self.mevcut_shm = shared_memory.SharedMemory(name=shm_adi)
        self.tampon_0 = np.ndarray(G_SEKIL, dtype=np.uint8, buffer=self.mevcut_shm.buf, offset=0)
        self.tampon_1 = np.ndarray(G_SEKIL, dtype=np.uint8, buffer=self.mevcut_shm.buf, offset=G_BOYUT)

        self.sinyal_q = sinyal_q
        self.yazilacak_indeks = 0

        self.debug_q = debug_q
        self.kapi_q = kapi_q
        self.ozet_q = ozet_q
        self.mod_q = mod_q

        # DEĞİŞİKLİK 1: Artık CompressedImage yayınlıyoruz
        self.debug_pub = self.create_publisher(CompressedImage, '/yolo_debug_goruntu/compressed', 10)
        self.ozet_pub = self.create_publisher(String, '/yolo_tespit_ozeti', 10)
        self.kapi_pub = self.create_publisher(Point, '/kapi_merkez_koordinat', 10)

        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)

        self.cap = cv2.VideoCapture(1)
        self.create_timer(0.04, self.dongu)

    def mod_callback(self, msg):
        if not self.mod_q.full():
            self.mod_q.put(msg.data)

    def dongu(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (G_GENISLIK, G_YUKSEKLIK))

            if self.yazilacak_indeks == 0:
                self.tampon_0[:] = frame[:]
            else:
                self.tampon_1[:] = frame[:]

            if self.sinyal_q.full():
                try:
                    self.sinyal_q.get_nowait()
                except:
                    pass

            self.sinyal_q.put(self.yazilacak_indeks)
            self.yazilacak_indeks = 1 - self.yazilacak_indeks

            # --- DEĞİŞİKLİK 2: CPU KURTARICI (SIKIŞTIRMA VE BOYUT KÜÇÜLTME) ---
            if not self.debug_q.empty():
                ham_goruntu = self.debug_q.get()

                # 1. Çözünürlüğü Düşür (Arayüzde görmek için 320x240 fazlasıyla yeterli)
                kucuk_goruntu = cv2.resize(ham_goruntu, (320, 240))

                # 2. JPEG formatında %50 kalite ile sıkıştır
                basari, kodlanmis_resim = cv2.imencode('.jpg', kucuk_goruntu, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

                if basari:
                    msg = CompressedImage()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.format = "jpeg"
                    msg.data = np.array(kodlanmis_resim).tobytes()  # Byte array'e çevirip bas
                    self.debug_pub.publish(msg)
            # -----------------------------------------------------------------

            if not self.ozet_q.empty():
                msg = String()
                msg.data = self.ozet_q.get()
                self.ozet_pub.publish(msg)

            if not self.kapi_q.empty():
                veri = self.kapi_q.get()
                self.kapi_pub.publish(Point(x=float(veri['x']), y=float(veri['y']), z=0.0))


if __name__ == '__main__':
    # 1. ANA RAM HAVUZUNU OLUŞTUR (Normal boyutun 2 KATI büyüklüğünde yer açıyoruz!)
    shm = shared_memory.SharedMemory(create=True, size=G_BOYUT * 2)

    # 2. KUYRUKLAR
    sinyal_q = Queue(maxsize=1)
    k_q = Queue();
    h_q = Queue();
    o_q = Queue();
    d_q = Queue(maxsize=1);
    m_q = Queue(maxsize=1);
    r_q = Queue()

    # 3. YOLO SÜRECİNE RAM İSMİNİ GÖNDER
    yolo_p = Process(target=yolo_hedef_tespiti_sureci,
                     args=(shm.name, sinyal_q, k_q, h_q, o_q, d_q, m_q, r_q))
    yolo_p.start()

    rclpy.init()
    bridge = YoloRosBridge(shm.name, sinyal_q, k_q, h_q, d_q, o_q, m_q)

    m_q.put("GOREV_2_ENGEL_KACIS")

    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n🧹 Sistem Kapatılıyor, Çift Tamponlu Bellek Temizleniyor...")
        bridge.cap.release()
        yolo_p.terminate()
        yolo_p.join()

        # ÇÖP TOPLAMA
        shm.close()
        shm.unlink()

        rclpy.shutdown()
        sys.exit(0)