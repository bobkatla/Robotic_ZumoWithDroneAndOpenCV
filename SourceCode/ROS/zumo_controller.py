#!/usr/bin/env python
import rospy
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist

rospy.init_node('zumo_controller', anonymous=True)
pub = rospy.Publisher('/zumo/cmd_vel', Twist, queue_size=10)

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
    if key == keyboard.Key.up: 
        print("Up") 
        vel_msg.linear.x = 1 
        pub.publish(vel_msg)
    if key == keyboard.Key.down: 
        print("Down") 
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
    if key == keyboard.Key.esc: 
        return False

# Collect events until released 
with keyboard.Listener(
    on_release=on_release) as listener: 
        listener.join()
listener.start()