

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
    global  onlyClick, clicks, radius,onyourMark,coor 
    try:
        
               
        # try:
            # checks if character given is in int and pass it to click
       
        if key.char=='+':
            clicks +=1
            
        elif key.char =='-':
            if clicks==1:
                pass
            else:
                clicks -=1 
        else:
            
            # print(key.char)
            char =  key.char
            char= int(char)
            
            clicks=char 
            # print("works")
        print(f"Now Clickiing at speed {clicks}")
    
#        
    except Exception as e:
        # if key==keyboard.Key.space:
        #     onyourMark =  not onyourMark
            
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
clicks=1

radius=10
count = 0
mouse =  Controller()
coor= getMousePosition()

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
        mouse.click(Button.left,clicks)
        sleep(0.05)
        # print(clicks)
print("loop ended")       
        
listener.stop()
kListen.stop()