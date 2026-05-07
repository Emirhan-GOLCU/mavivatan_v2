from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # 1. RPLIDAR S3 Düğümü
        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='rplidar_s3',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',  # Lidar'ın bağlı olduğu port
                'serial_baudrate': 256000,  # S3 için yüksek baudrate
                'frame_id': 'laser_link',
                'inverted': False,
                'angle_compensate': True,
                # Kendi gövdemizi görmemek için açı kısıtlaması (Örn: Sadece ön 270 derece)
                'angle_min': -135.0,
                'angle_max': 135.0
            }]
        ),

        # 2. ZED 2i Stereo Kamera Düğümü
        Node(
            package='zed_wrapper',
            executable='zed_wrapper',
            name='zed2i_kamera',
            output='screen',
            parameters=[{
                'camera_model': 'zed2i',
                'publish_tf': True,  # TF (Transform) ağacını yayınla
                'publish_map_tf': False,
                'general.grab_resolution': 1,  # 720p HD (Performans için)
                'general.grab_frame_rate': 30,  # Saniyede 30 kare
                'depth.depth_mode': 1,  # PERFORMANCE modu (AGX Orin'i yormamak için)
            }]
        )
    ])