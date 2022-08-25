import rospy
import numpy as np
import roslib
import time 
import sys
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 

from human_robot_interaction.msg import *

palm_direction = 0.0

def palm_direction_sensor(data):
	
	global palm_direction
	
	palm_direction = data.data 

def main():
	
	rospy.init_node('palm_direction')
	
	pub = rospy.Publisher('palm_direction_for_robot', Float32, queue_size = 1)
	
	r = rospy.Rate(10)
	
	print("Direction of palm node initialized!!")
	
	while not rospy.is_shutdown():
	
		rospy.Subscriber("hand_normal", Float32, palm_direction_sensor)
		
		direction_of_palm = palm_direction
		
		pub.publish(direction_of_palm)
		r.sleep()
		
if __name__ == '__main__':
	main()
