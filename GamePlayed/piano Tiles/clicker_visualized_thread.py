from asyncio import sleep
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
from threading import Thread


SCREEN_CAPTURE = (1452,60,1933,1035)

# THRESHOLD = ( 1450,660, 1920,901)
THRESHOLD = ( 2135,735, 2615,740)

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
upper_black = np.array([64, 64, 64], dtype=np.uint8)
sections= np.ones((4, 7, 480, 3))*255

clicker = False
rr = 60
keyP = {0:'a',1:'b',2:'c',3:'d'}
def watcher(section,idx):
    global keyP, rr
    while True:
        if np.sum(section[:,40:rr])==0:
            pyautogui.press(keyP[idx])
            sleep(1)
            print(keyP[idx])

def myThread():
    global sections
    while True:
        # Capture frame from screen
        frame =  ImageGrab.grab(THRESHOLD)
        # frame = pyautogui.screenshot(region=(THRESHOLD[0], THRESHOLD[1], 480, 240))
        frame = np.array(frame)  # Convert to NumPy array (BGR format)

        height, width, _ = frame.shape
        sec = width // 4
        # Split the frame into sections
        sections = [frame[:, sec*i:sec*(i+1)] for i in range(4)]

        sleep(.5)

if __name__ =="__main__":
    sleep(3)
    mm = Thread(target=myThread)
    mm.start() 
    for  i in range(4):
        thread = Thread(target=watcher, args=(sections[i],i))
        thread.start() 
        print(f"running Thread{i+1}")
    
    # while True:
    #     # Capture frame from screen
    #     frame =  ImageGrab.grab(THRESHOLD)
    #     # frame = pyautogui.screenshot(region=(THRESHOLD[0], THRESHOLD[1], 480, 240))
    #     frame = np.array(frame)  # Convert to NumPy array (BGR format)

    #     height, width, _ = frame.shape
    #     sec = width // 4
    #     # Split the frame into sections
    #     sections = [frame[:, sec*i:sec*(i+1)] for i in range(4)]

    #     sleep(.2)
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
    while True:
        
        sleep(5)
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
