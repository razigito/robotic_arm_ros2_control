import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, Int32

from .STservo_sdk import *

DEVICE_NAME = "/dev/ttyACM0"
BAUDRATE = 1000000
ACCELERATION = 50


class ServoBridge(Node):

    def __init__(self):
        super().__init__("servo_bridge")

        self.speed = 600

        self.portHandler = PortHandler(DEVICE_NAME)
        self.packetHandler = sts(self.portHandler)

        self.get_logger().info("Opening serial port...")

        if not self.portHandler.openPort():
            self.get_logger().error("Failed to open port")
            return

        if not self.portHandler.setBaudRate(BAUDRATE):
            self.get_logger().error("Failed to set baudrate")
            return

        self.get_logger().info("Servo connection successful!")

        self.subscription = self.create_subscription(
            Int32MultiArray,
            "/servo_command",
            self.servo_command_callback,
            10
        )

        self.speed_subscription = self.create_subscription(
            Int32,
            "/servo_speed",
            self.speed_callback,
            10
        )

        self.get_logger().info("Listening on /servo_command")
        self.get_logger().info("Listening on /servo_speed")
        self.get_logger().info("Send servo command: [servo_id, position]")
        self.get_logger().info(f"Initial Global Speed = {self.speed}")

    def speed_callback(self, msg):
        self.speed = int(msg.data)

        if self.speed < 100:
            self.speed = 100

        if self.speed > 1500:
            self.speed = 1500

        self.get_logger().info(f"Global Speed = {self.speed}")

    def servo_command_callback(self, msg):
        if len(msg.data) != 2:
            self.get_logger().error("Command must be: [servo_id, position]")
            return

        servo_id = int(msg.data[0])
        target_position = int(msg.data[1])

        if servo_id < 1 or servo_id > 6:
            self.get_logger().error("Servo ID must be between 1 and 6")
            return

        if target_position < 0:
            target_position = 0

        if target_position > 4095:
            target_position = 4095

        self.get_logger().info(
            f"Moving Servo {servo_id} to position {target_position} at speed {self.speed}"
        )

        self.packetHandler.WritePosEx(
            servo_id,
            target_position,
            self.speed,
            ACCELERATION
        )


def main(args=None):
    rclpy.init(args=args)

    node = ServoBridge()

    rclpy.spin(node)

    node.portHandler.closePort()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
