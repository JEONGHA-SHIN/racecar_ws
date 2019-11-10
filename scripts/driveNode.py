#!/usr/bin/env python

import numpy as np
import sys, math, random, copy
import rospy, copy, time
from sensor_msgs.msg import LaserScan
from racecar_ws.msg import drive_msg
from sensor_msgs.msg import Joy

AUTONOMOUS_MODE=False
count = 0

class PotentialField:
	def __init__(self):
		rospy.init_node("potentialField")
		self.data = None
		self.cmd = drive_msg()
		self.laser_sub = rospy.Subscriber("/scan", LaserScan, self.scan_callback) 
		#self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
		self.drive_pub = rospy.Publisher("/drive", drive_msg, queue_size=1)
		
		self.cmd.velocity = 255
		self.cmd.drive_angle = 0
		
		#cartesian points -- to be filled (tuples)
		self.cartPoints = [None for x in range(720)]
		
		#[speed, angle]
		self.finalVector = [0.5, 0]
		self.maxTurn = 1

	#def joy_callback(self, msg):
	#	global AUTONOMOUS_MODE

	#	if msg.buttons[5] == 1:
	#		AUTONOMOUS_MODE = True #LB >> joy
	#		self.drive_pub.publish(self.cmd)
	#	else:
	#		AUTONOMOUS_MODE = False
		
	
	def scan_callback(self, data):
		'''Checks LIDAR data'''
		self.data = data.ranges
		self.convertPoints(self.data)
		self.drive_callback()
		self.drive_pub.publish(self.cmd)

	def drive_callback(self):
		'''Publishes drive commands'''
		self.calcFinalVector(self.cartPoints)
		self.cmd.velocity = self.finalVector[1]
		self.cmd.drive_angle = self.finalVector[0]*255

	def convertPoints(self, points):
		'''Convert all current LIDAR data to cartesian coordinates'''
		for i in range(len(points)):
			x = points[i] * round(math.sin(math.radians(i/2)),5)
			y = points[i] * round(math.cos(math.radians(i/2)),5)*-1
			self.cartPoints[i] = (x,y)
			

	def calcFinalVector(self, points):
		'''Calculate the final driving speed and angle'''
		#a total force[x,y] from current data that will be added to the current velocity
		force = [0, 0]
		constant = 0.0001
		
		#checks if the data has been initialized
		if self.data:
			for pt in points:
				x, y = pt
				if x==0:
					x=constant
				if y==0:
					y=constant
				#adjusts the magnitude of the point's vector to increase the lower values (1/raw_magnitdue^2)
				mag = 0.1 #constant / (x**2 + y**2)**3
				force[0] += -x * mag #x dir
				force[1] += -y * mag #y dir

			#force[0] += 0.3
			#adjusts the sign depending if it will move backwards or forwards
			speedSign = 1 if (force[1] + self.finalVector[1]) > 0 else -1
			#pythagorean theorem to find magnitude
			self.finalVector[1] += math.sqrt((force[0]**2 + force[1]**2)) * speedSign
			#arctan to find angle (atan2 returns radians)
			self.finalVector[0] += math.atan2(force[0], force[1])
			
			if abs(self.finalVector[0]) > self.maxTurn:
				if self.finalVector[0] > 0:
					self.finalVector[0] = self.maxTurn
				else:
					self.finalVector[0] = -self.maxTurn

if __name__ == "__main__":
	try:
		node = PotentialField()
		rospy.spin()		
		#while not rospy.is_shutdown():
			#if AUTONOMOUS_MODE:
		#	if self.joy_sub.buttons[5]==1
		#		node.drive_pub.publish(node.cmd)
		#		count+=1
		#		print(AUTONOMOUS_MODE)
	except rospy.ROSInterruptException:
		exit()
