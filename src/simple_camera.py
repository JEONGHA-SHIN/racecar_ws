#!/usr/bin/python

import rospy
from sensor_msgs.msg import Image

import cv2
import numpy as np

cap = cv2.VideoCapture(2)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

rospy.init_node('camera')
pub_im = rospy.Publisher('/camera', Image, queue_size=1)

while not rospy.is_shutdown():

    _, frame = cap.read()

    if frame is None:
        continue

    msg = Image()
    msg.height = frame.shape[0]
    msg.width = frame.shape[1]
    msg.encoding = 'bgr8'
    msg.is_bigendian = 0
    msg.step = 3 * msg.width
    msg.data = frame.flatten().tostring()

    pub_im.publish(msg)

cap.release()

