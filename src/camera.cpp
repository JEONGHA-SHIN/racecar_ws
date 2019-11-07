#include <ros/ros.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <jetson-utils/gstCamera.h>
#include "image_converter.h"



// globals	
gstCamera* camera = NULL;

imageConverter* camera_cvt = NULL;
ros::Publisher* camera_pub = NULL;


// aquire and publish camera frame
bool aquireFrame()
{
	float* imgRGBA = NULL;

	// get the latest frame
	if( !camera->CaptureRGBA(&imgRGBA, 1000) )
	{
		ROS_ERROR("failed to capture camera frame");
		return false;
	}

	// assure correct image size
	if( !camera_cvt->Resize(camera->GetWidth(), camera->GetHeight()) )
	{
		ROS_ERROR("failed to resize camera image converter");
		return false;
	}

	// populate the message
	sensor_msgs::Image msg;

	if( !camera_cvt->Convert(msg, sensor_msgs::image_encodings::BGR8, imgRGBA) )
	{
		ROS_ERROR("failed to convert camera frame to sensor_msgs::Image");
		return false;
	}

	// publish the message
	camera_pub->publish(msg);
	ROS_INFO("published camera frame");
	return true;
}


// node main loop
int main(int argc, char **argv)
{
	ros::init(argc, argv, "camera");
 
	ros::NodeHandle nh;
	ros::NodeHandle private_nh("~");

	/*
	 * retrieve parameters
	 */
	std::string camera_device = "0";	// MIPI CSI camera by default

	private_nh.param<std::string>("device", camera_device, camera_device);
	
	ROS_INFO("opening camera device %s", camera_device.c_str());

	
	/*
	 * open camera device
	 */
	camera = gstCamera::Create(camera_device.c_str());

	if( !camera )
	{
		ROS_ERROR("failed to open camera device %s", camera_device.c_str());
		return 0;
	}


	/*
	 * create image converter
	 */
	camera_cvt = new imageConverter();

	if( !camera_cvt )
	{
		ROS_ERROR("failed to create imageConverter");
		return 0;
	}


	/*
	 * advertise publisher topics
	 */
	ros::Publisher camera_publisher = private_nh.advertise<sensor_msgs::Image>("/camera", 2);
	camera_pub = &camera_publisher;


	/*
	 * start the camera streaming
	 */
	if( !camera->Open() )
	{
		ROS_ERROR("failed to start camera streaming");
		return 0;
	}


	/*
	 * start publishing video frames
	 */
	while( ros::ok() )
	{
		//if( raw_pub->getNumSubscribers() > 0 )
			aquireFrame();

		ros::spinOnce();
	}

	delete camera;
	return 0;
}
