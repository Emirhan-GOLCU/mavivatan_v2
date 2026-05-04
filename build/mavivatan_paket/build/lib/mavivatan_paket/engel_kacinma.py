import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

import math
class EngelKacinma(Node):
    def __init__(self):
        super().__init__('engel_kacinma_node')

        self.guncel_mod = "IHA_BEKLENIYOR"
        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)

        # RPLidar'dan gelen lazer tarama verisini dinliyoruz
        self.create_subscription(LaserScan, '/scan', self.lidar_callback, 10)

        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.durum_bildir_pub = self.create_publisher(String, 'gorev_durumu', 10)

        # Güvenlik ve Hız Parametreleri
        self.guvenli_mesafe = 2.5  # Bir engele 2.5 metreden fazla yaklaşırsak manevra yap
        self.temel_hiz = 0.5  # Kanal içindeki standart ileri hız

        # Görev bitirme sayacı (Önümüz belli bir süre tamamen boş kalırsa parkur bitti demektir)
        self.temiz_yol_sayaci = 0
        self.parkur_bitis_esigi = 50  # Lidar saniyede ~10 kere veri yollasa, 5 saniye boşluk demek

    def mod_callback(self, msg):
        self.guncel_mod = msg.data

    def lidar_callback(self, msg):
        # Sadece GÖREV 2 modundaysak çalış!
        if self.guncel_mod != "GOREV_2_ENGEL_KACIS":
            return

        # Lidar ranges dizisindeki Sonsuz (inf) ve NaN değerleri temizle, en fazla 10 metre algıla
        temiz_veriler = []
        for x in msg.ranges:
            if math.isnan(x) or math.isinf(x) or x == 0.0:
                temiz_veriler.append(10.0)  # Tamamen boşluk
            elif x < 0.15:
                # 15 cm'den küçük değerler genelde donanım hatası veya çok dibimizdeki cisimlerdir
                temiz_veriler.append(0.1)  # Acil kaçış tetiklenmesi için küçük bir değer ata
            elif x > 10.0:
                temiz_veriler.append(10.0)
            else:
                temiz_veriler.append(x)
        # RPLidar için 0 derece genellikle tam önü temsil eder. Toplam 360 derece.
        # Ön: 330-360 ve 0-30 | Sol: 30-90 | Sağ: 270-330
        try:
            # Diziyi sektörlere böl ve her sektördeki EN YAKIN engeli bul
            sol_mesafe = min(temiz_veriler[30:90])
            on_mesafe = min(min(temiz_veriler[330:359]), min(temiz_veriler[0:30]))
            sag_mesafe = min(temiz_veriler[270:330])
        except ValueError:
            # Dizi boş gelirse aracı durdur
            return

        cmd = Twist()

        # OTONOM KAÇIŞ ALGORİTMASI
        if on_mesafe > self.guvenli_mesafe:
            # Önümüz boş! Düz git.
            cmd.linear.x = self.temel_hiz
            cmd.angular.z = 0.0

            # Eğer önümüz, sağımız ve solumuz çok açıksa (kanaldan çıkmışız demektir)
            if sol_mesafe > 5.0 and sag_mesafe > 5.0 and on_mesafe > 5.0:
                self.temiz_yol_sayaci += 1
            else:
                self.temiz_yol_sayaci = 0  # Tekrar dubaların arasına girdik, sayacı sıfırla

        else:
            # ÖNÜMÜZDE ENGEL VAR! Kaçış manevrası başlat.
            self.temiz_yol_sayaci = 0
            cmd.linear.x = 0.2  # Manevra yaparken hızı düşür (Jetson Nano'ya hesaplama payı bırak)

            # Hangi taraf daha boşsa oraya dön
            if sol_mesafe > sag_mesafe:
                # Sol daha açık, sola kır (Diferansiyel motorda pozitif = Sola dönüş varsayımıyla)
                cmd.angular.z = 0.5
                self.get_logger().info(f"🚧 Engel Önümüzde! SOLA dönülüyor. (Mesafe: {on_mesafe:.1f}m)")
            else:
                # Sağ daha açık, sağa kır
                cmd.angular.z = -0.5
                self.get_logger().info(f"🚧 Engel Önümüzde! SAĞA dönülüyor. (Mesafe: {on_mesafe:.1f}m)")

        self.cmd_pub.publish(cmd)

        # PARKUR BİTİŞ KONTROLÜ
        if self.temiz_yol_sayaci > self.parkur_bitis_esigi:
            # Aracı durdur
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.cmd_pub.publish(cmd)

            # Beyne haber ver! GÖREV 2 Bitti, Kamikaze'ye (GÖREV 3) geç!
            bitti_msg = String()
            bitti_msg.data = "GOREV_2_TAMAMLANDI"
            self.durum_bildir_pub.publish(bitti_msg)

            self.get_logger().warn("✅ KANAL GEÇİLDİ! Engel parkuru bitti, Kamikaze başlıyor!")
            # Sonsuz döngüye girmemesi için sayacı devasa bir sayıya eşitle
            self.temiz_yol_sayaci = -999999


def main(args=None):
    rclpy.init(args=args)
    node = EngelKacinma()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()