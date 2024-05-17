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
y = 750 #730 works optimally
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
    frame = pyautogui.screenshot(region=(THRESHOLD[0], THRESHOLD[1], 480, 240))
    frame = np.array(frame)  # Convert to NumPy array (BGR format)

    height, width, _ = frame.shape
    sec = width // 4
    # Split the frame into sections
    sections = [frame[:, sec*i:sec*(i+1)] for i in range(4)]

    # Apply white masks to section borders
    for section in sections:
        section[:, -rcut:] = [255, 255, 255]  # Right cut
        section[:, :lcut] = [255, 255, 255]   # Left cut
        section[:vcut, :] = [255, 255, 255]   # Top cut

    # Convert sections to HSV and apply black mask
    masks = [cv2.inRange(cv2.cvtColor(section, cv2.COLOR_BGR2HSV), lower_black, upper_black) for section in sections]
        
    
    for idx,mask in enumerate(masks):
        
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
