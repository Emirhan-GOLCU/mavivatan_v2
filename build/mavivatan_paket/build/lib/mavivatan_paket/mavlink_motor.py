import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pymavlink import mavutil

class MavlinkMotor(Node):
    def __init__(self):
        super().__init__('mavlink_motor_node')

        # Pixhawk / Orange Cube bağlantısı
        self.bağlantı_portu = '/dev/ttyACM0'
        self.baud_rate = 115200

        # --- YUMUŞATMA (RAMPING) DEĞİŞKENLERİ ---
        self.guncel_sol_pwm = 1500.0
        self.guncel_sag_pwm = 1500.0
        self.yumusatma_katsayisi = 0.15  # 1.0 = Anında tepki, 0.1 = Çok yumuşak geçiş

        try:
            self.master = mavutil.mavlink_connection(self.bağlantı_portu, baud=self.baud_rate)
            self.master.wait_heartbeat(timeout=3.0)
            self.get_logger().info("✅ Orange Cube ile MAVLink bağlantısı KURULDU!")
        except Exception as e:
            self.get_logger().warn(f"⚠️ Orange Cube bulunamadı. Simülasyon modunda devam ediliyor: {e}")
            self.master = None

        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)

    def cmd_vel_callback(self, msg):
        # 1. Twist mesajından değerleri al
        ileri = msg.linear.x
        donus = msg.angular.z

        sol_hiz_orani = ileri - donus
        sag_hiz_orani = ileri + donus

        # 2. HEDEF PWM HESAPLAMA
        hedef_sol_pwm = 1500.0 + (sol_hiz_orani * 400.0)
        hedef_sag_pwm = 1500.0 + (sag_hiz_orani * 400.0)

        # 3. ATALET VE FREN KONTROLÜ (Low-Pass Filter)
        self.guncel_sol_pwm += self.yumusatma_katsayisi * (hedef_sol_pwm - self.guncel_sol_pwm)
        self.guncel_sag_pwm += self.yumusatma_katsayisi * (hedef_sag_pwm - self.guncel_sag_pwm)

        # 4. GÜVENLİK KİLİDİ (1100 - 1900 arası sınırlandırma)
        sol_pwm_gonderilecek = int(max(1100, min(1900, self.guncel_sol_pwm)))
        sag_pwm_gonderilecek = int(max(1100, min(1900, self.guncel_sag_pwm)))

        self.get_logger().info(f"Yumuşatılmış Çıktı -> İskele: {sol_pwm_gonderilecek} | Sancak: {sag_pwm_gonderilecek}")

        # 5. ORANGE CUBE'A GÖNDERME (Sol: Kanal 1, Sağ: Kanal 3)
        if self.master:
            self.master.mav.rc_channels_override_send(
                self.master.target_system,
                self.master.target_component,
                sol_pwm_gonderilecek, 0, sag_pwm_gonderilecek, 0, 0, 0, 0, 0
            )

def main(args=None):
    rclpy.init(args=args)
    node = MavlinkMotor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Sistem kapanırken motorları güvenlice durdur
        if getattr(node, 'master', None):
            node.get_logger().warn("🛑 Sistem kapanıyor, motorlar durduruluyor!")
            node.master.mav.rc_channels_override_send(
                node.master.target_system, node.master.target_component,
                1500, 0, 1500, 0, 0, 0, 0, 0)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()