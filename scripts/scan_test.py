#!/usr/bin/python
# license removed for brevity

import rospy
import time

from racecar_ws.msg import drive_msg
from sensor_msgs.msg import LaserScan

mux_mode = ''



def scan_callback(msg):
	print(msg.ranges[540])


#init ROS
rospy.init_node('scan_test')
rospy.Subscriber('/scan', LaserScan, scan_callback)


rospy.spin()
