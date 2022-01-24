import psutil 
import time , os
import win32api

PowerInteruptionCount = dict()  
counter =1 
init_state =  False
threshold = ""
'''
sets the battery life to 60% by default if it crosses or reaches that level it shuts down 
if you want to seconds between intervals of power in and power out  
'''

def Usage():
    global threshold
    __ = input("Enter precentage level before computer hibernates >>> ")
    threshold = int(__) if __.isdecimal()  else  False 

    if threshold > psutil.sensors_battery().percent :
        print("value supplied is greater than current battery level ")

    return threshold 



def HIB():
    #Hibernates the system
    
    # win32api.SetSystemPowerState(False,True) 
    os.system("shutdown /h")

def batteryLevel():

    return psutil.sensors_battery().percent 

def disconnection_interval(var):

    B4= sorted(var.keys(), reverse=True)[0]
    AF =  sorted(var.keys(), reverse=True)[1]

    CTI = AF - B4
    print(f"{AF} this is the after")
    print(f"{B4} this is the before")
    if len(var) > 1:
        print(var)
    
    return CTI 

def checkConnection():
    
    return psutil.sensors_battery().power_plugged



if __name__ == "__main__":

    Usage() 

    while True:
        current =  psutil.sensors_battery().power_plugged
       
        if current:
            print("plugged in")
            init_state = True
            # time.sleep(0.3)
        else:
            print("Cable Disconnected")
            print(threshold)

            if threshold:
                if batteryLevel() == threshold:
                    HIB() 
            
            else:

                if init_state == True:
                    
                    input("about to call this function")
                    init_state = False
                    PowerInteruptionCount[counter] =  time.time()
                    counter += 1

                    check =  disconnection_interval(PowerInteruptionCount) if len(PowerInteruptionCount) > 1 else False 
                    print(check)
                    input("Just wrote the thing for ")
                    
                    if type(check)  is not  bool and check <=200:
                        print("there slept for 100 seconds")
                        time.sleep(100)
                        HIB()

                    elif type(check) is not  bool  and check >= 201 and check <= 300:
                        if checkConnection()  ==True:
                            HIB()
                            # time.sleep(150)
                            print("there slept for 150 seconds")
                        # action 2
                    else:
                        if checkConnection()  ==True:

                            time.sleep(150)
                            print("Tehre slepping  for 360 seconds")
                            time.sleep(360)
                            
                        # take ACtion here
                
            
print(Usage() - 10)
# print(psutil.sensors_battery().power_plugged)