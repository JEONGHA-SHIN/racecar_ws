#!/usr/bin/env python

import numpy as np
import sys, math, random, copy
import rospy, copy, time
from sensor_msgs.msg import LaserScan
from racecar_ws.msg import drive_msg
from sensor_msgs.msg import Joy

rospy.Subscriber('/teachable_machine', TM, ML_callback)

def ML_callback(TM):
    print(TM)
