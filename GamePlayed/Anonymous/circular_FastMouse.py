

import math
import random
from time import sleep

import pyautogui
from pynput.mouse import Listener, Button,Controller
from pynput import keyboard

def random_point_in_circle(radius,coor):
    """
    Generate a random point within a circle.
    """
    
    
    angle = random.uniform(0, 2 * math.pi)
    
    r = radius * math.sqrt(random.uniform(0, 1))
    x = int(coor[0] + r * math.cos(angle))
    y = int(coor[1] + r * math.sin(angle))
    return x, y

def getMousePosition() :
    x,y= pyautogui.position()
    
    return (x,y) 

def on_release(key):
    global running
    if key== keyboard.Key.esc:
        
        running = False
        print("Exiting mouse click")
        return False 


def on_press(key):
    global  onlyClick, clicks, radius,onyourMark,coor , sleeper
    try:
        
               
        # try:
            # checks if character given is in int and pass it to click
       
        if key.char=='+':
            clicks +=1
            sleeper +=0.001
            
            sleeper =  f"{sleeper:.3f}"
            sleeper =  float(sleeper)
            
        elif key.char =='-':
            if clicks==1:
                pass
            else:
                # clicks -=1 
                sleeper -=0.001
                sleeper =  f"{sleeper:.3f}"
                sleeper =  float(sleeper)
        else:
            
            # print(key.char)
            char =  key.char
            char= int(char)
            
            # clicks=char 
            sleeper =  0.01 if char < 1 else 0.01 * char
            sleeper =  f"{sleeper:.3f}"
            sleeper =  float(sleeper)
            # print("works")123
        # print(f"Now Clickiing at speed {sleeper}")
        print(f"speed now at {sleeper} " ,end='\r')
    
#        
    except Exception as e:
        if key==keyboard.Key.space:
            onyourMark =  not onyourMark
               
            if onyourMark:
                print("Now clicking")
            else:
                print("paused")
        #     print(onyourMark)
        #     # if onyourMark:
        #     coor= getMousePosition()
        #     print(coor)
            
        if key== keyboard.Key.up:
            radius +=1
            print(f"new Radius{radius}")
        elif key== keyboard.Key.down:
            if radius <15:
                pass
            else:
                radius -=1
            print(f"new Radius{radius}")
        
        

           
    
def on_click(x, y, button, pressed):
    global onyourMark, coor
    
    
    if button == Button.right and pressed:
        coor= getMousePosition()
        
        # sleep(0.3)
        onyourMark =  not onyourMark
        
        print("clicking" if onyourMark else "paused")
        # if onyourMark:
        # print(coor)
        # print(f"Left mouse button clicked at ({x}, {y})")

# Start the mouse listener
#   ()
listener =  Listener(on_click=on_click)
listener.start() 
# keyboard Listener 
kListen =  keyboard.Listener(on_press=on_press,on_release=on_release)
kListen.start() 

running= True 
onyourMark=False
clicks=0

radius=10
count = 0
mouse =  Controller()
coor= getMousePosition()
sleeper = 0.050
try:

    while running:
    # count +=1
    # print(count)0
        if onyourMark:
        
        # mpt =  getMousePosition()
        # x,y = random_point_in_circle(radius,coor)
            x,y =  getMousePosition()

        # pyautogui.click(x,y, clicks=clicks ) 
        # sleep(0.1)
        
            mouse.position=(x,y)
            mouse.click(Button.left,1)
            sleep(sleeper)
        # print(clicks)
except KeyboardInterrupt:
    
    listener.stop()
    kListen.stop()
    
    listener.join()
    kListen.join()
    
    print("Ended Gracefully")
 
# 17.8 @0.055
# 19 @ 0.051
# 18.6 @0.052
# 