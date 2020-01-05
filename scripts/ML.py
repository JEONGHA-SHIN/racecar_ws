#!/usr/bin/env python

import numpy as np
import sys, math, random, copy
import rospy, copy, time
from sensor_msgs.msg import LaserScan
from racecar_ws.msg import drive_msg
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32MultiArray


def ML_callback(TM):
    print(TM)


rospy.init_node('cmd_vel_mux')
rospy.Subscriber('/teachable_machine', TM, ML_callback)
print("drive_node is now working!!")

rospy.spin()
