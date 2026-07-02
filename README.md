# ROS2 Servo Bridge for STS3215 Bus Servos

A ROS 2 Humble package for controlling **STS3215 bus servos** using a **Waveshare Bus Servo Adapter**.

The package provides:

- ROS topic-based servo control
- Keyboard teleoperation
- Global speed control
- STServo SDK integration

---

## Requirements

### Software

- Ubuntu 22.04
- ROS 2 Humble
- Python 3

### Hardware

- Waveshare Bus Servo Adapter
- STS3215 Bus Servos
- External Servo Power Supply

---

# Installation

Clone this repository into the **src** folder of your ROS 2 workspace.

```bash
cd ~/your_ros2_workspace/src

git clone https://github.com/razigito/robotic_arm_ros2_control.git
```

Build the package.

```bash
cd ~/your_ros2_workspace

colcon build --packages-select my_arm_servo_bridge
```

Source the workspace.

```bash
source install/setup.bash
```

---

# Hardware Setup

1. Connect the Waveshare Bus Servo Adapter to your PC using USB.
2. Connect the adapter to the STS3215 servo bus.
3. Power the servos using an external power supply.
4. Verify the serial port.

```bash
ls /dev/ttyACM*
```

If your adapter appears on a different port, update:

```
my_arm_servo_bridge/my_arm_servo_bridge/servo_bridge.py
```

```python
DEVICE_NAME = "/dev/ttyACM0"
```

---

# Running

### Terminal 1

Start the servo bridge.

```bash
source ~/your_ros2_workspace/install/setup.bash

ros2 run my_arm_servo_bridge servo_bridge
```

Expected output:

```
Opening serial port...
Servo connection successful!
```

---

### Terminal 2

Start keyboard control.

```bash
source ~/your_ros2_workspace/install/setup.bash

ros2 run my_arm_servo_bridge keyboard_control
```

---

# Keyboard Controls

| Key | Function |
|------|----------|
| **1-6** | Select servo |
| **←** | Move selected servo left |
| **→** | Move selected servo right |
| **+** | Increase global speed |
| **-** | Decrease global speed |
| **s** | Show current speed |
| **q** | Quit |

---

# ROS Topics

## `/servo_command`

**Message Type**

```
std_msgs/Int32MultiArray
```

**Format**

```
[servo_id, target_position]
```

Example:

```bash
ros2 topic pub --once /servo_command \
std_msgs/msg/Int32MultiArray \
"{data: [1,2200]}"
```

---

## `/servo_speed`

**Message Type**

```
std_msgs/Int32
```

Example:

```bash
ros2 topic pub --once /servo_speed \
std_msgs/msg/Int32 \
"{data: 600}"
```

---

# Package Structure

```
my_arm_servo_bridge/
├── my_arm_servo_bridge/
│   ├── __init__.py
│   ├── servo_bridge.py
│   ├── keyboard_control.py
│   └── STservo_sdk/
├── resource/
├── package.xml
├── setup.py
└── setup.cfg
```

---

# Acknowledgements

Special thanks to **[@shehiin](https://github.com/shehiin)** for the hardware support.

---

# License

This project uses the **STServo SDK** for servo communication. Please refer to the SDK's license for its usage and redistribution terms.
