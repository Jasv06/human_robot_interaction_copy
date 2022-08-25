import rospy
import numpy as np
import roslib
import time 
import sys
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from interbotix_xs_modules.gripper import InterbotixGripperXS
from std_msgs.msg import Float32
from geometry_msgs.msg import Point
from std_msgs.msg import Int32 
from human_robot_interaction.msg import *

"""Script with the ability to detect if your hand is upsidedown and if your hand is moving and it will drop object till your hand has stopped moving"""

x = 0.3
y = 0.0
z = 0.3

id_ = 0.0
hands_number = 0.0
hand_status = 2.0

hand_life = 0.0

palm_direction = 0.0

x_rate_of_change = 0.0
y_rate_of_change = 0.0
z_rate_of_change = 0.0

def xyz(data):

   global x
   global y
   global z
   
   x = data.x
   y = data.y
   z = data.z
   

def hand(data):

   global id_
   global hands_number
   global hand_status
   
   id_ = data.handID
   hands_number = data.handnummer
   hand_status = data.handstates
   
   
def Leap_life_of_hand(data): 
   
   global hand_life
   
   hand_life = data.data

def xyz_rate_of_change(data):

   global x_rate_of_change
   global y_rate_of_change
   global z_rate_of_change
   
   x_rate_of_change = data.x
   y_rate_of_change = data.y
   z_rate_of_change = data.z  

def palm_normal_direction(data): 
   
   global palm_direction
   
   palm_direction = data.data
   
   
