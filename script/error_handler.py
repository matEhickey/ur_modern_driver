#!/usr/bin/env python

import rospy
import os
import sys
import std_msgs
import industrial_msgs.msg
from pprint import pprint
import socket
import time


nodeName = "error_handler"

HOST = '10.0.0.124'    # The remote host
PORT = 29999              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))



rospy.init_node(nodeName)

def preventMotion(data):
    print("-- prevent motion")
    s.sendall('power off\n')


def allowMotion(data):
    print("-- allow motion")
    s.sendall('power on\n')
    time.sleep(0.5)
    s.sendall('brake release\n')


def restart(data):
    print("-- restart")
    s.sendall('power off\n')
    time.sleep(0.5)
    s.sendall('power on\n')


def dismissProtection(data):
    print("-- dismiss protection")
    s.sendall('unlock protective stop\n')

rospy.Subscriber("/"+nodeName+"/preventMotion",std_msgs.msg.String,preventMotion)
rospy.Subscriber("/"+nodeName+"/allowMotion",std_msgs.msg.String,allowMotion)
rospy.Subscriber("/"+nodeName+"/restart",std_msgs.msg.String,restart)
rospy.Subscriber("/"+nodeName+"/dismissProtection",std_msgs.msg.String,dismissProtection)


rospy.spin()
