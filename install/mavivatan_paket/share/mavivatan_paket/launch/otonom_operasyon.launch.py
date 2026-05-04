from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # 1. GÖREV YÖNETİCİSİ (Beyin)
        Node(package='mavivatan_paket', executable='gorev_yoneticisi', name='beyin'),

        # 2. YOLO HEDEF TESPİTİ (Gözler - TensorRT)
        Node(package='mavivatan_paket', executable='yolo_hedef_tespiti', name='yolo'),

        # 3. SENSÖR FÜZYONU (Derinlik Hesabı)
        Node(package='mavivatan_paket', executable='sensor_fuzyonu', name='fuzyon'),

        # 4. GPS NAVİGASYON (Rota Takibi)
        Node(package='mavivatan_paket', executable='gps_navigasyon', name='gps_pilot'),

        # 5. NAVİGASYON VE KARAR (Kamikaze Mantığı)
        Node(package='mavivatan_paket', executable='navigasyon_karar', name='kamikaze_pilot'),

        # 6. MAVLINK MOTOR (Aktüatör - Orange Cube)
        Node(package='mavivatan_paket', executable='mavlink_motor', name='motor_kontrol'),

        # 7. TELEMETRİ MERKEZİ (RF Haberleşme)
        Node(package='mavivatan_paket', executable='telemetri_merkezi', name='rf_link'),

        # 8. YER KONTROL ARAYÜZÜ (Görselleştirme)
        Node(package='mavivatan_paket', executable='mavivatan_yars_ui', name='ui'),
    ])