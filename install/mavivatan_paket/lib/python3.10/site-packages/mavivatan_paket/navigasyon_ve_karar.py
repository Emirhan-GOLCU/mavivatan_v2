import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3, Point  # POINT BURAYA EKLENDİ
import sys
import math
from sensor_msgs.msg import NavSatFix


# --- 1. PID SINIFI ---
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, target, current, dt):
        error = target - current
        if error > 180: error -= 360
        if error < -180: error += 360
        p_out = self.kp * error
        self.integral += error * dt
        i_out = self.ki * self.integral
        derivative = (error - self.prev_error) / dt
        d_out = self.kd * derivative
        self.prev_error = error
        return p_out + i_out + d_out


# --- 2. ANA OTONOMİ SINIFI ---
class OtonomNavigasyon(Node):
    def __init__(self):
        super().__init__('otonom_navigasyon_node')

        # Değişkenler
        self.guncel_mod = "BEKLEME"  # Başlangıçta beklemede kalsın
        self.hedef_mesafe_toleransi = 4.5
        self.steering_pid = PIDController(0.4, 0.01, 0.1)
        self.create_subscription(String, 'aktif_mod', self.mod_callback, 10)
        # Kamikaze görevi (GPS) için sanal bir hedef
        self.hedef_enlem = 40.69400
        self.hedef_boylam = 29.50800

        # --- GÖRSEL HEDEF HAFIZASI ---
        self.son_hedef_gorme_zamani = 0.0
        self.hedef_x = 320.0
        self.kutu_genisligi = 0.0
        self.hedef_son_yon = 1.0  # 1.0 sağa, -1.0 sola demek

        # ROS 2 Timer: Saniyede 10 kez (0.1 sn) motorları kontrol eder
        self.motor_kontrol_zamanlayici = self.create_timer(0.1, self.motor_surus_dongusu)

        # Yayıncılar
        self.durum_bildir_pub = self.create_publisher(String, 'gorev_durumu', 10)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Abonelikler
        self.pid_sub = self.create_subscription(Vector3, '/pid_ayarlari', self.pid_callback, 10)
        self.gps_sub = self.create_subscription(NavSatFix, '/mavros/global_position/global', self.hedef_callback, 10)
        self.iha_sub = self.create_subscription(String, '/iha_onayli_hedef', self.iha_hedef_callback, 10)

        # YOLO'dan gelen görsel hedef noktasını dinleyen kanal
        self.kamera_hedef_sub = self.create_subscription(Point, '/hedef_koordinat', self.gorsel_hedef_callback, 10)

    def mod_callback(self, msg):
        self.guncel_mod = msg.data
        # Eğer mod Kamikaze ise terminale bilgi verelim uyanıp uyanmadığını anlayalım
        if "KAMIKAZE" in self.guncel_mod:
            self.get_logger().info(f"🔄 Kamikaze Beyni Uyandı! Mevcut Mod: {self.guncel_mod}")
    def pid_callback(self, msg):
        self.steering_pid.kp = msg.x
        self.steering_pid.ki = msg.y
        self.steering_pid.kd = msg.z
        self.get_logger().info(f"🚀 PID Değerleri Güncellendi: Kp={msg.x}, Ki={msg.y}, Kd={msg.z}")

    def iha_hedef_callback(self, msg):
        try:
            self.aranan_hedef_rengi = msg.data
            self.get_logger().info(f"🎯 İHA İSTİHBARATI ALINDI! Denizde aranacak renk: {self.aranan_hedef_rengi}")
            self.guncel_mod = "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR"

            # --- EKLENEN KISIM: Arama başladığında zamanı sıfırla ki anında "Kaybettim" demesin ---
            self.son_hedef_gorme_zamani = self.get_clock().now().nanoseconds / 1e9
        except Exception as e:
            self.get_logger().error(f"İHA veri ayrıştırma hatası: {e}")

    # GÖRSEL HAFIZA FONKSİYONU (SADECE KAYIT YAPAR, MOTOR SÜRMEZ)
    def gorsel_hedef_callback(self, msg):
        # Hedefi her gördüğümüzde hafızayı güncelliyoruz
        self.hedef_x = msg.x
        self.kutu_genisligi = msg.z

        # ROS 2 saati
        self.son_hedef_gorme_zamani = self.get_clock().now().nanoseconds / 1e9

        # Şamandıra ekranın neresinde kaybolmaya yakın? (Sol: -1, Sağ: 1)
        self.hedef_son_yon = -1.0 if msg.x < 320.0 else 1.0

    # ASIL BEYİN BURASI (MOTORLARI BU DÖNGÜ SÜRER)
    def motor_surus_dongusu(self):
        if self.guncel_mod != "GOREV_3_KAMIKAZE_ARAMA_YAPIYOR":
            return

        cmd = Twist()
        su_an = self.get_clock().now().nanoseconds / 1e9
        gecen_sure = su_an - self.son_hedef_gorme_zamani

        # SENARYO 1: Hedefi Kaybettik! (1 saniyeden uzun süredir görüntü yok)
        if gecen_sure > 1.0:
            if gecen_sure > 1.0:
                # Burası senin dediğin 'hafıza tabanlı manevra' kısmı
                self.get_logger().warn(
                    f"🔍 HEDEF KAYIP! Son bilinen yöne ({'SAĞ' if self.hedef_son_yon > 0 else 'SOL'}) dönülüyor...",
                    throttle_duration_sec=2.0)

                cmd.linear.x = 0.2  # Tamamen durma, çok yavaşça ilerle ki momentum kaybolmasın
                # En son sağda gördüyse sağa, solda gördüyse sola keskin bir dönüş ver
                cmd.angular.z = 0.8 * self.hedef_son_yon

                self.cmd_pub.publish(cmd)
                return
        # SENARYO 2: Hedef Görüş Alanında (PID İle Üzerine Sür)
        kamera_merkez_x = 320.0
        dt = 0.1
        donus_hizi = self.steering_pid.compute(kamera_merkez_x, self.hedef_x, dt)

        # SENARYO 3: Çarpışma Kontrolü (Genişlik 450 pikseli geçtiyse vur)
        # SENARYO 3: Çarpışma Kontrolü ve Dinamik Frenleme
        if self.kutu_genisligi > 450.0:
            self.cmd_pub.publish(Twist())  # Acil fren
            self.get_logger().warn("💥 KAMİKAZE BAŞARILI! (Temas sağlandı)")
            self.guncel_mod = "BEKLEME"

            onay_msg = String()
            onay_msg.data = "GOREV_3_TAMAMLANDI_GORSEL"
            self.durum_bildir_pub.publish(onay_msg)
        else:
            # (Dinamik frenleme matematiklerin burada duruyor)
            if self.kutu_genisligi < 150.0:
                ileri_hiz = 1.5
            else:
                ilerleme_orani = (self.kutu_genisligi - 150.0) / 300.0
                ileri_hiz = 1.5 - (ilerleme_orani * 1.2)
                ileri_hiz = max(0.3, ileri_hiz)

            cmd.linear.x = ileri_hiz
            cmd.angular.z = donus_hizi
            self.cmd_pub.publish(cmd)

            # --- EKLENEN KISIM: Hedefe kilitlendiğinde terminale bilgi bas ---
            self.get_logger().info(
                f"🚀 HEDEFE KİLİTLENİLDİ! Hız: {ileri_hiz:.2f} | Dümen: {donus_hizi:.2f} | Kutu: {self.kutu_genisligi}px",
                throttle_duration_sec=0.5)

    # ESKİ GPS GÖREVİ (Yedek olarak durabilir)
    def hedef_callback(self, msg):
        if self.guncel_mod != "GOREV_3_KAMIKAZE":
            return

        enlem_farki = (self.hedef_enlem - msg.latitude) * 111000
        boylam_farki = (self.hedef_boylam - msg.longitude) * 111000
        ileri_uzaklik = math.sqrt(enlem_farki ** 2 + boylam_farki ** 2)

        self.get_logger().info(f"Hedefe kalan mesafe: {ileri_uzaklik:.2f} metre")

        if ileri_uzaklik > self.hedef_mesafe_toleransi:
            pass  # PID ile hedefe dönme komutları buraya gelecek
        else:
            cmd = Twist()
            self.cmd_pub.publish(cmd)  # Motorları durdur
            onay_msg = String()
            onay_msg.data = "GOREV_3_TAMAMLANDI"
            self.durum_bildir_pub.publish(onay_msg)
            self.get_logger().warn("💥 HEDEF BÖLGESİNE GİRİLDİ (Tolerans İçi)! Görev Tamamlandı.")
            self.guncel_mod = "BEKLEME"


def main(args=None):
    rclpy.init(args=args)
    node = OtonomNavigasyon()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()