#!/usr/bin/env python

import rospy
import os
import sys
import std_msgs
import industrial_msgs.msg
import urx
from pprint import pprint

try:
    rate = 10

    rospy.init_node("robot_status_publisher")

    ip = rospy.get_param("/ur_driver/robot_ip_address")
    print("Try to connect to "+ip)
    robot = urx.Robot(ip)
    pprint(dir(robot))
    pprint(robot)




    pub = rospy.Publisher("robot_status",std_msgs.msg.String, queue_size=10)
    r = rospy.Rate(rate) # 10hz
    while not rospy.is_shutdown():
        status = industrial_msgs.msg.RobotStatus()
        status.mode.val = -1 # Unknown
        status.header = std_msgs.msg.Header(stamp=rospy.Time.now())
        print(status)

        state = robot.secmon.get_all_data()["RobotModeData"]
        print(state)

        if(state["isEmergencyStopped"] or state["isSecurityStopped"]):
            status.in_error.val = 1
            status.error_code = 1 if state["isSecurityStopped"] else 2 # 1 si protective stop, 2 si emergency stop
        else:
            if(state["robotMode"] == 5) or (state["robotMode"] == 3):
                    status.e_stopped.val = 1
                    status.error_code = 3 if state["robotMode"] == 5 else 4 # 3 si idle, 4 si power off


            elif(state["robotMode"] == 7):
                status.drives_powered.val = 1

                if(state["isProgramRunning"]):
                    status.in_motion.val = 1
                else:
                    status.motion_possible.val = 1


        pub.publish(str(status))
        print(".")
        r.sleep()

except Exception as e:
    print(e)
    sys.exit()
