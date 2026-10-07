"""仅用于本项目仿真：定时发布速度，结束时连续发送零速度。"""
import argparse
import time
import rclpy
from geometry_msgs.msg import Twist

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--linear',type=float,default=0)
parser.add_argument('--angular',type=float,default=.3)
parser.add_argument('--seconds',type=float,default=10)
args = parser.parse_args()
if abs(args.linear)>.35 or abs(args.angular)>1 or not 0<args.seconds<=60:
    parser.error('速度超出示例范围，或时长不在 (0, 60] 秒内')
rclpy.init()
node = rclpy.create_node('research_drive')
publisher = node.create_publisher(Twist,'/cmd_vel',10)
try:
    start = time.monotonic()
    while publisher.get_subscription_count()==0 and time.monotonic()-start<5:
        rclpy.spin_once(node,timeout_sec=.1)
    if publisher.get_subscription_count()==0:
        raise RuntimeError('没有速度订阅者；先运行 sim.sh')
    command = Twist()
    command.linear.x,command.angular.z = args.linear,args.angular
    end = time.monotonic()+args.seconds
    while rclpy.ok() and time.monotonic()<end:
        publisher.publish(command)
        rclpy.spin_once(node,timeout_sec=.05)
except KeyboardInterrupt:
    pass
finally:
    if rclpy.ok():
        for _ in range(10):
            publisher.publish(Twist())
            rclpy.spin_once(node,timeout_sec=.05)
    node.destroy_node()
    if rclpy.ok(): rclpy.shutdown()
