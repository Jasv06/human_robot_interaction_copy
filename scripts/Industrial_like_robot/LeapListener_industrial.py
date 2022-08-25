import rospy
import numpy as np
import roslib
import time 
import sys
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 

from human_robot_interaction.msg import *

x_coordi_sensor_stable = 0.0
y_coordi_sensor_stable = 0.0
z_coordi_sensor_stable = 0.0

x_coordi_sensor = 0.0
y_coordi_sensor = 0.0
z_coordi_sensor = 0.0

def LeapXYZ_stable(data): 
   
   global x_coordi_sensor_stable 
   global y_coordi_sensor_stable 
   global z_coordi_sensor_stable

   x_coordi_sensor_stable = data.x
   y_coordi_sensor_stable = data.y
   z_coordi_sensor_stable = data.z  

def LeapXYZ_normal(data):

   global x_coordi_sensor 
   global y_coordi_sensor 
   global z_coordi_sensor

   x_coordi_sensor = data.x
   y_coordi_sensor = data.y
   z_coordi_sensor = data.z
   
def main():
   
   rospy.init_node('XYZ_robot_coordinates')
   
   pub = rospy.Publisher('Robot_coordinates', Point, queue_size = 1)
   
   r = rospy.Rate(10)
   
   print("XYZ_robot_coordinates node initialized!")
     
   while not rospy.is_shutdown():
      
     coordenadas = Point()
       
     #rospy.Subscriber("/Leap/XYZ", Point, LeapXYZ_normal)
     #rospy.Subscriber("/LeapHandAngles", Point)
     rospy.Subscriber("/hand_position_stable", Point, LeapXYZ_stable)
 
     #x_rob_normal = z_coordi_sensor 
     #y_rob_normal = x_coordi_sensor
     #z_rob_normal = y_coordi_sensor
      
     x_rob_stable = z_coordi_sensor_stable + 0.3 
     y_rob_stable = x_coordi_sensor_stable
     z_rob_stable = y_coordi_sensor_stable 
      
     if z_rob_stable == 0:
         z_rob_stable = z_rob_stable + 0.3
      
     if z_rob_stable <= 0.2:
         z_rob_stable = z_rob_stable + 0.06
             
     if z_rob_stable > 0.2:
         z_rob_stable = z_rob_stable + 0.03
     
     coordenadas.x = x_rob_stable
     coordenadas.y = y_rob_stable
     coordenadas.z = z_rob_stable
     #print(coordenadas)
     pub.publish(coordenadas)
     r.sleep()
   
if __name__ == '__main__':
     main()

 
