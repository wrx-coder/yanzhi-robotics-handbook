"""两个终端分别运行 python3 ros2_pubsub.py 和 python3 ros2_pubsub.py --listen。"""
import argparse
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class ExperimentNode(Node):
    def __init__(self, listen):
        super().__init__('experiment_listener' if listen else 'experiment_publisher')
        if listen:
            self.subscription = self.create_subscription(Float64, 'experiment_signal', self.receive, 10)
        else:
            self.publisher = self.create_publisher(Float64, 'experiment_signal', 10)
            self.samples = 0
            self.timer = self.create_timer(0.5, self.publish)

    def publish(self):
        message = Float64()
        message.data = math.sin(self.samples * 0.1)
        self.samples += 1
        self.publisher.publish(message)
        self.get_logger().info(f'发送：{message.data:.4f}')

    def receive(self, message):
        self.get_logger().info(f'接收：{message.data:.4f}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--listen', action='store_true')
    args, ros_args = parser.parse_known_args()
    rclpy.init(args=ros_args)
    node = ExperimentNode(args.listen)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
