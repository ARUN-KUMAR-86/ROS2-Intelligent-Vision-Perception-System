from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='ros_camera_vision',
            executable='camera_node'
        ),

        Node(
            package='ros_camera_vision',
            executable='vision_node'
        ),

    ])