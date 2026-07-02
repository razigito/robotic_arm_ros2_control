from setuptools import find_packages, setup

package_name = 'my_arm_servo_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ub',
    maintainer_email='ub@example.com',
    description='ROS 2 bridge for STS servo robotic arm',
    license='TODO',
    entry_points={
        'console_scripts': [
            'servo_bridge = my_arm_servo_bridge.servo_bridge:main',
            'keyboard_control = my_arm_servo_bridge.keyboard_control:main',
        ],
    },
)




