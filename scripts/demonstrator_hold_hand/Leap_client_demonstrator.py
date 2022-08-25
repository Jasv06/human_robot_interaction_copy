import socket
import sys,thread ,time
import pickle
import time 
import struct

#The path can be changed based on the directory or folder were the leap motion files are located
sys.path.insert(0,"/home/irobot/catkin_ws/src/human_robot_interaction/LeapMotion")

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
 
AddressPort = ("127.0.0.1", 57410)

UDPSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

class LeapMotionListener(Leap.Listener):
    ctr = 0.5
    finger_names = ['thumb','Index','Middle','Ring','Pinky']
    bone_names = ['Metacarpal','Proximal','Intermediate','Distal']
    state_names = ['INVALID_STATE','STATE_START','STATE_UPDATE','STATE_END']
    
    def on_init(self,controller):
       print "Initialized"
    
    def on_connect(self,controller):
       print "Motion Sensor Connected!"
       
       #Enable gestures 
       controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
       controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
       controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
       controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
       
    def on_disconnect(self,controller):
        print "Motion sensor disconnected!"

    def on_exit(self,controller):
        print "Exited"

    def on_frame(self,controller):
        
        frame = controller.frame() 

        handnummer  = len(frame.hands)
        
        if handnummer < 1:
           #print("No hand in frame so the data being sent has default values!!!")
           LeapMotionListener.ctr = 4
           strength = 2
           hand_identifier = 0
           pitch = 0
           yaw = 0
           roll = 0
           filtered_hand = [0,0,0]
           hand_speed  = [0,0,0]
           life_time_of_hand = 0
           bytes = [0,strength,hand_identifier,filtered_hand[0],filtered_hand[1],filtered_hand[2],life_time_of_hand,1]
           info = struct.pack('<8f', *bytes)
           UDPSocket.sendto(info ,AddressPort)
           
        self.id = LeapMotionListener.ctr
        

        
        if handnummer > 0:
            print "Hands: %d" % (handnummer)
                     
        for hand in frame.hands:
            handType = " Left Hand " if hand.is_left else " Right Hand "
            print handType + "Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)
            
            life_time_of_hand = hand.time_visible
            print("life time of hand in sensor: %f" % life_time_of_hand)
            print("mano abierta o cerrada: %f" % hand.grab_strength)
            strength = hand.grab_strength
            hand_identifier = hand.id
            pitch = hand.direction.pitch
            yaw = hand.direction.yaw
            roll = hand.palm_normal.roll
            filtered_hand = hand.stabilized_palm_position
            hand_speed  = hand.palm_velocity
                        
            bytes = [len(frame.hands),strength,hand_identifier,filtered_hand[0],filtered_hand[1],filtered_hand[2],life_time_of_hand,1]
            
            if handnummer == 1 and life_time_of_hand >= self.id and life_time_of_hand < (self.id + 0.02):
            #if handnummer == 1 and life_time_of_hand >= 4 and life_time_of_hand < 4 + 0.01:
               LeapMotionListener.ctr += 0.5
               
               info = struct.pack('<8f', *bytes)
          
               UDPSocket.sendto(info ,AddressPort)
             
            
  
         
    
def main():

   listener = LeapMotionListener()
   controller = Leap.Controller()
   
   controller.add_listener(listener)
   
   print "Press enter to quit..."
   try:
     sys.stdin.readline()
   except KeyboardInterrupt:
     pass   
   finally:
     controller.remove_listener(listener)
     
if __name__ == "__main__":
  main()   

