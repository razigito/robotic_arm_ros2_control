import sys
import tty
import termios

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, Int32


STEP_SIZE = 100
SPEED_STEP = 100


class KeyboardControl(Node):

    def __init__(self):
        super().__init__("keyboard_control")

        self.publisher = self.create_publisher(
            Int32MultiArray,
            "/servo_command",
            10
        )

        self.speed_pub = self.create_publisher(
            Int32,
            "/servo_speed",
            10
        )

        self.selected_id = 1
        self.speed = 600

        self.current_positions = {
            1: 2048,
            2: 2048,
            3: 2048,
            4: 2048,
            5: 2048,
            6: 2048,
        }

        self.get_logger().info("Keyboard servo control started")
        self.print_help()

    def print_help(self):
        print("\n--- ROS SERVO KEYBOARD CONTROL ---")
        print(" [1-6]  : Select Servo ID")
        print(" [<-]   : Decrease position")
        print(" [->]   : Increase position")
        print(" [+]    : Increase global speed")
        print(" [-]    : Decrease global speed")
        print(" [s]    : Show current speed")
        print(" [q]    : Quit")
        print("----------------------------------")
        print(f"Active Servo: {self.selected_id}")
        print(f"Global Speed: {self.speed}")

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

            if ch == "\x1b":
                ch = sys.stdin.read(2)
                if ch == "[C":
                    return "RIGHT"
                if ch == "[D":
                    return "LEFT"
                return "ESC"

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch

    def publish_command(self, servo_id, position):
        msg = Int32MultiArray()
        msg.data = [servo_id, position]
        self.publisher.publish(msg)

        self.get_logger().info(
            f"Servo {servo_id} -> {position}"
        )

    def publish_speed(self):
        msg = Int32()
        msg.data = self.speed
        self.speed_pub.publish(msg)

        self.get_logger().info(
            f"Global Speed -> {self.speed}"
        )

    def run_keyboard_loop(self):
        while rclpy.ok():
            key = self.get_key()

            if key == "q" or key == "\x03":
                print("\nExiting keyboard control...")
                break

            elif key in ["1", "2", "3", "4", "5", "6"]:
                self.selected_id = int(key)
                print(
                    f"\rActive Servo: {self.selected_id} | "
                    f"Position: {self.current_positions[self.selected_id]} | "
                    f"Speed: {self.speed}     ",
                    end=""
                )

            elif key == "RIGHT":
                pos = self.current_positions[self.selected_id] + STEP_SIZE

                if pos > 4095:
                    pos = 4095

                self.current_positions[self.selected_id] = pos
                self.publish_command(self.selected_id, pos)

            elif key == "LEFT":
                pos = self.current_positions[self.selected_id] - STEP_SIZE

                if pos < 0:
                    pos = 0

                self.current_positions[self.selected_id] = pos
                self.publish_command(self.selected_id, pos)

            elif key == "+":
                self.speed += SPEED_STEP

                if self.speed > 1500:
                    self.speed = 1500

                self.publish_speed()
                print(f"\nGlobal Speed: {self.speed}")

            elif key == "-":
                self.speed -= SPEED_STEP

                if self.speed < 100:
                    self.speed = 100

                self.publish_speed()
                print(f"\nGlobal Speed: {self.speed}")

            elif key == "s":
                print(f"\nCurrent Global Speed: {self.speed}")


def main(args=None):
    rclpy.init(args=args)

    node = KeyboardControl()

    try:
        node.run_keyboard_loop()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
