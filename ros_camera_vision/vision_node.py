import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np
import time
import os

from ultralytics import YOLO
from ament_index_python.packages import get_package_share_directory


class VisionNode(Node):

    def __init__(self):
        super().__init__('vision_node')

        self.bridge = CvBridge()

        self.create_subscription(
            Image,
            '/camera/image_raw',
            self.process_frame,
            10)

        # Publishers
        self.hist_pub = self.create_publisher(Image, '/vision/histogram', 1)
        self.denoise_pub = self.create_publisher(Image, '/vision/denoise', 1)
        self.edge_pub = self.create_publisher(Image, '/vision/edges', 1)
        self.track_pub = self.create_publisher(Image, '/vision/tracking', 1)
        self.yolo_pub = self.create_publisher(Image, '/vision/yolo', 1)

        # -------- Load Face Cascade (ROS way) --------
        pkg_path = get_package_share_directory('ros_camera_vision')

        cascade_path = os.path.join(
            pkg_path,
            'models',
            'haarcascade_frontalface_default.xml'
        )

        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            self.get_logger().error("Face cascade NOT loaded")
        else:
            self.get_logger().info("Face cascade loaded")

        # -------- Load YOLO Model --------
        self.yolo_model = YOLO("yolov8n.pt")

        # FPS
        self.prev_time = time.time()

        self.get_logger().info("Vision Node with FULL Features Started")


    def process_frame(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        frame = cv2.resize(frame, (640, 480))

        # -------- Histogram --------
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])

        hist_img = np.zeros((300, 256, 3), dtype=np.uint8)

        cv2.normalize(hist, hist, 0, 300, cv2.NORM_MINMAX)

        for x, y in enumerate(hist):
            cv2.line(hist_img, (x, 300), (x, 300 - int(y)), (255, 0, 0))

        # -------- Denoise --------
        denoise = cv2.GaussianBlur(frame, (5, 5), 0)

        # -------- Edge Detection --------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        # -------- Face Detection --------
        tracking = frame.copy()

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(
                tracking,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                3
            )

        # -------- YOLO Detection --------
        yolo_frame = frame.copy()

        results = self.yolo_model(yolo_frame, verbose=False)

        for r in results:
            boxes = r.boxes

            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])

                    label = self.yolo_model.names[cls]

                    cv2.rectangle(
                        yolo_frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 255),
                        2
                    )

                    cv2.putText(
                        yolo_frame,
                        f"{label} {conf:.2f}",
                        (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2
                    )

        # -------- FPS --------
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time

        cv2.putText(
            tracking,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # -------- Publish --------
        self.hist_pub.publish(
            self.bridge.cv2_to_imgmsg(hist_img, 'bgr8'))

        self.denoise_pub.publish(
            self.bridge.cv2_to_imgmsg(denoise, 'bgr8'))

        self.edge_pub.publish(
            self.bridge.cv2_to_imgmsg(edges, 'mono8'))

        self.track_pub.publish(
            self.bridge.cv2_to_imgmsg(tracking, 'bgr8'))

        self.yolo_pub.publish(
            self.bridge.cv2_to_imgmsg(yolo_frame, 'bgr8'))


def main():
    rclpy.init()
    node = VisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()