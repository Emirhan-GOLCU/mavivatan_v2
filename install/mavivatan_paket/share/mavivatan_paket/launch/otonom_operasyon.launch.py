import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


def generate_launch_description():
    pkg_name = 'mavivatan_paket'

    # twist_mux config dosyasının sistemdeki dinamik yolunu buluyoruz
    twist_mux_config = os.path.join(
        get_package_share_directory(pkg_name),
        'config',
        'twist_mux_topics.yaml'
    )

    return LaunchDescription([
        # 1. DONANIM VE HABERLEŞME
        Node(package=pkg_name, executable='telemetri_merkezi', name='telemetri_merkezi_node', output='screen'),
        Node(package=pkg_name, executable='mavlink_motor', name='mavlink_motor_node', output='screen'),

        # 2. GÖREV YÖNETİCİSİ (ANA BEYİN)
        Node(package=pkg_name, executable='gorev_yoneticisi', name='gorev_yoneticisi_node', output='screen'),

        # 3. OTONOMİ ALGORİTMALARI
        Node(package=pkg_name, executable='kanal_navigasyonu', name='kanal_navigasyonu_node', output='screen'),
        Node(package=pkg_name, executable='gps_navigasyon', name='gps_navigasyon_node', output='screen'),
        Node(package=pkg_name, executable='navigasyon_ve_karar', name='navigasyon_ve_karar_node', output='screen'),

        # Eğer aktif kullanıyorsan sensör füzyonunu da açabilirsin:
        # Node(package=pkg_name, executable='sensor_fuzyonu', name='sensor_fuzyonu_node', output='screen'),

        # 4. HAKEM (TWIST MUX) - YAML DOSYASIYLA BİRLİKTE!
        Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux',
            parameters=[twist_mux_config],
            remappings=[('/cmd_vel_out', '/cmd_vel')],
            output='screen'
        ),

        # 5. GÖRSEL ZEKA (YOLO)
        # (TNA.engine dosyasını rahat bulması için Python betiği olarak tetikledik)
        ExecuteProcess(
            cmd=['python3', 'yolo_hedef2_tespiti.py'],
            cwd='/home/baris/mavivatan_ws',  # Komutun çalıştırılacağı dizin
            output='screen'
        )
    ])