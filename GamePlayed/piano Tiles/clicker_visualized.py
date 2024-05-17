from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
pyautogui.press


SCREEN_CAPTURE = (1452,60,1933,1035)

# THRESHOLD = ( 1450,660, 1920,901)
THRESHOLD =  ( 2135,710, 2615,740)

clicked = dict(A=False, B=False,C=False, D=False)
counter =0

A,B,C,D = 0,0,0,0
def reset():
    global clicked    
    clicked = {key: False for key in clicked}
    
rcut = 20
lcut = 30 
vcut= 55
y = 680 #730 works optimally
Ax = 2250
Bx = 2300
Cx = 2400
Dx = 2500

lower_black = np.array([0, 0, 0],dtype=np.uint8)
upper_black = np.array([64, 64, 64], dtype=np.uint8)\


clicker = False
while True:
    # Capture frame from screen
    frame =  ImageGrab.grab(THRESHOLD)
    # frame = pyautogui.screenshot(region=(THRESHOLD[0], THRESHOLD[1], 480, 240))
    frame = np.array(frame)  # Convert to NumPy array (BGR format)

    height, width, _ = frame.shape
    sec = width // 4
    # Split the frame into sections
    sections = [frame[:, sec*i:sec*(i+1)] for i in range(4)]

   
    rr = 70
    # if np.sum(sections[0][:,40:rr])==0:
    #     # pyautogui.click(Ax,y)
    #     pyautogui.press('a')
    #     print("a")
    # if np.sum(sections[1][:,40:rr])==0:
    #     # pyautogui.click(Ax+100,y)
    #     pyautogui.press('b')
    #     print("b")
    # if np.sum(sections[2][:,40:rr])==0:
    #     # pyautogui.click(Ax+200,y)
    #     pyautogui.press('c')
    #     print("c")
    # if np.sum(sections[3][:,40:rr])==0:
    #     # pyautogui.click(Ax+300,y)
    #     pyautogui.press('d')
    #     print("d") 
    _lr, _rr = 25,100
    if np.sum(sections[0][_lr,_rr])==0:
        pyautogui.click(Ax,y)
        # if clicked['A']:
        #     pass
        # else:
        #     pyautogui.press('a')
        #     reset()
        #     clicked['A']=True 
        
        print("click a")
    if np.sum(sections[1][_lr,_rr])==0:
        pyautogui.click(Ax+100,y)
        # if clicked['B']:
        #     pass
        # else:
        #     pyautogui.press('b')
        #     reset()
        #     clicked['B']=True
        print("click b")
    if np.sum(sections[2][_lr,_rr])==0:
        
        pyautogui.click(Ax+200,y)
        # if clicked['C']:
        #     pass
        # else:
        #     pyautogui.press('c')
        #     reset()
        print("Click c")
    if np.sum(sections[3][_lr,_rr])==0:
        pyautogui.click(Ax+300,y)
        # if clicked['D']:
        #     pass
        # else:
        #     pyautogui.press('d')
        #     reset()
        print("Click d")
               
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
