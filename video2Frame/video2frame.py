import cv2 
from time import sleep 
import time , os 
from tkinter import filedialog 
from tkinter import * 


filepath = filedialog.askopenfile(title="SELECT VIDEO FILE", filetypes=(("video    files",("*.mp4","*.MP4")),))

video =  cv2.VideoCapture(filepath.name) 


# Get the number of frames in the video file
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate the length of the video in seconds
fps = video.get(cv2.CAP_PROP_FPS)
video_length = total_frames / fps

print(f"FPS {fps}")

VIM =  video_length/60
VIM =  float(f"{VIM:.1f}") 

VIS =  video_length
VIS =  float(f"{VIS:.1f}")
S_or_M =  "Minute" if video_length > 60 else "Seconds" 


filename =  os.path.splitext(os.path.basename(filepath.name))[0]
path2save = STORAGE
counter=1
starttime =time.time(

print("The Length of video is {1} {0}".format(S_or_M,VIS if video_length < 60 else VIM))


STORAGE = filedialog.askdirectory (title="SELECT FOLDER TO STORE FRAMES CAPTURED")

while True:
    
    try:
        
        TInterval =  input(f"enter the time interval at which you want screenshots to be saved default is 1s ")
        if TInterval == "":
            TInterval = 1
        else:
            TInterval = float(TInterval)
        break 
    except ValueError:
        print("Incorrect value  enter a float or an integer , no strings")
        
        
)


def save(name):
    global counter, starttime,filename
    tmp = name
    name =  f"{name}/{filename}-{counter}.jpg"
    
    while True:
        if os.path.exists(name):
            counter +=1
            name =  f"{tmp}/{filename}-{counter}.jpg"
        else:
        
            cv2.imwrite(name, frame)
            counter+=1
            starttime =  time.time()
            
            break
           
while video.isOpened():
    ret, frame = video.read()
    
    if ret:
        
        # resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("frame", frame)
        
        if (time.time() -  starttime) >TInterval:
            save(f"{path2save}")
            
        # sleep(1)
        #if counter ==100:
         #   break 
        if cv2.waitKey(int(fps)) & 0xFF == ord('q'):
            
            break
    else:
        break 

video.release()
cv2.destroyAllWindows() 



