import os , shutil
from pathlib import Path 



print("By default the validation file are picked 1 for 5 files copied to the train folder")

while True:
    try:
        val_pass =  input("if your data isnt that much or you wish to tweak this you enter an integer >>> ")
        if val_pass ==  "":
            val_pass = 5
            break
        else:
            val_pass =  int(val_pass) 
            break
    except ValueError:
        print("Incorrect value passed in please pass only integer values")
    

if os.path.exists("train"):
    pass
else:
    os.makedirs("train/images")
    os.makedirs("train/labels")
    
    
if os.path.exists("val"):
    pass

else:
    os.makedirs("val/images")
    os.makedirs("val/labels")
    
    
    
img_folder =  Path("images")
label_folder = Path("labels")

train_img =  Path("train/images")
train_lbl =  Path("train/labels")

val_img =  Path("val/images")
val_lbl =  Path("val/labels")

pf =  ".jpg"

os.listdir(img_folder)


for idx,FName  in enumerate(label_folder.rglob("*.txt"), start=1):
    
    if idx %val_pass == 0:
        shutil.copy(FName,val_lbl)
        
        pic =Path(str(img_folder) + f"/{FName.stem}{pf}" )
        shutil.copy(pic, val_img)
        
    else:
        
        shutil.copy(FName, train_lbl)
        # print(FName.parent)
        pic =Path(str(img_folder) + f"/{FName.stem}{pf}" )
        # print(pic)
        shutil.copy(pic, train_img)
