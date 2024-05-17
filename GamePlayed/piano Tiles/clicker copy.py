from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
pyautogui.press


SCREEN_CAPTURE = (1452,60,1933,1035)

# THRESHOLD = ( 1450,660, 1920,901)
THRESHOLD = ( 2135,550, 2615,800)

# while True:
    
#     frame =  np.array



# hsv =  cv2.cvtColor(corrected,cv2.COLOR_BGR2HSV)

# cv2.imshow("hsv", corrected)
# # cv2.imshow("hsv", hsv)
# WIDTH =  115
# box1=THRESHOLD[0]+WIDTH
# box2=THRESHOLD[0]+WIDTH*2
# box3=THRESHOLD[0]+WIDTH*3
# box4=THRESHOLD[0]+WIDTH*4
clicked = dict(A=False, B=False,C=False, D=False)
counter =0
# mid =  THRESHOLD[2] -  THRESHOLD[0]
# center_x = x + w / 2
# center_y = y + h / 2
A,B,C,D = 0,0,0,0
def reset():
    global clicked    
    clicked = {key: False for key in clicked}
    
    
while True:
    # Capture frame from screen
    frame =  ImageGrab.grab(THRESHOLD)
    height, width=  int(frame.height/2), frame.width
    line_width  = width //6

    sec = int( width/4)
    # print(frame.height, frame.width)
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # last_50_px =  width - line_width
    # frame[:, width//4:, :] = [255, 255, 255]
    
    section1 = frame[0:height, 0:sec]
    section2 = frame[0:height, sec:sec*2]
    section3 = frame[0:height, sec*2:sec*3]
    section4 = frame[0:height, sec*3:sec*4]
    cut = 60
    section1[:, sec-30:sec +cut, :] = [255, 255, 255]
    section2[:, (sec*2)-30:sec*2 +cut, :] = [255, 255, 255]
    section3[:, (sec*3):sec*3+cut , :] = [255, 255, 255]
    section4[:, (sec*4)-30:sec*4, :] = [255, 255, 255]
    # corrected =  cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # Convert BGR to HSV
    
    lower_black = np.array([0, 0, 0],dtype=np.uint8)
    upper_black = np.array([64, 64, 64], dtype=np.uint8)
    # Display HSV image
    
    mask1 = cv2.inRange(section1, lower_black, upper_black)
    mask2= cv2.inRange(section2, lower_black, upper_black)
    mask3 = cv2.inRange(section3, lower_black, upper_black)
    mask4 = cv2.inRange(section4, lower_black, upper_black)
    # mask = cv2.erode(mask, None, iterations=2)
    # mask = cv2.dilate(mask, None, iterations=2)
   
    # contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    # for contour in contours:
    #     x,y,w,h  =  cv2.boundingRect(contour)
    #     center_x = x + w // 2
        
    #     if (center_x, y) > 
    # print(len(contours))
    if np.any(mask1) and np.any(mask2):
        if clicked['A'] and clicked['B']:
            
            if A>0:
                pass
            else:
                pyautogui.press('a')
                C,D = 0,0
                A+=1
                
                
            if B>0:
                pass
            else:
                pyautogui.press('b')
                C,D = 0,0
                B+=1
            
    
        else:
            reset()
            clicked["A"]= not clicked['A']
            clicked["B"]= not clicked['B']
            print("Both A and B clicked")
            
    elif np.any(mask1) and np.any(mask3):
        if clicked['A'] and clicked['C']:
            if A>0:
                pass
            else:
                pyautogui.press('a')
                B,D = 0,0
                A+=1
                
                
            if C>0:
                pass
            else:
                pyautogui.press('c')
                B,D = 0,0
                C+=1
        
        else:
            reset()
            clicked["A"]= not clicked['A']
            clicked["C"]= not clicked['C'] 
           
            print("Both A and C clicked")
    elif np.any(mask1) and np.any(mask4):
        if clicked['A'] and clicked['D']:
            if A>0:
                pass
            else:
                pyautogui.press('a')
                B,C = 0,0
                A+=1
                
                
            if D>0:
                pass
            else:
                pyautogui.press('d')
                B,C = 0,0
                D+=1
        else:
            reset()
            clicked["A"]= not clicked['A']
            clicked["D"]= not clicked['D'] 

            print("Both A and D clicked")
    elif np.any(mask2) and np.any(mask3):
        if clicked['b'] and clicked['c']:
            if B>0:
                pass
            else:
                pyautogui.press('b')
                A,D = 0,0
                B+=1
                
                
            if C>0:
                pass
            else:
                pyautogui.press('c')
                A,D = 0,0
                D+=1
      
        else:
            reset()
            clicked["B"]= not clicked['B']
            clicked["C"]= not clicked['C']
            print("Both B and C clicked")
    elif np.any(mask2) and np.any(mask4):
        
        if clicked['b'] and clicked['d']:
            if B>0:
                pass
            else:
                pyautogui.press('b')
                A,C = 0,0
                B+=1
                
                
            if D>0:
                pass
            else:
                pyautogui.press('d')
                A,C = 0,0
                D+=1
        else:
                
            reset()
            clicked["B"]= not clicked['B']
            clicked["D"]= not clicked['D']
            
            print("Both B and D clicked")
    elif np.any(mask1):
        if clicked["A"]:
            if A>0:
                pass
            else:
                pyautogui.press('a')
                A +=1
    
        else:
            reset()
            clicked["A"]= not clicked['A']
            B,C,D = 0,0,0
            print("click A")
    elif np.any(mask2):
        if clicked["B"]:
            if B>0:
                pass
            else:
                pyautogui.press('b')
                B +=1
        else:
            reset()
            clicked["B"]= not clicked['B']
            A,C,D = 0,0,0
            print("click B")
    elif np.any(mask3):
        if clicked["C"]:
            if C>0:
                pass
            else:
                pyautogui.press('c')
                C +=1
        else:
            reset()
            clicked["C"]= not clicked['C']
            A,B,D = 0,0,0
            print("click C")
    elif np.any(mask4):
        if clicked["D"]:
            if D >0:
                pass
            else:
                pyautogui.press('d')
                D +=1
                
        else:
            reset()
            clicked["D"]= not clicked['D']
            A,B,C = 0,0,0
            print("click D")
        # counter+=1
    # cv2.imshow('HSV Image', mask)
    cv2.imshow('masked', mask3)
    # Exit on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
