#
# THIS WAS USED FOR THE SUBWAY SURF DATA GATHERING
# 
# 
from PIL import ImageGrab
from time import sleep
import time 
import pandas as pd
from pynput.keyboard import Key,KeyCode, Listener

prev_name =''
new_name=''
isdone=False 
pause = False
filename = "new_csv.csv"
sleeper = 6
current_key= "blank"
begin = False
df_idx =0
dfp=0
Mdtypes = {'image': int, 'keyPress': str}
# serves more like checkpoint to avoid overrting perviously saved images
counter_var = "counter.txt"
acceptable_keys  =["'a'","'s'","'d'","'w'"]

freq =  dict(pd.read_csv(filename)['keyPress'].value_counts())
_blk = freq['blank']
fc =[]
for i,j in freq.items():
    if i in acceptable_keys:        
        if j >= _blk  :
            fc.append(True)
        else:
            fc.append(False)

if all(fc):
    
    isdone=True
    print("all keys are balanced")

def creatDF( name:str):
    global counter,df_idx,dfp
    try:
        # df = loadPickle(name)
        df =  pd.read_csv(name,dtype=Mdtypes)
        df_idx =  df.shape[0]
        dfp =  df_idx
    except FileNotFoundError :
        
        df = pd.DataFrame(columns=['image', 'keyPress'])
        df.image.astype(int)
    
    return df

def screenSave():
    im2 = ImageGrab.grab(bbox=(2137,59,2609,1047))
    
    name =  nameMaker() 
    path = "SHOTS/"
    filename = path+name 
    
    counter+=1
    df_idx+=1
    return new_name+".jpg"

def onPress(key):
    global pause , current_key, isdone, begin,df_idx
    
    if df_idx %1000==0:
            df.to_csv(filename, index=False,)
            print("Checkpoint Saved")
    try:
        
        if "Key" in str(key):
            pass 
        
        else:
            
            current_key =  key
            
            if str(current_key) in acceptable_keys:
                
                if not dataIsBalanced(str(current_key)):
                    
                    screenSave()
                    df.loc[df_idx, ['image', 'keyPress']] = [counter-1, current_key ]
                    
                    freq[str(current_key)] = freq[str(current_key)]+1
                    print(current_key,"------pressed")
                else:
                    print("key has been balanced")
            
            # if str(key) in acceptable_keys:
                
            #     begin=True
            #     pause = True
            #     current_key =  key
            #     screenSave()
            #     df.loc[df_idx, ['image', 'keyPress']] = [counter, current_key ]
                
            #     pause= False 
            #     print(current_key,"------pressed") 
            #     current_key = "blank"
            # else: pass
    except  Exception as e:
        print(e.__class__.__name__)
        print("an Exception occured")
        isdone=True


def onRelease(key):
    global isdone
    if key== Key.esc:
        isdone =  True
        
        return False 
def dataIsBalanced(param:str):
    global freq 
       
    if freq[param]>= freq['blank']:
        return True
    else:
        return False
        
def checkpoint():
    global counter_var
    
    
    try:
        with open(counter_var,'r') as file:
            counter =  int(file.readline() )
            counter +=1 
            
        return counter 
    
    except FileNotFoundError:
        counter=0
        with open(counter_var,'w') as file:
            file.write(str(counter))
        
        return counter
            
    
if __name__ == "__main__":

    # INTIALIZE THE COUNTER BY CALLING IT
    counter =  checkpoint()

    
    
    df =  creatDF(filename)
    print(f"counter: {counter} \t\t df_index: {df_idx} ")
    print(freq)
    sleep(5)
    print("GO!!")
    
    
    listner =    Listener(on_press=onPress,on_release=onRelease)
    listner.start()
    
    # remove this join as this waits for the main thread to end before it ends
    # listner.join()
    # uncomment this to get input
    
    while True:
        
        # this starts the capture process once a key is pressed
        if begin:
            
            while not isdone:
                
                if not pause:
                    # uncomment below to get full blank being written in
                    # screenSave()
                    # df.loc[df_idx, ['image', 'keyPress']] = [counter, current_key ]
                    # time.sleep(0.27)
                    pass
        if isdone:
            break 
    
        
               
    print(f"total Keys pressed {df_idx - dfp}")
    df.to_csv(filename, index=False,)
    # print(isdone)   
    
# get the frequencies of all the key inputs count and take account 
# then take account and disable each key input when they get equal to the amount the max which is blank