def main():
   
	bot = InterbotixManipulatorXS("rx150","arm","gripper", gripper_pressure = 0.5)	
	
	rospy.init_node('rx150_robot_manipulation')
   
	print("Ready to control the robot!!")
      
	r = rospy.Rate(100)
   
	counter_uno = 0
   
	counter_dos = 0
	
	emergencia = 0
	
	counter = 0
	
	drop = 0
	
	while not rospy.is_shutdown():
      
		rospy.Subscriber("/hand_life_in_sensor", Float32, Leap_life_of_hand)
		rospy.Subscriber("/Robot_coordinates", Point, xyz)
		rospy.Subscriber("/hand_status", handstatus, hand)
		rospy.Subscriber("/rate_of_change", Point, xyz_rate_of_change)
		rospy.Subscriber("/palm_direction_for_robot", Float32, palm_normal_direction)
                     
		x_robot_control = x
		y_robot_control = y
		z_robot_control = z
      
		identification_id = id_
		number_of_hands = hands_number
		status_of_hands = hand_status
            
		x_rate = x_rate_of_change
		y_rate = y_rate_of_change
		z_rate = z_rate_of_change
      
		palm_pointing = palm_direction
      
		if number_of_hands == 1 and counter_uno == counter_dos and hand_life >= 0.5: 
			
			if counter == 0:
				bot.arm.set_ee_pose_components(x=0.18,z=0.2)
				bot.gripper.open()
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", -np.pi/2.0)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x = 0.15,z=0.02)   
				time.sleep(0.5) 
				bot.arm.set_ee_cartesian_trajectory(x=0.08,z=-0.14)
				bot.gripper.close()
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.08,z=0.14)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", 0)
				time.sleep(0.5)
				emergencia = 1
				counter_dos = 1
				counter = 1
				drop = 0
				RO = bot.arm.get_joint_commands()
				print(RO)
				continue
				
			elif counter == 1:
				bot.arm.set_ee_pose_components(x=0.18,z=0.2)
				bot.gripper.open()
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", -np.pi/3)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x = 0.22,z=0.017) 
				time.sleep(0.5)
				bot.arm.set_single_joint_position("wrist_rotate",position=0.44)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("wrist_angle",position=1.3)
				time.sleep(0.5)
				bot.gripper.close()
				bot.arm.set_single_joint_position("wrist_rotate",position=0)
				bot.arm.set_single_joint_position("wrist_angle",position=0)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.15, z=0.18)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", 0)
				emergencia = 1
				counter_dos = 1
				counter = 2
				drop = 1
				ROB = bot.arm.get_joint_commands()
				print(ROB)
				continue 
				
			elif counter == 2:
				bot.arm.set_ee_pose_components(x=0.18,z=0.2)
				bot.gripper.open()
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", -np.pi/3.25)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x = 0.15,z=0.02)    
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=0.049,z=-0.14)
				bot.gripper.close()
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.049,z=0.14)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", 0)
				time.sleep(0.5)
				emergencia = 1
				counter_dos = 1
				counter = 3
				drop = 2
				ROBO = bot.arm.get_joint_commands()
				print(ROBO)
				continue
				
			elif counter == 3:
				bot.arm.set_ee_pose_components(x=0.18,z=0.2)
				bot.gripper.open()
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", -np.pi/2.5)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x = 0.15,z=0.02)    
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=0.049,z=-0.14)
				bot.gripper.close()
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.049,z=0.14)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", 0)
				time.sleep(0.5)
				emergencia = 1
				counter_dos = 1
				counter = 0
				drop = 3
				ROBOT = bot.arm.get_joint_commands()
				print(ROBOT)
				continue 
			

		"""dont forget to update the line below"""
		robot_position = bot.arm.get_joint_commands()
		
     
		if number_of_hands == 1 and hand_status >= 0.8 and hand_status <= 1 and hand_life >= 5 and emergencia == 1: #or palm_pointing < 0 and emergencia == 1 and hand_life > 5: 
         
			if robot_position[0] <= 0 and robot_position[1] <= -1.7 and robot_position[2] >= 1.5 and robot_position[3] <= 0.9 and robot_position[4] <= 0.05:
				exit()
			
			if drop == 0 and robot_position == [0.0, -0.452328098393586, -0.45814388830579644, 0.9104719866994214, -4.5103991595197685e-17]:			
				bot.arm.set_single_joint_position("waist", -np.pi/2.0)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
				time.sleep(0.5)    
				bot.arm.set_ee_cartesian_trajectory(x=0.08,z=-0.14)
				time.sleep(0.5)
				bot.gripper.open()
				time.sleep(1)
				bot.arm.set_ee_cartesian_trajectory(x=-0.08,z=0.14)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
				time.sleep(1)
				bot.arm.set_single_joint_position("waist", 0)  
				bot.arm.go_to_sleep_pose()        
				counter_dos = 0
				emergencia = 0
				time.sleep(1)
				
			elif drop == 1 and robot_position == [0.0, -0.1431028024781285, -0.9939358192110259, 1.245021987624909, 1.0457262282043245e-16]:
				bot.arm.set_ee_pose_components(x=0.18,z=0.2)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", -np.pi/3)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x = 0.22,z=0.017)
				time.sleep(0.5) 
				bot.arm.set_single_joint_position("wrist_rotate",position=0.44)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("wrist_angle",position=1.3)
				time.sleep(0.5)
				bot.gripper.open()
				bot.arm.set_single_joint_position("wrist_angle",position=0)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("wrist_rotate",position=0)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.15, z=0.18)
				bot.arm.set_single_joint_position("waist", 0)
				bot.arm.go_to_sleep_pose()
				counter_dos = 0
				emergencia = 0
				time.sleep(1)
				
			elif drop == 2 and robot_position == [0.0, -0.45232809839358706, -0.4581438883057943, 0.91047198669942, -2.47275898276998e-17]:
				bot.arm.set_ee_pose_components(x=0.18,z=0.2)
				bot.arm.set_single_joint_position("waist", -np.pi/2.5)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x = 0.15,z=0.02)    
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=0.049,z=-0.14)
				bot.gripper.open()
				bot.arm.set_ee_cartesian_trajectory(x=-0.049,z=0.14)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", 0)
				bot.arm.go_to_sleep_pose()
				counter_dos = 0
				emergencia = 0
				time.sleep(1)
				
			elif drop == 3 and robot_position == [0.0, -0.45232809839358756, -0.45814388830579406, 0.9104719866994205, -1.90717601420712e-17]:
				bot.arm.set_ee_pose_components(x=0.18,z=0.2)
				bot.arm.set_single_joint_position("waist", -np.pi/2.5)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x = 0.15,z=0.02)    
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=0.049,z=-0.14)
				bot.gripper.open()
				bot.arm.set_ee_cartesian_trajectory(x=-0.049,z=0.14)
				time.sleep(0.5)
				bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
				time.sleep(0.5)
				bot.arm.set_single_joint_position("waist", 0)
				bot.arm.go_to_sleep_pose()
				counter_dos = 0 
				emergencia = 0 
				time.sleep(1)
				
			else: 
				continue 				
				
		if number_of_hands == 1 and hand_status < 0.8 and hand_life >= 0.5 and emergencia == 1:#and palm_pointing > 0
 
			bot.arm.set_ee_pose_components(x=x_robot_control,y=y_robot_control, z = (z_robot_control+0.035)) 
 			
			if x_rate < 1.5 and x_rate > -1.5 and y_rate < 1.5 and y_rate > -1.5 and z_rate < 1.5 and z_rate > -1.5 and hand_life > 6:
			
				bot.arm.set_ee_pose_components(x=x_robot_control,y=y_robot_control,z=z_robot_control)       
				bot.gripper.open()
				time.sleep(0.5)				
				bot.arm.set_ee_cartesian_trajectory(x=-0.08, z=0.02)
				bot.arm.set_single_joint_position("waist", 0)  
				bot.arm.go_to_sleep_pose()
				counter_dos = 0
				emergencia = 0
				time.sleep(1)
			else: 
         	
				continue
 
		else: 
			
			continue 
			         
		time.sleep(0.5)             
      

if __name__ == '__main__': 
    main()   
