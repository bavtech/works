from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
import os 
import shutil 
from tkinter import filedialog 
import re

with open("last_seen.txt" ,'r') as file:
    
    last_seen = file.readline().strip()

def writeToFile(filename:str):
    with open("last_seen.txt",'w') as file:
        file.write(filename)
     
def extract_number(filename):
    return int(filename[:-4])


def remainder(path):
    totalFile  = len(os.listdir(path))
    
    return totalFile 
    
threshold = 20000   
mappings =  {0:'ACTIONS/jump',1:"ACTIONS/left",2:"ACTIONS/right",3:"ACTIONS/noAction",4:"ACTIONS/roll"}
class ImageViewer(App):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        # PTH =  "/media/grey/24B4B6AE7953752A1/TrainingGround/SHOTS/"
        PTH = filedialog.askdirectory (title="SELECT FOLDER THAT HOUSES FRAMES CAPTURED")+"/"
        step1 = [i for i in os.listdir(PTH)] # Add your image paths here
        
        #sorted_names = sorted(step1, key=extract_number)
        sorted_files = sorted(step1, key=lambda f: int(re.search(r'-(\d+)\.jpg$', f).group(1)))
        self.images =  [PTH+file for file in sorted_files]
        try:
            
            index = self.images.index(last_seen)
            
            self.current_image_index= index         
        except Exception as e:
            print(e)
            self.current_image_index = 0
            
            
        self.image = Image(source=self.images[self.current_image_index])
        self.layout = BoxLayout(orientation='vertical')
        
        # Add image to the layout and center it horizontally
        image_layout = BoxLayout(size_hint=(1, 0.8))
        image_layout.add_widget(self.image)
        self.layout.add_widget(image_layout)

        # Create a horizontal layout for buttons
        buttons_layout = BoxLayout(size_hint=(1, 0.1))

        self.prev = Button(text="PREV")
        self.prev.bind(on_press=self.prevBtn)
        buttons_layout.add_widget(self.prev)
        
        self.next = Button(text="NEXT")
        self.next.bind(on_press=self.nextBtn)
        buttons_layout.add_widget(self.next)
        
        

        # self.delete = Button(text="Delete")
        # self.delete.bind(on_press=self.onDelete)
        # buttons_layout.add_widget(self.delete)

        self.noAction = Button(text="NoAction")
        self.noAction.bind(on_press=self.Action)
        buttons_layout.add_widget(self.noAction)
        
        self.left_button = Button(text="Left")
        self.left_button.bind(on_press=self.move_left)
        buttons_layout.add_widget(self.left_button)

        self.right_button = Button(text="Right")
        self.right_button.bind(on_press=self.move_right)
        buttons_layout.add_widget(self.right_button)

        self.jump_button = Button(text="Jump")
        self.jump_button.bind(on_press=self.jump_image)
        buttons_layout.add_widget(self.jump_button)

        self.roll_button = Button(text="Roll")
        self.roll_button.bind(on_press=self.roll_images)
        buttons_layout.add_widget(self.roll_button)

        # Add buttons layout to the main layout
        self.layout.add_widget(buttons_layout)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        #print(f"Key pressed: {key} | Codepoint: {codepoint} | Modifiers: {modifiers}")

        if key == 32:
            #print("Space bar was pressed!")
            self.current_image_index+=1 
            if self.current_image_index > len(self.images)-1:
                self.current_image_index=len(self.images) -1
            self.image.source =  self.images[self.current_image_index]
            writeToFile(self.image.source)
        return False
        
        
    def onDelete(self, instance):
        os.remove(self.images[self.current_image_index])
        self.current_image_index +=1 
        self.image.source  =  self.images[self.current_image_index]
         
    def nextBtn(self, instance):
        
        self.current_image_index+=1 
        if self.current_image_index > len(self.images)-1:
            self.current_image_index=len(self.images) -1
        self.image.source =  self.images[self.current_image_index]
        writeToFile(self.image.source)
    
        
    def prevBtn(self, instance):
        
        self.current_image_index-=1 
        
        if self.current_image_index <1:
            self.current_image_index = 0
        self.image.source =  self.images[self.current_image_index]
        writeToFile(self.image.source)
            
            
    def Action(self, instance):
        sz =  remainder(mappings[3])
        if sz >=threshold:
            self.noAction.disabled=True 
       
        else:
            shutil.copy(self.image.source,mappings[3])
            self.current_image_index += 1 if self.current_image_index < len(self.images) else  self.current_image_index
            self.image.source = self.images[self.current_image_index]
        
            writeToFile(self.image.source)
        
            

    def move_left(self, instance):
        
        sz =  remainder(mappings[1])
        if sz >=threshold:
            self.left_button.disabled=True 
        else:
                
            shutil.copy(self.image.source,mappings[1])
            self.current_image_index += 1 if self.current_image_index < len(self.images) else  self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
        
    def move_right(self, instance):
        sz =  remainder(mappings[2])
        if sz >=threshold:
            self.right_button.disabled=True 
            
        else:
            
            shutil.copy(self.image.source,mappings[2])
            self.current_image_index += 1 if self.current_image_index < len(self.images) else  self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
        
    def jump_image(self, instance):
        sz =  remainder(mappings[0])
        if sz >=threshold:
            self.jump_button.disabled=True 
        else:
                
            shutil.copy(self.image.source,mappings[0])
            self.current_image_index += 1 if self.current_image_index < len(self.images) else  self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
# mappings =  {0:'ACTIONS/jump',1:"ACTIONS/left",2:"ACTIONS/right",3:"ACTIONS/noAction",4:"ACTIONS/roll"}
        
    def roll_images(self, instance):
        sz =  remainder(mappings[4])
        if sz >=threshold:
            self.roll_button.disabled=True 
        else:
            shutil.copy(self.image.source,mappings[4])
            self.current_image_index += 1 if self.current_image_index < len(self.images) else  self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
        
    def build(self):
        Window.size = (900, 700)  # set initial window size
        return self.layout


if __name__ == '__main__':
    ImageViewer().run()
