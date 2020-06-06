#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist

import sys, signal

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

rospy.init_node('tello_controller', anonymous=True)
pub = rospy.Publisher('/drone/cmd_vel', Twist, queue_size=10)
pub2 = rospy.Publisher('/drone/user_control', UInt8, queue_size=10)

from pynput import keyboard
import getpass

def on_release(key):
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    pub2.publish(1)
    if key == keyboard.Key.up:
        print("Forward")
        vel_msg.linear.x = 1
        pub.publish(vel_msg)
    if key == keyboard.Key.down:
        print("Backward")
        vel_msg.linear.x = -1
        pub.publish(vel_msg)
    if key == keyboard.Key.left:
        print("Left")
        vel_msg.linear.y = 1
        pub.publish(vel_msg)
    if key == keyboard.Key.right:
        vel_msg.linear.y = -1
        pub.publish(vel_msg)
        print("Right")
    if key == keyboard.Key.f1:
        vel_msg.linear.z = 1
        pub.publish(vel_msg)
        print("Up")
    if key == keyboard.Key.f2:
        vel_msg.linear.z = -1
        pub.publish(vel_msg)
        print("Down")
    if key == keyboard.Key.enter:
        vel_msg.linear.x = 9
        pub.publish(vel_msg)
        print("Fly on")
    if key == keyboard.Key.backspace:
        vel_msg.linear.x = -9
        pub.publish(vel_msg)
        print("Land off")
    if key == keyboard.Key.esc:
        pub2.publish(0)
        return False
        
# Collect events until released
with keyboard.Listener(
        on_release=on_release) as listener:
           listener.join()
listener.start()
