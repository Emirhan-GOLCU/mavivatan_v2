import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import json

class TelemetriMerkezi(Node):
    def __init__(self):
        super().__init__('telemetri_merkezi_node')

        # Port ayarını donanıma göre değiştirmeyi unutma (ttyUSB0, ttyUSB1 vb.)
        self.rf_port = '/dev/ttyUSB1'
        self.baud = 57600

        try:
            # timeout=0.1 önemli; veri yokken kodu kilitlemez
            self.seri = serial.Serial(self.rf_port, self.baud, timeout=0.1)
            self.get_logger().info(f"📡 RFD900x Bağlantısı {self.rf_port} üzerinden Başarılı.")
        except Exception as e:
            self.get_logger().error(f"❌ RF Bağlantı Hatası: {e}")
            self.seri = None

        # Yayımcılar (Publishers)
        self.renk_pub = self.create_publisher(String, 'iha_hedef_rengi', 10)
        self.komut_pub = self.create_publisher(String, 'yki_komut', 10)

        # Seri portu saniyede 20 kez kontrol et (0.05 saniye aralık)
        self.create_timer(0.05, self.dinle_ve_coz)

    def dinle_ve_coz(self):
        # Seri portun açık olduğundan ve veri beklediğinden emin ol
        if self.seri is not None and self.seri.in_waiting > 0:
            try:
                # Satırı oku, decode et ve boşlukları temizle
                raw_data = self.seri.readline().decode('utf-8').strip()

                # Boş satır gelirse işlem yapma
                if not raw_data:
                    return

                # JSON Çözümleme
                paket = json.loads(raw_data)

                # 1. Renk Kontrolü
                if "target_color" in paket:
                    renk_msg = String()
                    renk_msg.data = str(paket["target_color"])
                    self.renk_pub.publish(renk_msg)
                    self.get_logger().info(f"🚁 İHA'dan Gelen Renk: {renk_msg.data}")

                # 2. Görev Komutu Kontrolü
                if "command" in paket:
                    komut_msg = String()
                    komut_msg.data = str(paket["command"])
                    self.komut_pub.publish(komut_msg)
                    self.get_logger().info(f"📥 YKİ'den Gelen Komut: {komut_msg.data}")

            except json.JSONDecodeError:
                # RF sinyali zayıfsa bazen veri yarım gelir, bu hata sistemi çökertmez
                self.get_logger().warn("⚠️ Hatalı JSON paketi alındı (Veri bozulmuş olabilir).")
            except Exception as e:
                self.get_logger().error(f"Telemetri Çözümleme Hatası: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = TelemetriMerkezi()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.seri:
            node.seri.close() # Portu temizce kapat
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()