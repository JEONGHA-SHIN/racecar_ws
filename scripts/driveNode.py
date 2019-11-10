#!/usr/bin/python

#import libraries and color segmentation code
import rospy
import cv2
import time
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from color_segmentation import cd_color_segmentation
from racecar_ws.msg import drive_msg
from sensor_msgs.msg import Joy, Image


RED = np.array([[0, 44, 147], [8, 254, 255]])
YELLOW = np.array([[19, 14, 150], [33, 163, 255]])
BLUE = np.array([[56, 109, 150], [111, 255, 255]])


class driveStop(object):
	"""class that will help the robot drive and stop at certain conditions
	"""
	def __init__(self):
		self.pub = rospy.Publisher('/drive', drive_msg, queue_size = 1)
		self.bridge = CvBridge()		
		self.image_sub = rospy.Subscriber('/camera', Image, self.driveStop_car_callback)

		self.flag_box = ((0,0),(0,0))
		self.flag_center = (0,0)
		self.flag_size = 0

		self.cmd = drive_msg()
		self.cmd.drive_angle = 0
		self.cmd.velocity = 0
	
		self.min_value=0

	def size_calc(self):
		pix_width = self.flag_box[1][0] - self.flag_box[0][0]
		pix_height = self.flag_box[1][1] - self.flag_box[0][1]	

		self.box_size = pix_width*pix_height
		#print(self.flag_box)
	
		    
	def driveStop_car_callback(self,data):
		try:
	       		self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
     		except CvBridgeError as e:
       			print(e)

		while self.cv_image is None:
			time.sleep(0.5)
			print("sleeping")

		self.flag_box = cd_color_segmentation(self.cv_image, show_image=False)
		cv2.imshow("Image window", self.cv_image)
    		cv2.waitKey(3)

		self.size_calc()
		
		if self.box_size > 10000: 
			mid_point = (self.flag_box[1][0] + self.flag_box[0][0])/2
			#print(mid_point)
			self.cmd.drive_angle = -(mid_point - 640) * (0.55)
			if abs(self.cmd.drive_angle) > 255:
				if self.cmd.drive_angle > 0:
					self.cmd.drive_angle = 255
				else:
					self.cmd.drive_angle = -255
			
			self.cmd.velocity = 200
		else:
			self.cmd.drive_angle = 0
			self.cmd.velocity = 0
	
		self.pub.publish(self.cmd)
                


def main():
	ic = driveStop()
	rospy.init_node('driveStop')
	try:
		rospy.spin()
		#ic.pub.publish(ic.cmd)
	except KeyboardInterrupt:
    		print("Shutting down")
  		cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
