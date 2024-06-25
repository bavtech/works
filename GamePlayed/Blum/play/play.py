import random
import string
import subprocess
from time import sleep
import time
from PIL import ImageGrab,Image
import cv2
import numpy as np
import pyautogui
from pynput import keyboard
import sys
from ultralytics import YOLO 
from pynput.mouse import Listener, Button,Controller



# SCREEN_CAPTURE = (1440,0,1925,946)

# THRESHOLD = ( 1450,660, 1920,901)
# THRESHOLD = ( 2135,550, 2615,800)

counter =0
device_name =  sys.argv

clicker = False

running = True
onyourMark= False
samp ='3'

def on_press(key):
    global paused, confidence
    try:
        
        if key.char == '+':
            if  confidence+ 0.01 > 1 :
                confidence =1 
                
            if confidence <1 :
                # confidence +=0.02
                refactor(0.01)
                print(f"Confidence score now{confidence}")
                
        if key.char =='-':
            
            if confidence >0.5:
                    refactor(-0.01)
                    # confidence -=0.02
                    print(f"Confidence score now{confidence}")
            
#        
    except AttributeError:
        # Handle special keys here if needed
        if key == keyboard.Key.space:
            # print('Space bar press')
            paused =  not paused
            if paused:
                print("Taking keyboard inputs")
            else:
                print(" Keyboard Input Paused")
        if key == keyboard.Key.page_up:
            if confidence >1:
                confidence =1 
                
            if confidence <1:
                # confidence +=0.02
                refactor(0.01)
                print(f"Confidence score now{confidence}")
        if key == keyboard.Key.page_down:
            if confidence >0.5:
                refactor(-0.01)
                # confidence -=0.02
                print(f"Confidence score now{confidence}")
                
        

def on_release(key):
    global running
   
    try:
        
        if key.char == 'q':
         #             # print("Key 'q' pressed, exiting loop.")
            print("Exiting Keyboard press")
            running = False
            return False 
    except Exception as e:
        # print("Not recognized")
        pass
#         # Stop the listener




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

def refactor(val):
    global confidence 
    
    confidence += val
    
    formatted_result = f"{confidence:.2f}"
    # return float(formatted_result)
    confidence =  float(formatted_result)
    
def getCenter(coor):
    
    x_min = coor[0]
    y_min = coor[1]
    x_max = coor[2]
    y_max = coor[3]
    
    center_x =  int(x_min + x_max)//2
    center_y =  int(y_min + y_max)//2
    
    return y_max, (center_x,center_y)
temp='' 
ma = ''
def colorDetected(pixel):
    global temp ,SCREEN_CAPTURE,ma
    x1,y1,x2,y2 =  SCREEN_CAPTURE[0]+ pixel[0], SCREEN_CAPTURE[1]+ pixel[1], SCREEN_CAPTURE[0]+ pixel[2],SCREEN_CAPTURE[1]+pixel[3]
    frame2 = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    frame2 =  np.array(frame2)
    hsv = cv2.cvtColor(frame2, cv2.COLOR_RGB2HSV)


    blurred_image = cv2.blur(hsv, (15, 15))
    ma=hsv

    lower_bound = np.array([35, 50, 50],dtype=np.uint8)  
    upper_bound = np.array([85, 255, 255], dtype=np.uint8)
    
    mask =  cv2.inRange(blurred_image, lower_bound, upper_bound)   

    temp=mask
    
    if cv2.countNonZero(mask)>0:
        return True
    
    else:
        return False
    
    
# SCREEN_CAPTURE =  getCordinate('samsung')
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
paused=  False 
gap =440

confidence=.91
mouse =  Controller()
# sleep(5)
model =  YOLO("red_det.pt",verbose=True)
prev=(0,0)
device_name =  device_name[1]
while running:
#     #     # Capture frame from screen
    SCREEN_CAPTURE =  getCordinate(device_name)
    # st =  time.time()

    frame =  ImageGrab.grab(SCREEN_CAPTURE)
    
    
    height,width =  frame.height, frame.width 
    
    frame=  np.array(frame)
    
    if "samsung" in device_name.lower() or "personal" in device_name.lower():
        
        v_cut1 =  int((height//2) -(height * 0.25))
        v_cut2 =  int((height//2) +(height*0.2)) 
        
        frame[0:v_cut1, ::] = [255, 255,255]
        frame[v_cut2:, ::] = [255, 255,255]

    
    frame =  Image.fromarray(frame)
    
    results = model.predict(frame,conf=confidence,verbose=False)[0]
    results = results.cpu().boxes.xyxy.numpy()
    print(len(results),"Flakes Found",end='\r')
    if paused:
        
        for result in results:
            
            
                
                flkH,center = getCenter(result)
                
                # pyautogui.click(SCREEN_CAPTURE[0]+center[0], center[1]+SCREEN_CAPTURE[1],clicks=1)
                x =  SCREEN_CAPTURE[0]+ center[0]
                y =  SCREEN_CAPTURE[1]+ center[1]
                
                # if colorDetected(result):
                if int(prev[0])!= int(x) and int(prev[1]) != int(y):
                    mouse.position=(x,y)
                    mouse.click(Button.left,1)

                    prev =  (x,y)

    # print(f"took {time.time() - st}")


# USE SPACEBAR TO TOGGLE WHEN THE AI DETECTS
# PLUS AND MINUS TO INCREASE OR DECREASE CONFIDENCE LEVEL
# BUTTON Q OR EXIT TO QUIT THE PROGRAM
    
  
