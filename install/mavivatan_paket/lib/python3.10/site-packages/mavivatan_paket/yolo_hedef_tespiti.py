import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import json

# BU SATIRIN EKSİK OLMADIĞINDAN VEYA YORUMDA OLMADIĞINDAN EMİN OL:
from ultralytics import YOLO
class YoloHedefTespiti(Node):
    def __init__(self):
        super().__init__('yolo_hedef_tespiti_node')
        self.br = CvBridge()
        self.guncel_mod = "IHA_BEKLENIYOR"
        self.aranan_renk = None
        self.ozet_pub = self.create_publisher(String, '/yolo_tespit_ozeti', 10)

        self.model = YOLO('yolo8n.pt', task='detect')
        self.debug_pub = self.create_publisher(Image, '/yolo_debug_goruntu', 10)

        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)
        self.create_subscription(String, 'iha_hedef_rengi', self.renk_callback, 10)
        self.create_subscription(Image, '/zed/zed_node/rgb/color/rect/image', self.kamera_callback, 10)

        # Dubaların koordinatlarını basacağımız kanallar
        self.kapi_orta_nokta_pub = self.create_publisher(Point, 'kapi_merkez_koordinat', 10)
        self.hedef_pub = self.create_publisher(Point, 'hedef_koordinat', 10)

    def mod_callback(self, msg):
        self.guncel_mod = msg.data

    def renk_callback(self, msg):
        self.aranan_renk = msg.data

    def kamera_callback(self, data):
        try:
            cv_image = self.br.imgmsg_to_cv2(data, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Görüntü hatası: {e}")
            return

        results = self.model.track(cv_image, imgsz=1024, persist=True, tracker="bytetrack.yaml", verbose=False, conf=0.5)
        # --- CANLI YAYIN / GÖRSELLEŞTİRME EKLENTİSİ ---
        cizimli_goruntu = results[0].plot()

        # Görüntüyü OpenCV penceresine değil, ROS üzerinden ARAYÜZE fırlatıyoruz!
        try:
            debug_msg = self.br.cv2_to_imgmsg(cizimli_goruntu, encoding="bgr8")
            self.debug_pub.publish(debug_msg)
        except Exception as e:
            pass
        # ----------------------------------------------
        kirmizi_dubalar = []
        yesil_dubalar = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                isim = self.model.names[cls]
                x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0

                # --- GÖREV 2: KANAL GEÇİŞİ MANTIĞI (Duba Sınıflandırma) ---
                if self.guncel_mod == "GOREV_2_ENGEL_KACIS":
                    if "person" in isim.lower():
                        kirmizi_dubalar.append({'x': mx, 'y': my, 'alan': (x2 - x1) * (y2 - y1)})
                    elif "bottle" in isim.lower():
                        yesil_dubalar.append({'x': mx, 'y': my, 'alan': (x2 - x1) * (y2 - y1)})

                # --- GÖREV 3: KAMİKAZE MANTIĞI ---
                elif self.guncel_mod == "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR" and self.aranan_renk and self.aranan_renk.lower() in isim.lower():
                    kutu_genisligi = float(x2 - x1)
                    h_msg = Point(x=mx, y=my, z=kutu_genisligi)
                    self.hedef_pub.publish(h_msg)

        # --- GÖREV 2: OFSET VE MERKEZ HESAPLAMA ---
        if self.guncel_mod == "GOREV_2_ENGEL_KACIS":
            orta_x = None
            orta_y = None

            if kirmizi_dubalar and yesil_dubalar:
                en_yakin_k = max(kirmizi_dubalar, key=lambda d: d['alan'])
                en_yakin_y = max(yesil_dubalar, key=lambda d: d['alan'])
                orta_x = (en_yakin_k['x'] + en_yakin_y['x']) / 2.0
                orta_y = (en_yakin_k['y'] + en_yakin_y['y']) / 2.0
                self.get_logger().info("🚪 KAPI BULUNDU: Tam merkeze gidiliyor.")

            elif kirmizi_dubalar:
                en_yakin_k = max(kirmizi_dubalar, key=lambda d: d['alan'])
                orta_x = en_yakin_k['x'] + 250.0
                orta_y = en_yakin_k['y']
                self.get_logger().warn("⚠️ Sadece Kırmızı görüldü! Sağa ofset verilerek geçiliyor.")

            elif yesil_dubalar:
                en_yakin_y = max(yesil_dubalar, key=lambda d: d['alan'])
                orta_x = en_yakin_y['x'] - 250.0
                orta_y = en_yakin_y['y']
                self.get_logger().warn("⚠️ Sadece Yeşil görüldü! Sola ofset verilerek geçiliyor.")

            if orta_x is not None:
                self.kapi_orta_nokta_pub.publish(Point(x=orta_x, y=orta_y, z=0.0))

        # ---------------------------------------------------------
        # --- COST MAP İÇİN JSON ÖZETİ YAYINLA (GİRİNTİ DÜZELTİLDİ) ---
        # ---------------------------------------------------------
        ozet_listesi = []
        for duba in kirmizi_dubalar:
            ozet_listesi.append({"renk": "kirmizi", "x": duba['x']})
        for duba in yesil_dubalar:
            ozet_listesi.append({"renk": "yesil", "x": duba['x']})

        if self.guncel_mod == "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR" and self.aranan_renk:
            for r in results:
                for box in r.boxes:
                    isim = self.model.names[int(box.cls[0])]
                    if self.aranan_renk.lower() in isim.lower():
                        mx = (box.xyxy[0][0] + box.xyxy[0][2]) / 2.0
                        ozet_listesi.append({"renk": self.aranan_renk.lower(), "x": float(mx)})

        msg_ozet = String()
        msg_ozet.data = json.dumps(ozet_listesi)
        self.ozet_pub.publish(msg_ozet)

def main(args=None):
    rclpy.init(args=args)
    node = YoloHedefTespiti()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()