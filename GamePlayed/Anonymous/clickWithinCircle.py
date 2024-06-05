import subprocess
from time import sleep
import cv2 
from pynput import keyboard
import random
import math
import pyautogui
import sys


arguments = sys.argv
def on_press(key):
    global onyourMark, onlyClick
    try:
        if key == keyboard.Key.space:
            
            # print('Space bar press')
            onyourMark =  not onyourMark
            
            if onyourMark:
                print("Taking Mouse inputs")
            else:
                print("Mouse input Paused")
        if key.char == '+':
            # print('Plus key pressed')
            onlyClick= not onlyClick
    
#        
    except AttributeError:
        # Handle special keys here if needed
        pass
    
def on_release(key):
    global running
    if key== keyboard.Key.esc:
        
        running = False
        print("Exiting mouse click")
        return False 
#         # Stop the list

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

def random_point_in_circle(radius, name):
    """
    Generate a random point within a circle.
    """
    coord =  getCordinate(name)
    
    center_x= (coord[2] - coord[0])  //2 +  coord[0]
    center_y= (coord[3] - coord[1] )//2 + coord[1]
    
    angle = random.uniform(0, 2 * math.pi)
    r = radius * math.sqrt(random.uniform(0, 1))
    x = int(center_x + r * math.cos(angle))
    y = int(center_y + r * math.sin(angle))
    return x, y
     
# SCREEN_CAPTURE =  getCordinate('samsung')
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
running = True 
onyourMark=False
onlyClick = False
print("mouse Clicking running")
perClick=1

try:
    
    perClick = int(arguments[1])
    
except Exception as e:
    print("Wrong Value supplied can only be int")
    perClick=1
    
try:
    
    while running:
    
        if onyourMark:
        
            if onlyClick:
                
                x,y = random_point_in_circle(120,'samsung')

                pyautogui.click(x,y, clicks=perClick)
            #sleep(3)
        # sleep(.5)
except KeyboardInterrupt:
    listener.stop()
    
    listener.join()
    
    print("Ended")
