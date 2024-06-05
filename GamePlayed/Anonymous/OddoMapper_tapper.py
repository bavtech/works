import random
import string
import subprocess
from time import sleep
from PIL import ImageGrab,Image
import cv2
import numpy as np
import pyautogui
from pynput import keyboard
import sys

# Get the arguments passed to the script
arguments = sys.argv

# The first argument is always the script name
script_name = arguments[0]


# SCREEN_CAPTURE = (1440,0,1925,946)

# THRESHOLD = ( 1450,660, 1920,901)
# THRESHOLD = ( 2135,550, 2615,800)

clicked = dict(A=False, B=False,C=False, D=False)
counter =0

A,B,C,D = 0,0,0,0
def reset():
    global clicked    
    clicked = {key: False for key in clicked}
    
# rcut = 20
# lcut = 30 
# vcut= 55
# y = 730
# Ax = 2250
# Bx = 2300
# Cx = 2400
# Dx = 2500

# lower_black = np.array([0, 0, 0],dtype=np.uint8)
# upper_black = np.array([64, 64, 64], dtype=np.uint8)

lower_bound = np.array([40, 50, 50],dtype=np.uint8)  
upper_bound = np.array([80, 255, 255], dtype=np.uint8)  

clicker = False

running = True
onyourMark= False
samp ='3'
def on_press(key):
    global onyourMark
    try:
        if key == keyboard.Key.space:
            # print('Space bar press')
            onyourMark =  not onyourMark
            if onyourMark:
                print("Taking keyboard inputs")
            else:
                print(" Keyboard Input Paused")
    
#        
    except AttributeError:
        # Handle special keys here if needed
        pass
def on_release(key):
    global running
    if key== keyboard.Key.esc:
         
#             # print("Key 'q' pressed, exiting loop.")
            print("Exiting Keyboard press")
            running = False
            return False 
#         # Stop the listener

# def on_press(key):
#     try:
#         if key == keyboard.Key.space:
#             print('Space bar pressed')
#     except AttributeError:
#         print(f"Special key {key} pressed")
def center(contour):
    M = cv2.moments(contour)

# Calculate centroid
    try:
        
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        return cx,cy
    except ZeroDivisionError  as e:
        pass
    

def getCordinate(window)  :
    
    try:
        # Get the list of windows with wmctrl
        output = subprocess.check_output(['wmctrl', '-lG']).decode('utf-8')
        # Search for the Chrome window
        for line in output.splitlines():
            if window.lower() in line.lower():
                parts = line.split()
                # Extract position and size
                x, y, width, height = map(int, parts[2:6])
                return  (x, y, x + width, y + height-20)
        # print("No Chrome window found")
        return None, None
    except subprocess.CalledProcessError as e:
        print(f"Error calling wmctrl: {e}")
        return None, None
     
# SCREEN_CAPTURE =  getCordinate('samsung')
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

letters = list(string.ascii_lowercase[:18])

# List of numbers from '0' to '9'
numbers = list(string.digits)
combined_list = letters + numbers

hamster = [ 'f11', 'f10', 'f6', 'f7', 'f8', 'f9','s', 't', 'u', 'v', 'w', 'x', 'y', 'z']




def select_random_characters(combined_list, num_chars=8):
    return random.sample(combined_list, num_chars) 

def tappingwhat():
    global combined_list, onyourMark
    if len(arguments)>1:
        
        if 'ham' in arguments[1]:
            combined_list =  hamster
 
    try:
          
        while running:
            # print(1)
            if onyourMark:
                # print("i am in")
                randint =  random.randint(1,len(combined_list))
                val = select_random_characters(combined_list, randint)
                
                for i in val:
                    if i=='q':
                        pass
                    else:
                            
                        pyautogui.press(i)
    except KeyboardInterrupt:
        listener.stop()
        listener.join()
        
        print("loop Ended")
        
if __name__ == "__main__":
    print("keyboard input running")
    
    tappingwhat()
