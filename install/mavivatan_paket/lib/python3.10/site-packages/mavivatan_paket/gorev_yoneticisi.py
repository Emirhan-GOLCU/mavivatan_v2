import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json


class GorevYoneticisi(Node):
    def __init__(self):
        super().__init__('gorev_yoneticisi_node')
        self.guncel_mod = "IHA_BEKLENIYOR"

        # Diğer düğümlere şu an hangi görevde olduğumuzu fırlatacağımız kanal
        self.aktif_mod_pub = self.create_publisher(String, 'aktif_mod', 10)

        # Durum güncellemelerini ve YKİ komutlarını dinliyoruz
        self.create_subscription(String, 'gorev_durumu', self.durum_callback, 10)
        self.create_subscription(String, '/yki_komut', self.yki_callback, 10)

        self.get_logger().info("Görev Yöneticisi Başlatıldı. Mod: IHA_BEKLENIYOR")

    def durum_callback(self, msg):
        durum = msg.data

        # GÖREV 1 BİTTİ -> GÖREV 2 BAŞLAR
        if durum == "GOREV_1_TAMAMLANDI":
            self.guncel_mod = "GOREV_2_ENGEL_KACIS"
            self.get_logger().warn("🚀 GÖREV 1 BİTTİ -> KANAL GEÇİŞİ BAŞLATILIYOR (G2)")

        # GÖREV 2 BİTTİ -> GÖREV 3 İNTİKAL BAŞLAR
        elif durum == "GOREV_2_TAMAMLANDI":
            self.guncel_mod = "GOREV_3_GPS_INTIKAL"
            self.get_logger().warn("🚀 GÖREV 2 BİTTİ -> KAMİKAZE BÖLGESİNE GİDİLİYOR")

        # GÖREV 3 İNTİKAL BİTTİ -> GÖRSEL ARAMA BAŞLAR
        elif durum == "GOREV_3_INTIKAL_TAMAMLANDI":
            self.guncel_mod = "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR"
            self.get_logger().warn("🚀 HEDEF BÖLGESİNE VARILDI -> GÖRSEL KAMİKAZE AKTİF (G3)")

        self.yayinla()  # Yeni modu tüm ağa duyur
    def yki_callback(self, msg):
        try:
            paket = json.loads(msg.data)
            komut = paket.get("command", "")

            # YKİ'den başlatma komutu gelirse
            if komut == "GOREV_BUTCESI_BASLAT" or komut == "GOREV_1_NOKTA_TAKIP":
                self.guncel_mod = "GOREV_1_NOKTA_TAKIP"
                self.get_logger().info("🔄 OPERASYON ADIMI DEĞİŞTİ -> GOREV_1_NOKTA_TAKIP")

            # YKİ'den Kill Switch (Acil Durdurma) gelirse
            elif komut == "ACIL_DURDURMA":
                self.guncel_mod = "ACIL_DURDURMA"
                self.get_logger().warn("🛑 ACIL DURDURMA ALINDI! MOTORLAR KAPATILIYOR.")

            self.yayinla()
        except Exception as e:
            self.get_logger().error(f"Komut okuma hatası: {e}")

    def yayinla(self):
        msg = String()
        msg.data = self.guncel_mod
        self.aktif_mod_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GorevYoneticisi()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()