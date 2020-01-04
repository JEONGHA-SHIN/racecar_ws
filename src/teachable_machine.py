#!/usr/bin/env python3
#!/usr/bin/env python2

import tensorflow.keras
import cv2

import numpy as np
import rospy
#from cv_bridge import CvBridge, CvBridgeError
from cv_bridge.boost.cv_bridge_boost import getCvType
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray

np.set_printoptions(suppress=True)

model = tensorflow.keras.models.load_model('/home/racecar/catkin_ws/src/racecar_ws/src/keras_model.h5')

data = np.ndarray(shape=(1, 224, 224, 3), dtype = np.float32)

print("????")

def ML_callback(msg):
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
        print(e)

    while cv_image is None:
        time.sleep(0.5)
        print('sleeping')

    image_array = cv2.resize(cm_image, (224, 224), interpolation = cv2.INTER_AREA)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)
    print(prediction)
    ML_pub.publish(prediction)

#init ROS
rospy.init_node('teachable_machine')

ML_pub = rospy.Publisher('/teachable_machine', Float32MultiArray, queue_size=1)
rospy.Subscriber('/camera', Image, ML_callback)

rospy.spin()
