#!/usr/bin/python
# license removed for brevity

import rospy
import time

from racecar_ws.msg import drive_msg
from sensor_msgs.msg import LaserScan

mux_mode = ''



def scan_callback(msg):
	print(round(msg.ranges[0],1),round(msg.ranges[180],1),round(msg.ranges[360],1))#,round(msg.ranges[540],1))


#init ROS
rospy.init_node('scan_test')
rospy.Subscriber('/scan', LaserScan, scan_callback)


rospy.spin()
