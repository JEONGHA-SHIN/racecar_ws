#!/usr/bin/python

#import libraries and color segmentation code
import rospy
import cv2
import time
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from color_segmentation import cd_color_segmentation
from racecar1.msg import drive_msgs
from sensor_msgs.msg import Joy, Image

class driveStop(object):
	"""class that will help the robot drive and stop at certain conditions
	"""
	def __init__(self):
		"""initalize the node"""
<<<<<<< HEAD
		rospy.init_node("driveNode)
		self.pub = rospy.Publisher(DRIVE_TOPIC, AckermannDriveStamped, queue_size = 1)
		rospy.Subscriber("/camera", img, self.driveStop_car_callback)
=======
		self.pub = rospy.Publisher('/drive', drive_msgs, queue_size = 1)
		self.bridge = CvBridge()		
		self.image_sub = rospy.Subscriber('/camera', Image, self.driveStop_car_callback)
>>>>>>> 60260008417f76c96b2d8fcb97fc4989742d3356

		""" initialize the box dimensions"""
		self.flag_box = ((0,0),(0,0))
		self.flag_center = (0,0)
		self.flag_size = 0

                """driving stuff"""
		self.cmd = drive_msgs()
		self.cmd.direction = "Stop"
		self.cmd.velocity = 0
	
		"""get the camera data from the class Zed_converter in Zed"""
		
		self.min_value=0

	def size_calc(self):
		""" calculate the x and y size of the box in pixels"""
		pix_width = self.flag_box[1][0] - self.flag_box[0][0]
		pix_height = self.flag_box[1][1] - self.flag_box[0][1]	

		self.box_size = pix_width*pix_height
		#print(self.box_size)
	
	def drive(self):
            self.cmd.direction = "Forward"
	    self.cmd.velocity = 255
	    
	def stop(self):
            self.cmd.direction = "Stop"
	    self.cmd.velocity = 0
	    
	def driveStop_car_callback(self,data):
		try:
	       		self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
     		except CvBridgeError as e:
       			print(e)

		#checks if the image is valid first
		while self.cv_image is None:
			time.sleep(0.5)
			print("sleeping")

		#applies the current filter to the image and stores the image in imagePush
		self.flag_box = cd_color_segmentation(self.cv_image, show_image=False)
		#cv2.imshow("Image window", self.cv_image)
    		#cv2.waitKey(3)

		#finds the size of the box
		self.size_calc()
<<<<<<< HEAD
		
		
         self.drive()
	
	def drive(self):
            self.cmd.drive.speed = 1
            self.cmd.drive.steering_angle = 1
=======
		if self.box_size < 200000:
			self.drive()
			print("go Front")
		else: 
			self.stop()
			print("Stop")
		self.pub.publish(self.cmd)
                
>>>>>>> 60260008417f76c96b2d8fcb97fc4989742d3356


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
