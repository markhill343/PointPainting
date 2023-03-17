import os
import cv2
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import time

class ImagePublisherNode(Node):
    def __init__(self, image_dir, publish_rate):
        super().__init__('image_publisher')
        self.publisher = self.create_publisher(Image, 'image', 10)
        self.bridge = CvBridge()
        self.image_dir = image_dir
        self.publish_rate = publish_rate
        self.timer = self.create_timer(1.0 / self.publish_rate, self.publish_image)

    def publish_image(self):
        for file in os.listdir(self.image_dir):
            file_path = os.path.join(self.image_dir, file)
            if os.path.isfile(file_path) and (file.lower().endswith('.jpg') or file.lower().endswith('.png')):
                img = cv2.imread(file_path, cv2.IMREAD_COLOR)
                if img is not None:
                    msg = self.bridge.cv2_to_imgmsg(img, encoding="bgr8")
                    self.publisher.publish(msg)
                    time.sleep(1.0 / self.publish_rate)

def main(args=None):
    rclpy.init(args=args)
    image_dir = "<your_image_directory>"
    publish_rate = 1.0  # In Hz
    node = ImagePublisherNode(image_dir, publish_rate)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
