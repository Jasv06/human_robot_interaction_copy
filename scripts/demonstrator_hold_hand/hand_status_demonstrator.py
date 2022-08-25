import rospy
import numpy as np
import roslib
import time 
import sys
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 
from human_robot_interaction.msg import *

hand_id = 0.0

hand_open_or_close = 0.0

number_of_hands = 0.0

def Hands_ID(data):
   
   global hand_id
   
   hand_id = data.data

def Hand_number(data):
   
   global number_of_hands
   
   number_of_hands = data.data
   
def hand_OPEN_or_CLOSE(data):

   global hand_open_or_close
   
   hand_open_or_close = data.data
   
def main():
   
   rospy.init_node('Hand_data')
   
   pub = rospy.Publisher('hand_status', handstatus, queue_size = 1)
   
   r = rospy.Rate(10)
   
   print("Hand node initialized!")
     
   while not rospy.is_shutdown():
     
     msg = handstatus()
     
     rospy.Subscriber("HandNumber", Float32, Hand_number)
     rospy.Subscriber("hand_id", Float32, Hands_ID)
     rospy.Subscriber("hand_state", Float32, hand_OPEN_or_CLOSE)
     
     msg.handnummer = number_of_hands
     msg.handID = hand_id
     msg.handstates = hand_open_or_close
     
     #print(msg)
     
     pub.publish(msg)
     r.sleep()
   
if __name__ == '__main__':
     main()

