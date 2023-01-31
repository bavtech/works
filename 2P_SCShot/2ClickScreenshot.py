# you would need an external  mouse to work with this as i used the mouse middle button
# 

from PIL import  ImageGrab 
import os 
from pynput import mouse
import notify2

origin_clicked =  False 

X,Y = 0,0
width,height =  0,0
ready2click= False 
middle_pressed = False 
screenshotName =  "screenshot"



#  PIL expects that screenshot are made  from top_left to bottom_right  , reversing this input and moving from bottom_left to top_right would throw an error , this function  checks and corrects that . so no matter what direction  you move the no error is thrown
    
def checker(A,B):

    collate =  A+B 
    collate= list(collate)
    duplicated =  collate[::]

    # it is expected that value at index 3  and 2 be always greater than  value at index 1 and 0
    collate[3] =  max(duplicated[1], duplicated[3])
    collate[1] =  min(duplicated[1],duplicated[3])
    collate[2] =  max(duplicated[2], duplicated[0])
    collate[0] =  min(duplicated[2],duplicated[0])
    
    
    return tuple(collate)

# saves screenshot serially , if  a file is deleted up the  chain the new screenshot would  take the name of the deleted file
def fileSave (pilgrab):

    global screenshotName

    i=1
    
    while True:

        name =  screenshotName+f"{i}.png"
        if os.path.exists(name):
            i +=1 
        else:
            pilgrab.save(name)
            break

def notify(title,readyMessage, alternative ):
    
    global ready2click 
   
    notify2.init("My App")   # x,y = 0,0

    # Create the notification
    n = notify2.Notification(title or "Screenshot" ,readyMessage or "can screenshot now" if ready2click else alternative or "screenshot disabled" )
    n.set_timeout(2500)
    # Show the notification
    n.show()

def on_click(x, y, button, pressed):
    global origin_clicked, final_clicked, X,Y, width, height ,ready2click,middle_pressed

    # checks  if the mouse middle button   has been pressed
    if button == mouse.Button.middle:   
        ready(X,Y,pressed) 
        middle_pressed= not middle_pressed

    if ready2click:
        
        try:
            if origin_clicked and middle_pressed:
                origin_clicked =  not origin_clicked
            
            elif button == mouse.Button.left and origin_clicked == False:
                 
                if pressed:

                    origin_clicked =  True 
                    X,Y  = x,y 

                    print("ORIGIN AT ({0}, {1})".format(x, y))
                    notify("MESSAGE","SELECT LOCATION TWO TO COMPLETE SCREENSHOT","AA")

            elif button == mouse.Button.left and origin_clicked == True:
                
                if pressed:
                    print("FINAL POINT AT ({0}, {1})".format(x, y))
   
                    print()
                    origin_clicked =  False 
                    width,height =  x,y 
                    grab =  ImageGrab.grab(checker((X,Y),(width,height)))
                 
                    fileSave(grab)
                    notify("CAPTURED","SCREENSHOT SAVED","NOTHING TO SAVE YET")
                    X,Y,width,height = 0,0,0,0
          
        except ValueError as e:
        
            grab =  ImageGrab.grab(checker((X,Y),(width,height)))
            fileSave(grab)
            print("Error thrown")


def ready(x,y,pressed):
    global ready2click,width, height
    if pressed:
        
        ready2click = not ready2click
        notify("MESSAGE","SCREENSHOT ACTIVATED",'SCREENSHOT DEACTIVATED ORIGIN SET TO (0,0) ') 
     
        if ready2click == False:
            x,y,width,height=0,0,0,0
              
if __name__ == '__main__':
    print("""\nNOTE:You would need an external mouse for this to work.\n
THIS IS NOT A CLICK ONE POINT AND DRAG TO ANOTHER POINT PROGRAM ,
THIS IS A CLICK ONE POINT ,THEN CLICK ANOTHER POINT AND A SCREENSHOT THAT FALLS WITHIN THE INITLA AND FINAL POINT WOULD BE  SAVED TO THE SAME PATH WHERE THE SCRIPT IS LOCATED.\n\n
    
    YOU WOULD GET A NOTIFICATION FROM  TIME TO TIME ON WHAT TO DO
        
    \n1. press the middle mouse button to activate the listener 
   \n2. click first point 
   \n3. click second point that forms a rectangle.
   \n4. If you are unsure of the points previously clicked, press the middle mouse button twice and it would reset the point
    """)
    try:

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
    except (SystemError,ValueError ) as e:
        print("error Thrown in mouse listener") 
