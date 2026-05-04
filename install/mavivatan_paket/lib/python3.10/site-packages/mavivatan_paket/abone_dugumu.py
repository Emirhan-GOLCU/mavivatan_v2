import rclpy
from rclpy.node import Node

# KENDİ MESAJ TİPİMİZİ İÇERİ AKTARIYORUZ
from mavivatan_interfaces.msg import IdaDurum


class MaviVatanAbone(Node):
    def __init__(self):
        super().__init__('mavivatan_abone_node')

        # Artık 'String' değil, kendi yazdığımız 'IdaDurum' tipini dinliyoruz
        self.subscription = self.create_subscription(
            IdaDurum,
            'operasyon_durumu',
            self.listener_callback,
            10)
        self.subscription  # Uyarıyı engellemek için

    def listener_callback(self, msg):
        # Gelen sayısal verileri kullanarak karar mekanizması kuruyoruz
        if msg.batarya < 20.0:
            batarya_durumu = "⚠️ KRİTİK SEVİYE: EVE DÖNÜŞ BAŞLATILMALI!"
        else:
            batarya_durumu = "✅ Güç Normal."

        # Terminale yazdırma kısmı
        self.get_logger().info(f'Merkeze Ulaşan Veri | Hız: {msg.hiz} knot | {batarya_durumu}')


def main(args=None):
    rclpy.init(args=args)
    abone = MaviVatanAbone()

    try:
        rclpy.spin(abone)
    except KeyboardInterrupt:
        pass

    abone.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()