from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
pyautogui.press


SCREEN_CAPTURE = (1452,60,1933,1035)

# THRESHOLD = ( 1450,660, 1920,901)
THRESHOLD = ( 2135,550, 2615,800)

clicked = dict(A=False, B=False,C=False, D=False)
counter =0

A,B,C,D = 0,0,0,0
def reset():
    global clicked    
    clicked = {key: False for key in clicked}
    
rcut = 20
lcut = 30 
vcut= 55
y = 730
Ax = 2250
Bx = 2300
Cx = 2400
Dx = 2500

lower_black = np.array([0, 0, 0],dtype=np.uint8)
upper_black = np.array([64, 64, 64], dtype=np.uint8)\


clicker = False
while True:
    # Capture frame from screen
    # frame =  ImageGrab.grab(THRESHOLD)
    frame = pyautogui.screenshot(region=(THRESHOLD[0],THRESHOLD[1],480,240))
    height, width=  frame.height, frame.width
    # line_width  = width //6

    sec = int( width/4)
    # print(frame.height, frame.width)
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    
    section1 = frame[0:height, 0:sec]
    section2 = frame[0:height, sec:sec*2]
    section3 = frame[0:height, sec*2:sec*3]
    section4 = frame[0:height, sec*3:sec*4]
    

    
    section1[:, sec-rcut:, :] = [255, 255, 255]
    section2[:, sec-rcut:, :] = [255, 255, 255]
    section3[:, sec-rcut:, :] = [255, 255, 255]
    section4[:, sec-rcut:, :] = [255, 255, 255]
    
    
    section1[:, 0:lcut, :] = [255, 255, 255]
    section2[:, 0:lcut, :] = [255, 255, 255]
    section3[:, 0:lcut, :] = [255, 255, 255]
    section4[:, 0:lcut, :] = [255, 255, 255]
    
    section1[0:vcut, ::] = [255, 255, 255]
    section2[0:vcut, ::] = [255, 255, 255]
    section3[0:vcut, ::] = [255, 255, 255]
    section4[0:vcut, ::] = [255, 255, 255]
       
    # Display HSV image
    
    mask1 = cv2.inRange(section1, lower_black, upper_black)
    mask2= cv2.inRange(section2, lower_black, upper_black)
    mask3 = cv2.inRange(section3, lower_black, upper_black)
    mask4 = cv2.inRange(section4, lower_black, upper_black)
    
    
    for idx,mask in enumerate([mask1,mask2,mask3,mask4]):
        
        if np.any(mask):
            if clicker >0:
                pass
            else:
                pyautogui.click(Ax+(idx*100),y)
                clicker+=1
        else:
            clicker=0
               
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
