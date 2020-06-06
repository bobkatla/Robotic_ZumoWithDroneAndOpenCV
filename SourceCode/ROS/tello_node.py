#!/usr/bin/python
import socket
import threading
import time
from time import sleep

import rospy
from std_msgs.msg import Int16
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import sys, signal

def signal_handler(signal, frame):
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

pubBa = rospy.Publisher('/tello/battery', String, queue_size = 10)

class Tello:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_adderss = (self.tello_ip, self.tello_port)
        self.MAX_TIME_OUT = 15.0

    def send_command(self, command):
        self.socket.sendto(command.encode('utf-8'), self.tello_adderss)
        print 'sending command: %s to %s' % (command, self.tello_ip)

        start = time.time()
        now = time.time()
        diff = now - start
        if diff > self.MAX_TIME_OUT:
            print 'Max timeout exceeded... command %s' % command
            return
        print 'Done!!! sent command: %s to %s' % (command, self.tello_ip)

    def _receive_thread(self):
        #Listen to responses from the Tello.
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))
            except socket.error, exc:
                print "Caught exception socket.error : %s" % exc

tello = Tello()
tello.send_command("command")
#tello.send_command("takeoff")
rospy.init_node('tello_node', anonymous=True)

def callback_move(cmd_msg):
    rospy.loginfo(rospy.get_caller_id() + 'I heard a command')
    x = cmd_msg.linear.x
    print(x)
    y = cmd_msg.linear.y
    print(y)
    z = cmd_msg.linear.z
    print(z)
    if(x == 1.0): #forward 20cm
        tello.send_command("forward 20")
    if(x == -1.0): #backward 20cm
        tello.send_command("back 20")
    if(y == 1.0): #left 10deg
        tello.send_command("ccw 20")
    if(y == -1.0): #right 10deg
        tello.send_command("cw 20")
    if(z == 1.0): #up 20cm
        tello.send_command("up 20")
    if(z == -1.0): #down 20cm
        tello.send_command("down 20")
    if(x == 9.0): #fly
        tello.send_command("takeoff")
    if(x == -9.0): #land
        tello.send_command("land")
#pub = rospy.Subscriber('/drone/cmd_vel', Twist, callback_move)

while True:
    #new topic of tello that can be drone or zumo
    pub = rospy.Subscriber('/tello/cmd_vel', Twist, callback_move)
    sleep(1)
    
    tello.send_command("battery?")
    result = tello.response[:-2]
    pubBa.publish(result)
    sleep(3)