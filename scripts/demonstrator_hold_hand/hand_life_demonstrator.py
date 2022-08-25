import rospy
import numpy as np
import roslib
import time 
import sys
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32

hand_life = 0.0

def Leap_life_of_hand(data): 
   
   global hand_life
   
   hand_life = data.data
   
def main():
   
   rospy.init_node('Hand_life')
   
   pub = rospy.Publisher('hand_life_in_sensor', Float32, queue_size = 1)
   
   r = rospy.Rate(10)
   
   print("Hand life node initialized!")
     
   while not rospy.is_shutdown():
    
     rospy.Subscriber("life_of_hand", Float32, Leap_life_of_hand)
     
     life_of_hand = hand_life
     
     pub.publish(life_of_hand)
     r.sleep()
   
if __name__ == '__main__':
     main()
