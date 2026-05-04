import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from std_msgs.msg import String
from cv_bridge import CvBridge
import numpy as np


class SensorFuzyonu(Node):
    def __init__(self):
        super().__init__('sensor_fuzyonu_node')
        self.br = CvBridge()
        self.guncel_mod = "IHA_BEKLENIYOR"

        # YOLO'dan gelecek aktif hedefin pikselleri
        self.aktif_hedef_x = None
        self.aktif_hedef_y = None

        # Abonelikler (Hem beyni, hem Gözleri dinliyoruz)
        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)
        self.create_subscription(Point, 'kapi_merkez_koordinat', self.kapi_callback, 10)  # Görev 2'den gelir
        self.create_subscription(Point, 'hedef_koordinat', self.hedef_callback, 10)  # Görev 3'ten gelir

        # ZED Kameranın Metrik Derinlik Haritası (32-bit Float formatında)
        self.create_subscription(Image, '/zed/zed_node/depth/depth_registered', self.derinlik_callback, 10)

        # Navigasyona gidecek gerçek 3D Koordinat Yayımcısı
        self.hedef_3d_pub = self.create_publisher(Point, 'hedef_3d_gercek_konum', 10)

        # ZED Kamera / Optik Parametreler (640x480 çözünürlüğe göre optimize edilmiştir)
        self.ekran_merkez_x = 320.0
        self.odak_uzakligi_fx = 350.0  # ZED'in calibration dosyasından alınan yaklaşık fx değeri

    def mod_callback(self, msg):
        self.guncel_mod = msg.data

    def kapi_callback(self, msg):
        if self.guncel_mod == "GOREV_2_ENGEL_KACIS":
            self.aktif_hedef_x = int(msg.x)
            self.aktif_hedef_y = int(msg.y)

    def hedef_callback(self, msg):
        if self.guncel_mod == "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR":
            self.aktif_hedef_x = int(msg.x)
            self.aktif_hedef_y = int(msg.y)

    def derinlik_callback(self, msg):
        # Eğer henüz YOLO bir şey bulamadıysa veya görevde değilsek Jetson Nano'yu yorma!
        if self.aktif_hedef_x is None or self.aktif_hedef_y is None:
            return
        if self.guncel_mod not in ["GOREV_2_ENGEL_KACIS", "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR"]:
            return

        try:
            # Görüntüyü Numpy matrisine çevir (Her bir piksel metre cinsinden mesafe tutar)
            cv_depth_image = self.br.imgmsg_to_cv2(msg, desired_encoding="32FC1")
        except Exception as e:
            self.get_logger().error(f"Derinlik çeviri hatası: {e}")
            return

        h, w = cv_depth_image.shape
        x = max(0, min(w - 1, self.aktif_hedef_x))
        y = max(0, min(h - 1, self.aktif_hedef_y))

        # 1. Z Eksenini (İleri Uzaklık) Oku
        mesafe_z = float(cv_depth_image[y, x])

        # Eğer güneş parlaması vs. yüzünden ZED o pikselin derinliğini okuyamadıysa (NaN döner)
        if np.isnan(mesafe_z) or np.isinf(mesafe_z):
            mesafe_z = 5.0  # Sistemi çökertmemek için 5 metre uzağımızdaymış gibi davran

        # 2. X Eksenini (Yanal Sapma) Hesapla
        # Formül: (Piksel_X - Merkez_X) * Z_Mesafe / Odak_Uzaklığı
        # Sonuç pozitifse hedef SAĞDA, negatifse SOLDA demektir.
        sapma_x = (x - self.ekran_merkez_x) * mesafe_z / self.odak_uzakligi_fx

        # 3. Gerçek 3D Noktayı Navigasyona Fırlat
        hedef_3d_msg = Point()
        hedef_3d_msg.x = sapma_x  # Sağ/Sol sapma (metre)
        hedef_3d_msg.y = 0.0  # İrtifa (İDA yüzeyde olduğu için hep 0)
        hedef_3d_msg.z = mesafe_z  # İleri uzaklık (metre)

        self.hedef_3d_pub.publish(hedef_3d_msg)

        # Test için log (Yarışmada kapatabilirsin)
        # self.get_logger().info(f"📐 3D HEDEF | Uzaklık: {mesafe_z:.2f}m | Yanal Sapma: {sapma_x:.2f}m")


def main(args=None):
    rclpy.init(args=args)
    node = SensorFuzyonu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()