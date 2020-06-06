#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16
from std_msgs.msg import UInt8
import os
import time

rospy.init_node('control_tello', anonymous = True)
pub = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=10)
current_topic = 0
new_topic = 1
    
def handle_tello(msg):
    global current_topic
    
    if (msg.data == 1):
        new_topic = 2
    else:
        new_topic = 1
        
    #only change topics if we need to.
    if (current_topic == 1 and new_topic == 2):
        os.system("rosrun topic_tools mux_select mux_tello_cmdvel /drone/cmd_vel")
        current_topic = 2
    if (current_topic == 2 and new_topic == 1):
        os.system("rosrun topic_tools mux_select mux_tello_cmdvel /zumo/cmd_vel")
        current_topic = 1

rospy.Subscriber('/drone/user_control', UInt8, handle_tello)
os.system("rosrun topic_tools mux_select mux_tello_cmdvel /zumo/cmd_vel")
current_topic = 1
rospy.spin()