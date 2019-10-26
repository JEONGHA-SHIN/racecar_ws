#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image

import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError



def gstreamer_pipeline(
    	capture_width=1280,
    	capture_height=720,
    	display_width=1280,
    	display_height=720,
    	framerate=60,
    	flip_method=0,
):
    	return (
        	"nvarguscamerasrc ! "
        	"video/x-raw(memory:NVMM), "
        	"width=(int)%d, height=(int)%d, "
        	"format=(string)NV12, framerate=(fraction)%d/1 ! "
        	"nvvidconv flip-method=%d ! "
        	"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        	"videoconvert ! "
        	"video/x-raw, format=(string)BGR ! appsink"
        	% (
       	    		capture_width,
            		capture_height,
            		framerate,
            		flip_method,
            		display_width,
            		display_height,
        	)
    )


def show_camera():
    	rospy.init_node('camera')
    	pub_im = rospy.Publisher('/camera', Image, queue_size=1)
    	# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
	#print(gstreamer_pipeline(flip_method=0))
	cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
	#if cap.isOpened():
        #window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
	while not rospy.is_shutdown():
	    	ret_val, img = cap.read()
	    	#cv2.imshow("CSI Camera", img)
		msg = Image()
		msg.height = 720
		msg.width = 1280
	        msg.encoding = 'bgr8'
		msg.is_bigendian = 0
		msg.step = 3 * 1280
	 	msg.data = img.flatten().tostring()
		pub_im.publish(msg)
	        # This also acts as
	        keyCode = cv2.waitKey(30) & 0xFF
	        # Stop the program on the ESC key
	        if keyCode == 27:
	        	break
	cap.release()
        #cv2.destroyAllWindows()
    #else:
        #print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
   

