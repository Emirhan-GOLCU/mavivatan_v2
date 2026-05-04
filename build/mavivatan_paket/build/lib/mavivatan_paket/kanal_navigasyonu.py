import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import time
import math

class KanalNavigasyonu(Node):
    def __init__(self):
        super().__init__('kanal_navigasyonu_node')
        self.guncel_mod = "IHA_BEKLENIYOR"

        self.kamera_merkez_x = 320.0
        self.hedef_kapi_x = None
        self.son_gorme_zamani = 0
        self.acil_durum = False

        # --- PARKUR BİTİŞ SAYACI ---
        self.temiz_yol_sayaci = 0
        self.parkur_bitis_esigi = 25  # Yaklaşık 5 saniye boyunca etraf tamamen boşsa

        # Abonelikler
        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)
        self.create_subscription(Point, '/kapi_merkez_koordinat', self.yolo_callback, 10)
        self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)

        # Yayımcılar
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.durum_bildir_pub = self.create_publisher(String, 'gorev_durumu', 10)  # BİTİŞ İÇİN EKLENDİ

        # Otonomi Döngüsü (Saniyede 5 kez çalışır)
        self.create_timer(0.2, self.kontrol_dongusu)
        self.get_logger().info("Kanal Navigasyonu (Görev 2) Uykuda, Emir Bekliyor...")

    def mod_callback(self, msg):
        self.guncel_mod = msg.data

    def yolo_callback(self, msg):
        if self.guncel_mod != "GOREV_2_ENGEL_KACIS": return
        self.hedef_kapi_x = msg.x
        self.son_gorme_zamani = time.time()

    def lidar_callback(self, msg):
        if self.guncel_mod != "GOREV_2_ENGEL_KACIS": return

        temiz_veriler = []
        for x in msg.ranges:
            if math.isnan(x) or math.isinf(x) or x == 0.0:
                temiz_veriler.append(10.0)
            elif x < 0.15:
                temiz_veriler.append(0.1)  # Kaza riski!
            elif x > 10.0:
                temiz_veriler.append(10.0)
            else:
                temiz_veriler.append(x)

        # Dinamik Çözünürlük Çarpanı
        toplam_nokta = len(temiz_veriler)
        carpan = toplam_nokta / 360.0

        sol_bas, sol_bitis = int(30 * carpan), int(90 * carpan)
        on_sag, on_sol = int(330 * carpan), int(30 * carpan)
        sag_bas, sag_bitis = int(270 * carpan), int(330 * carpan)

        try:
            sol_mesafe = min(temiz_veriler[sol_bas:sol_bitis])
            on_mesafe = min(min(temiz_veriler[on_sag:]), min(temiz_veriler[:on_sol]))
            sag_mesafe = min(temiz_veriler[sag_bas:sag_bitis])
        except ValueError:
            return
        # 1. Acil Durum Çarpışma Kontrolü
        if on_mesafe < 1.2:
            self.acil_durum = True
            self.temiz_yol_sayaci = 0
        else:
            self.acil_durum = False

        # 2. Parkur Bitti mi? (Sağ, Sol ve Ön 5 metreden açıksa kanaldan çıkmışızdır)
        if sol_mesafe > 5.0 and sag_mesafe > 5.0 and on_mesafe > 5.0:
            self.temiz_yol_sayaci += 1
        else:
            self.temiz_yol_sayaci = 0

    def kontrol_dongusu(self):
        if self.guncel_mod != "GOREV_2_ENGEL_KACIS": return

        cmd = Twist()

        # --- GÖREV BİTİRME KONTROLÜ ---
        if self.temiz_yol_sayaci > self.parkur_bitis_esigi:
            self.get_logger().warn("✅ KANAL GEÇİLDİ! Görev 2 bitti, Kamikaze'ye (GÖREV 3) geçiş bildiriliyor!")
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.cmd_pub.publish(cmd)

            bitti_msg = String()
            bitti_msg.data = "GOREV_2_TAMAMLANDI"
            self.durum_bildir_pub.publish(bitti_msg)

            self.temiz_yol_sayaci = -999999  # Sürekli tetiklenmemesi için
            return

        # 1. ACİL DURUM KONTROLÜ (Lidar kamerayı ezer)
        if self.acil_durum:
            self.get_logger().warn("🛑 LİDAR: ÇARPIŞMA RİSKİ! Motorlar durduruluyor!")
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.cmd_pub.publish(cmd)
            return

        # 2. GÖRÜŞ KAYBI KONTROLÜ (2 saniyedir kapı göremiyorsak)
        if self.hedef_kapi_x is None or (time.time() - self.son_gorme_zamani) > 2.0:
            self.get_logger().info("🔍 Kapı aranıyor... (Kamera verisi yok)")
            cmd.linear.x = 0.1
            cmd.angular.z = 0.3  # Etrafı taramak için
            self.cmd_pub.publish(cmd)
            return

        # 3. KAPIYI HİZALAMA (Görsel P-Kontrolcü)
        hata = self.kamera_merkez_x - self.hedef_kapi_x
        cmd.linear.x = 0.4
        cmd.angular.z = hata * 0.002
        cmd.angular.z = max(-0.5, min(0.5, cmd.angular.z))

        self.get_logger().info(f"🚢 Kanalda İlerleniyor | Hata: {hata:.1f}px | Dümen: {cmd.angular.z:.2f}")
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = KanalNavigasyonu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()