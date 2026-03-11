# 🚀 ROS2 Intelligent Vision Perception System

A real-time robotics vision pipeline developed using **ROS2, OpenCV and YOLOv8** for intelligent perception tasks.

This project demonstrates a **multi-stage computer vision architecture** capable of performing classical image processing and deep learning-based object detection simultaneously.

---

## 📌 Project Overview

The system captures live video from a camera, processes frames through multiple vision modules, and publishes processed outputs on separate ROS topics for visualization and integration with robotic systems.

This architecture can be extended for:

- Autonomous navigation
- Object tracking robots
- Surveillance robotics
- Warehouse automation
- Human-robot interaction systems

---

## 🔥 Features

✅ Live camera streaming using ROS2  
✅ Histogram colour analysis  
✅ Image denoising pipeline  
✅ Edge detection module  
✅ Face detection using Haar Cascade  
✅ Deep learning object detection using YOLOv8  
✅ Multi-topic ROS2 communication architecture  
✅ Real-time FPS performance monitoring  

---

## 🧠 Vision Processing Pipeline


Published Topics:

- `/camera/image_raw`
- `/vision/histogram`
- `/vision/denoise`
- `/vision/edges`
- `/vision/tracking`
- `/vision/yolo`

---

## ⚙️ System Requirements

- Ubuntu 24.04
- ROS2 Jazzy
- Python 3.12
- OpenCV
- cv_bridge
- Ultralytics YOLOv8
- NumPy 1.26

---

## 📦 Installation

### Clone Repository

```bash
cd ~/ros2_ws/src
git clone https://github.com/ARUN-KUMAR-86/ROS2-Intelligent-Vision-Perception-System.git

Build Workspace

cd ~/ros2_ws
colcon build
source install/setup.bash

Run Project

ros2 launch ros_camera_vision vision_launch.py

👁️ Visualize Output

rqt → Plugins → Visualization → Image View