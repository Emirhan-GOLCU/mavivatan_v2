import rclpy
from rclpy.node import Node

# KENDİ MESAJ TİPİMİZİ İÇERİ AKTARIYORUZ!
from mavivatan_interfaces.msg import IdaDurum


class MaviVatanYayinici(Node):
    def __init__(self):
        super().__init__('mavivatan_yayinici_node')

        # Artık 'String' değil, kendi yazdığımız 'IdaDurum' tipini kullanıyoruz
        self.publisher_ = self.create_publisher(IdaDurum, 'operasyon_durumu', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        # Yeni mesaj objemizi oluşturuyoruz
        msg = IdaDurum()

        # İçini sayısal ve metinsel verilerle dolduruyoruz
        msg.hiz = 15.5
        msg.batarya = 89.2
        msg.mod = 'Otonom Seyir'

        self.publisher_.publish(msg)

        # Terminale yazdırma kısmı
        self.get_logger().info(f'Yayınlanan -> Hız: {msg.hiz} knot, Batarya: %{msg.batarya}, Mod: {msg.mod}')


def main(args=None):
    rclpy.init(args=args)
    yayinici = MaviVatanYayinici()

    try:
        rclpy.spin(yayinici)
    except KeyboardInterrupt:
        pass

    yayinici.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()