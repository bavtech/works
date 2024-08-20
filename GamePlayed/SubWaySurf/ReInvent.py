import os
from pathlib import Path
import random
import string
import subprocess
from time import sleep
import time
from PIL import ImageGrab,Image
from pynput import keyboard


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


# def generate_unique_name(prefix="nm"):
#     global counter #last_2
#     """Generate a unique name with a maximum of 8 characters."""
    
#     refresh = 'uAEjindqwDCAEGueiqpieEClikujmDFGZcvcxponbvf'
#     # Limit the prefix to a maximum of 2 characters to allow room for uniqueness
#     file_size = Total_file()
    
   
        
#     if file_size %1000==0:
#         counter +=1
        
#         with open("progress.txt",'w') as file:
#             file.write(str(counter))
#         # last_2 += counter
#     prefix = prefix[0]+refresh[counter]

#     # Generate a random 4-character string from letters and digits
#     unique_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6 - len(prefix)))

#     # Combine the prefix with the unique suffix
#     unique_name = f"{prefix}{unique_suffix}"
    
#     return unique_name
# last_2 = 0
def generate_unique_name():
    global counter
    file_size =  Total_file()
    
    # if file_size+1 %1000==0:
        
    with open("progress.txt",'w') as file:
        file.write(str(counter))
#         # last_2 += counter
    name =  f"{counter}.png" 
    counter +=1
    
    return name


def Total_file():
    
    
    global path 
    
    directory =  Path(path)
    match_files =  list(directory.rglob("*.png"))
    
    return len(match_files)


def grab_n_spit():
    global path , confidence
    cord =  getCordinate('samsung')
    img = ImageGrab.grab((cord[0],cord[1],cord[2]-(cord[2]*0.015),cord[3]-(cord[3]*0.018)))
    name = generate_unique_name()
    img.save(f"{path}/{name}.png")
    sleep(confidence)
    
    # return transform(img).unsqueeze(0).to(device) 

def run():
    global paused
    while paused:
        grab_n_spit()

def refactor(val):
    global confidence 
    
    confidence += val
    
    formatted_result = f"{confidence:.2f}"
    # return float(formatted_result)
    confidence =  float(formatted_result)     

def on_press(key):
    global paused, confidence
    try:
        
        if key.char == '+':
            if  confidence+ 0.02 > 1 :
                confidence =1 
                print(f"Cant go beyond  {1/confidence} Frame per second")
                
            if confidence <1 :
                # confidence +=0.02
                refactor(0.02)
                print(f"Frames per second now at {1/confidence}")
                
        if key.char =='-':
            
            
            # if confidence >0.5:
            #         refactor(-0.02)
            #         # confidence -=0.02
            #         print(f"Frames per second now at {1/confidence}")
            refactor(-0.02)
            
            if confidence < 0.02:
                confidence = 0.02 
                print(f"Cant go further than  {1/confidence} frames per Second") 
            else:
                print(f"Frames per second now at {1/confidence}")
            
#        
    except AttributeError:
        # Handle special keys here if needed
        if key == keyboard.Key.space:
            # print('Space bar press')
            paused =  not paused
            if paused:
                print("Taking Screenshots")
            else:
                print("Screen Shots Paused")
        if key == keyboard.Key.page_up:
            if confidence >1:
                confidence =1 
                
            if confidence <1:
                # confidence +=0.02
                refactor(0.02)
                print(f"Frames per second now at {1/confidence}")
        if key == keyboard.Key.page_down:
            if confidence >0.5:
                refactor(-0.02)
                # confidence -=0.02
                print(f"Frames per second now at {1/confidence}")
                
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
              
        
if __name__ == '__main__':
    print("KEYS TO PRESS  \n + Decreases speed  of Frame capture \n - Increases Speed of Frame capture \n SPACE pauses Frame capture ")
    paused=False 
    confidence=0.02
    running = True
    path =  "/home/grey/Documents/AI/Supervised/GamePlayWithAI/SubWaySurf/SHOTS"
    
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    if os.path.exists("progress.txt"):
        with open("progress.txt",'r') as file:
            counter=  file.read()
            counter =  int(counter)
    else:
        counter =0
        
    while running:
        
        run()
    