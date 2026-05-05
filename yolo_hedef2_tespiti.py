import cv2
import json
import time
import signal
import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
from geometry_msgs.msg import Point
from multiprocessing import Process, Queue
from ultralytics import YOLO
import numpy as np
from multiprocessing import shared_memory

# --- 1. SAF PYTHON YOLO SÜRECİ (ARKA PLAN) ---
def yolo_hedef_tespiti_sureci(goruntu_q, kapi_q, hedef_q, ozet_q, debug_q, mod_q, renk_q):
    print("🚀 YOLO TensorRT Motoru Yükleniyor...")
    model = YOLO('TNA.engine', task='detect')
    print("✅ YOLO Başarıyla Yüklendi!")

    guncel_mod = "IHA_BEKLENIYOR"
    aranan_renk = None

    while True:
        if not mod_q.empty(): guncel_mod = mod_q.get_nowait()
        if not renk_q.empty(): aranan_renk = renk_q.get_nowait()

        if goruntu_q.empty():
            time.sleep(0.01)
            continue

        cv_image = goruntu_q.get()
        results = model.track(cv_image, imgsz=1024, persist=True, tracker="bytetrack.yaml", verbose=False, conf=0.2)

        kirmizi_dubalar = []
        yesil_dubalar = []
        ozet_listesi = []  # ARAYÜZDEKİ RADAR İÇİN EKLENDİ

        for r in results:
            if not debug_q.full():
                debug_q.put(r.plot())

            for box in r.boxes:
                cls = int(box.cls[0])
                isim = model.names[cls].lower()
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0

                print(f"🔍 Tespit: {isim} [%{conf * 100:.1f}]")

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

        # Radarı (Costmap) Güncellemek İçin Veriyi Kuyruğa At
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
                # ÖNEMLİ: Çözünürlük 1024 olduğu için Y ekseni 512 olmalı!
                kapi_q.put({'x': orta_x, 'y': 512.0, 'z': 0.0})


# --- 2. ROS KÖPRÜSÜ (ÖN PLAN) ---
class YoloRosBridge(Node):
    def __init__(self, goruntu_q, kapi_q, hedef_q, debug_q, ozet_q, mod_q):
        super().__init__('yolo_bridge_node')
        self.br = CvBridge()
        self.goruntu_q = goruntu_q
        self.debug_q = debug_q
        self.kapi_q = kapi_q
        self.ozet_q = ozet_q
        self.mod_q = mod_q

        # Arayüze Veri Basan Yayıncılar
        self.debug_pub = self.create_publisher(Image, '/yolo_debug_goruntu', 10)
        self.ozet_pub = self.create_publisher(String, '/yolo_tespit_ozeti', 10)
        self.kapi_pub = self.create_publisher(Point, '/kapi_merkez_koordinat', 10)

        # Görev Yöneticisinden Gelen Modu Dinle
        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)

        # Kamerayı SADECE BURADA açıyoruz
        self.cap = cv2.VideoCapture(0)
        self.create_timer(0.04, self.dongu)  # ~25 FPS

    def mod_callback(self, msg):
        if not self.mod_q.full():
            self.mod_q.put(msg.data)

    def dongu(self):
        ret, frame = self.cap.read()
        if ret:
            if not self.goruntu_q.full():
                self.goruntu_q.put(frame)

            if not self.debug_q.empty():
                self.debug_pub.publish(self.br.cv2_to_imgmsg(self.debug_q.get(), "bgr8"))

            if not self.ozet_q.empty():
                msg = String()
                msg.data = self.ozet_q.get()
                self.ozet_pub.publish(msg)

            if not self.kapi_q.empty():
                veri = self.kapi_q.get()
                self.kapi_pub.publish(Point(x=float(veri['x']), y=float(veri['y']), z=0.0))


if __name__ == '__main__':
    g_q = Queue(maxsize=1);
    k_q = Queue();
    h_q = Queue();
    o_q = Queue();
    d_q = Queue(maxsize=1);
    m_q = Queue(maxsize=1);
    r_q = Queue()

    yolo_p = Process(target=yolo_hedef_tespiti_sureci, args=(g_q, k_q, h_q, o_q, d_q, m_q, r_q))
    yolo_p.start()

    rclpy.init()
    bridge = YoloRosBridge(g_q, k_q, h_q, d_q, o_q, m_q)

    # Test için ilk başta görev 2'yi aktif edelim
    m_q.put("GOREV_2_ENGEL_KACIS")

    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n🧹 Sistem Kapatılıyor...")
        bridge.cap.release()
        yolo_p.terminate()
        yolo_p.join()
        rclpy.shutdown()
        sys.exit(0)