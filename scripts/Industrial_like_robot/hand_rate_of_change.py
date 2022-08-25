import rospy
import numpy as np
import roslib
import time 
import sys
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 

from human_robot_interaction.msg import *

x_rate_of_change = 0.0
y_rate_of_change = 0.0
z_rate_of_change = 0.0

def LeapXYZ_stable(data): 
   
	global x_rate_of_change 
	global y_rate_of_change 
	global z_rate_of_change
	
	x_rate_of_change = data.x
	y_rate_of_change = data.y
	z_rate_of_change = data.z

def main():

	rospy.init_node('rate_of_change_for_robot')   
	
	pub = rospy.Publisher('rate_of_change',Point, queue_size = 1)
	
	r = rospy.Rate(10)
	
	print("Rate of change from the hand node initialized!!")
	
	while not rospy.is_shutdown():
	
		rate = Point()
		
		rospy.Subscriber("hand_rate_of_change",Point, LeapXYZ_stable)
		
		rate.x = x_rate_of_change
		rate.y = y_rate_of_change
		rate.z = z_rate_of_change
		
		pub.publish(rate)
		
		r.sleep()
 
if __name__ == '__main__':
     main()

