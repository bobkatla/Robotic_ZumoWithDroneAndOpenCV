#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time
import sys, signal

def signal_handler(signal, frame):
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)
    
rospy.init_node('zumo_move_forward', anonymous = True)
pub = rospy.Publisher('/zumo/1/cmd_vel', Twist, queue_size = 10)

def move_forward():
    vel_msg=Twist()
    
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x=0
    vel_msg.angular.y=0
    vel_msg.angular.z=0
    
    vel_msg.linear.x=1
    pub.publish(vel_msg)

while True:
    move_forward()
    time.sleep(1)