import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('research_talker')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.count = 0
        self.timer = self.create_timer(.5, self.tick)

    def tick(self):
        message = String()
        message.data = f'实验样本 {self.count}'
        self.publisher.publish(message)
        self.get_logger().info(message.data)
        self.count += 1


class Listener(Node):
    def __init__(self):
        super().__init__('research_listener')
        self.subscription = self.create_subscription(String, 'chatter', self.receive, 10)

    def receive(self, message):
        self.get_logger().info('收到：'+message.data)


def run(node_class):
    rclpy.init()
    node = node_class()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


def talker():
    run(Talker)


def listener():
    run(Listener)
