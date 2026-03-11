⭐ ROS2 Intelligent Vision Perception System

Real-time robotics vision pipeline built using ROS2 + OpenCV + YOLOv8.

🔥 Features

Live Camera Streaming using ROS2

Histogram Colour Analysis

Image Denoising Pipeline

Edge Detection Module

Face Detection System

YOLOv8 Object Detection

Multi-topic ROS Vision Architecture

Real-time FPS Monitoring

📡 Published Topics

/camera/image_raw

/vision/histogram

/vision/denoise

/vision/edges

/vision/tracking

/vision/yolo

⚙️ Run Instructions

cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 launch ros_camera_vision vision_launch.py

👁️ View Outputs

Use:

rqt → Plugins → Visualization → Image View