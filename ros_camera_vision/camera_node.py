import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):

    def __init__(self):
        super().__init__('camera_node')

        self.publisher = self.create_publisher(Image,'/camera/image_raw',1)

        self.bridge = CvBridge()

        self.cap = cv2.VideoCapture(0)

        self.timer = self.create_timer(0.03,self.capture_frame)

    def capture_frame(self):

        ret, frame = self.cap.read()

        if not ret:
            self.get_logger().warn("Camera not detected")
            return

        frame = cv2.resize(frame,(640,480))

        msg = self.bridge.cv2_to_imgmsg(frame,'bgr8')
        self.publisher.publish(msg)


def main():
    rclpy.init()
    node = CameraNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()