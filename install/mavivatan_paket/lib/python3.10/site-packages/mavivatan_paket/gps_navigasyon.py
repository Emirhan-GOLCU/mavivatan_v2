import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64
import math
import json
from sensor_msgs.msg import Imu

class GPSNavigasyon(Node):
    def __init__(self):
        super().__init__('gps_navigasyon_node')
        self.guncel_mod = "IHA_BEKLENIYOR"
        # ... (diğer init kodların) ...
        self.rota_gorev_1 = []  # Kanal girişine kadar olan yol
        self.hedef_gorev_3 = None  # Kamikaze başlangıç koordinatı
        self.hedef_indeks = 0
        # Teknenin Konumu
        self.mevcut_enlem = None
        self.mevcut_boylam = None
        self.mevcut_pusula = 0.0

        # Rota (YKİ'den gelecek waypoint'ler)
        self.hedefler = []
        self.hedef_indeks = 0

        # Lidar Engel Durumu
        self.engel_var = False
        self.kacis_hizi_z = 0.0

        # Abonelikler
        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)
        self.create_subscription(String, '/yki_komut', self.yki_callback, 10)  # Rotaları almak için
        self.create_subscription(NavSatFix, '/mavros/global_position/global', self.gps_callback, 10)
        self.create_subscription(Imu, '/zed/zed_node/imu/data', self.pusula_callback, 10)
        self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)  # LİDAR EKLENDİ

        # Yayımcılar
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.durum_pub = self.create_publisher(String, 'gorev_durumu', 10)

        # 0.5 saniyede bir karar döngüsü çalışır
        self.create_timer(0.5, self.navigasyon_dongusu)

    def mod_callback(self, msg):
        self.guncel_mod = msg.data

    def quaternion_to_yaw(self, x, y, z, w):
        # Quaternion'dan Z ekseni (Yaw/Pusula) açısını Derece cinsinden çeker
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_radyan = math.atan2(t3, t4)
        return math.degrees(yaw_radyan)

    def yki_callback(self, msg):
        try:
            paket = json.loads(msg.data)

            # YKİ'den gelen JSON artık şu formatta olmalı:
            # {"task1_waypoints": ["lat,lon", ...], "task3_waypoint": "lat,lon"}

            if "task1_waypoints" in paket:
                self.rota_gorev_1 = []
                for pt in paket["task1_waypoints"]:
                    lat, lon = map(float, pt.split(","))
                    self.rota_gorev_1.append({"lat": lat, "lon": lon})

            if "task3_waypoint" in paket:
                lat, lon = map(float, paket["task3_waypoint"].split(","))
                self.hedef_gorev_3 = {"lat": lat, "lon": lon}

            self.hedef_indeks = 0
            self.get_logger().info("🗺️ Operasyon Planı Alındı! Görev 1 ve Görev 3 noktaları ayrıştırıldı.")
        except Exception as e:
            self.get_logger().error(f"Paket ayrıştırma hatası: {e}")

    def gps_callback(self, msg):
        self.mevcut_enlem = msg.latitude
        self.mevcut_boylam = msg.longitude

    def pusula_callback(self, msg):
        q = msg.orientation
        # ZED 2i'nin manyetometre ve jiroskop verisini dereceye çevir
        yaw_acisi = self.quaternion_to_yaw(q.x, q.y, q.z, q.w)

        # ZED açısı ile standart harita kuzeyini eşleştir
        self.mevcut_pusula = yaw_acisi
        # self.get_logger().info(f"🧭 ZED Pusula: {self.mevcut_pusula:.1f} Derece", throttle_duration_sec=2.0)
    def lidar_callback(self, msg):
        # ÖNEMLİ: Her iki GPS modunda da engel kaçınma aktif olmalı
        gps_aktif_modlar = ["GOREV_1_NOKTA_TAKIP", "GOREV_3_GPS_INTIKAL"]
        if self.guncel_mod not in gps_aktif_modlar:
            return

        temiz_veriler = [x if 0.1 < x < 10.0 else 10.0 for x in msg.ranges]
        try:
            sol_mesafe = min(temiz_veriler[30:90])
            on_mesafe = min(min(temiz_veriler[330:359]), min(temiz_veriler[0:30]))
            sag_mesafe = min(temiz_veriler[270:330])
        except ValueError:
            return

        if on_mesafe < 4.0:
            self.engel_var = True
            if sol_mesafe > sag_mesafe:
                self.kacis_hizi_z = 0.5
            else:
                self.kacis_hizi_z = -0.5
        else:
            self.engel_var = False

    def haversine_mesafe(self, lat1, lon1, lat2, lon2):
        # İki koordinat arası metre cinsinden gerçek mesafe hesaplama
        R = 6371000  # Dünya yarıçapı (metre)
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def navigasyon_dongusu(self):
        # 1. HEDEF SEÇİCİ
        aktif_hedef = None
        if self.guncel_mod == "GOREV_1_NOKTA_TAKIP" and self.rota_gorev_1:
            if self.hedef_indeks < len(self.rota_gorev_1):
                aktif_hedef = self.rota_gorev_1[self.hedef_indeks]
        elif self.guncel_mod == "GOREV_3_GPS_INTIKAL" and self.hedef_gorev_3:
            aktif_hedef = self.hedef_gorev_3

        if not aktif_hedef or self.mevcut_enlem is None:
            return

        # 2. MESAFE HESABI
        mesafe = self.haversine_mesafe(self.mevcut_enlem, self.mevcut_boylam, aktif_hedef["lat"], aktif_hedef["lon"])

        # 3. VARILDI KONTROLÜ
        if mesafe < 3.0:
            if self.guncel_mod == "GOREV_1_NOKTA_TAKIP":
                self.hedef_indeks += 1
                self.get_logger().info(f"✅ NOKTA {self.hedef_indeks} TAMAMLANDI!")
                if self.hedef_indeks >= len(self.rota_gorev_1):
                    self.bitis_bildir("GOREV_1_TAMAMLANDI", "🚩 Görev 1 Rotası Bitti. Kanal moduna geçiliyor.")
                    return
            elif self.guncel_mod == "GOREV_3_GPS_INTIKAL":
                self.bitis_bildir("GOREV_3_INTIKAL_TAMAMLANDI", "🎯 Kamikaze Alanına Varıldı. Görsel Arama Başlıyor.")
                return

        # 4. SÜRÜŞ MANTIĞI
        cmd = Twist()
        if self.engel_var:
            cmd.linear.x = 0.2
            cmd.angular.z = self.kacis_hizi_z
        else:
            cmd.linear.x = 0.5
            hedef_aci = math.degrees(math.atan2(aktif_hedef["lon"] - self.mevcut_boylam, aktif_hedef["lat"] - self.mevcut_enlem))
            aci_farki = (hedef_aci - self.mevcut_pusula + 180) % 360 - 180
            cmd.angular.z = max(-0.5, min(0.5, aci_farki * 0.02))
            self.get_logger().info(f"🚢 {self.guncel_mod} | Mesafe: {mesafe:.1f}m", throttle_duration_sec=1.0)

        self.cmd_pub.publish(cmd)

    def bitis_bildir(self, mesaj_metni, log_metni):
        self.cmd_pub.publish(Twist())
        msg = String(); msg.data = mesaj_metni
        self.durum_pub.publish(msg)
        self.get_logger().warn(log_metni)
        self.hedef_indeks = 0 # Bir sonraki görev için sıfırla

def main(args=None):
    rclpy.init(args=args)
    node = GPSNavigasyon()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()