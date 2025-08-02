from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
import os 
import shutil 
from tkinter import filedialog 
import re
from pathlib import Path
import threading


def ensure_action_dirs_exist():
    required_dirs = [
        "ACTIONS/jump",
        "ACTIONS/left",
        "ACTIONS/right",
        "ACTIONS/noAction",
        "ACTIONS/roll"
    ]
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            
def load_necessary_files():
    global last_seen, Pic_Dir 
    
    #this would first create the Action folder in the current directory where the python script was run from
    ensure_action_dirs_exist() 
    try:
        with open("checkpoint.txt", 'r') as file:
            last_seen = file.readline().strip()
            
            Pic_Dir = os.path.dirname(last_seen)
            

    except FileNotFoundError:
        with open('checkpoint.txt', 'a') as file:
            pass
        Pic_Dir  =''           

def writeToFile(filename: str):
    with open("checkpoint.txt", 'w') as file:
        file.write(filename)
     
def extract_number(filename):
    return int(filename[:-4])

def attachCmd(cmd, filename, mapping):
    dirname = os.path.dirname(filename)
    fN = cmd + '_' + os.path.basename(filename)
    return os.path.join(mapping, fN)
    
def getFile(name: str):
    try:
        store = list(Path('ACTIONS').rglob(f'*{name}*'))
        return store
    except StopIteration as e:
        return False 

def delByPathName(name: list):
    name = Path(name).name
    files2delete = getFile(name)
    for title in files2delete:
        try:
            title.unlink()
        except FileNotFoundError as FNE:
            pass 

            
            
def remainder(path):
    totalFile = len(os.listdir(path))
    return totalFile 

def threaded_copy(src, dst):
    """Threaded function to copy files without blocking the UI"""
    try:
        shutil.copy(src, dst)
    except Exception as e:
        print(f"Error copying file: {e}")



class ImageViewer(App):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        PTH = filedialog.askdirectory(title="SELECT FOLDER THAT HOUSES FRAMES CAPTURED") + "/" if not Pic_Dir else Pic_Dir+'/'  # this mitigates selecting the picture folder everytime
        #print(PTH)
        step1 = [i for i in os.listdir(PTH)]        
        sorted_files = sorted(step1, key=lambda f: int(re.search(r'-(\d+)\.jpg$', f).group(1)))
        self.images = [PTH + file for file in sorted_files]
        
        try:
            index = self.images.index(last_seen)
            self.current_image_index = index         
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

        self.delete = Button(text="Delete")
        self.delete.bind(on_press=self.onDelete)
        buttons_layout.add_widget(self.delete)

        self.prev = Button(text="PREV")
        self.prev.bind(on_press=self.prevBtn)
        buttons_layout.add_widget(self.prev)
        
        self.next = Button(text="NEXT")
        self.next.bind(on_press=self.nextBtn)
        buttons_layout.add_widget(self.next)
        
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

        self.layout.add_widget(buttons_layout)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        sz = remainder(mappings[3])
        
        if key == 32:  # Space bar
            if sz >= threshold:
                self.noAction.disabled = True 
                self.current_image_index += 1 
                if self.current_image_index > len(self.images)-1:
                    self.current_image_index = len(self.images) -1
                self.image.source = self.images[self.current_image_index]
                writeToFile(self.image.source)
                return False
            else:
                temp_name = attachCmd('noAction', self.image.source, mappings[3])
                # Start a new thread for copying
                threading.Thread(target=threaded_copy, args=(self.image.source, temp_name)).start()
                self.current_image_index += 1 if self.current_image_index < len(self.images) else self.current_image_index
                self.image.source = self.images[self.current_image_index]
                writeToFile(self.image.source)
        
        if codepoint == 'm':
            self.current_image_index += 1 
            if self.current_image_index > len(self.images)-1:
                self.current_image_index = len(self.images) -1
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
        if codepoint == 'n':
            self.current_image_index -= 1 
            if self.current_image_index < 1:
                self.current_image_index = 0
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
       
    def onDelete(self, instance):
        delByPathName(self.image.source)
         
    def nextBtn(self, instance):
        self.current_image_index += 1 
        if self.current_image_index > len(self.images)-1:
            self.current_image_index = len(self.images) -1
        self.image.source = self.images[self.current_image_index]
        writeToFile(self.image.source)
    
    def prevBtn(self, instance):
        self.current_image_index -= 1 
        if self.current_image_index < 1:
            self.current_image_index = 0
        self.image.source = self.images[self.current_image_index]
        writeToFile(self.image.source)
            
    def Action(self, instance): 
        sz = remainder(mappings[3])
        if sz >= threshold:
            self.noAction.disabled = True 
        else:
            temp_name = attachCmd('noAction', self.image.source, mappings[3])
            delByPathName(self.image.source)
            # Start a new thread for copying
            threading.Thread(target=threaded_copy, args=(self.image.source, temp_name)).start()
            self.current_image_index += 1 if self.current_image_index < len(self.images) else self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)

    def move_left(self, instance):
        sz = remainder(mappings[1])
        if sz >= threshold:
            self.left_button.disabled = True 
        else:
            temp_name = attachCmd('left', self.image.source, mappings[1])
            delByPathName(self.image.source)
            # Start a new thread for copying
            threading.Thread(target=threaded_copy, args=(self.image.source, temp_name)).start()
            self.current_image_index += 1 if self.current_image_index < len(self.images) else self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
    def move_right(self, instance):
        sz = remainder(mappings[2])
        if sz >= threshold:
            self.right_button.disabled = True 
        else:
            delByPathName(self.image.source)
            temp_name = attachCmd('right', self.image.source, mappings[2])
            # Start a new thread for copying
            threading.Thread(target=threaded_copy, args=(self.image.source, temp_name)).start()
            self.current_image_index += 1 if self.current_image_index < len(self.images) else self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
    def jump_image(self, instance):
        sz = remainder(mappings[0])
        if sz >= threshold:
            self.jump_button.disabled = True 
        else:
            delByPathName(self.image.source)
            temp_name = attachCmd('jump', self.image.source, mappings[0])
            # Start a new thread for copying
            threading.Thread(target=threaded_copy, args=(self.image.source, temp_name)).start()
            self.current_image_index += 1 if self.current_image_index < len(self.images) else self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
    def roll_images(self, instance):
        sz = remainder(mappings[4])
        if sz >= threshold:
            self.roll_button.disabled = True 
        else:
            delByPathName(self.image.source)
            temp_name = attachCmd('roll', self.image.source, mappings[4])
            # Start a new thread for copying
            threading.Thread(target=threaded_copy, args=(self.image.source, temp_name)).start()
            self.current_image_index += 1 if self.current_image_index < len(self.images) else self.current_image_index
            self.image.source = self.images[self.current_image_index]
            writeToFile(self.image.source)
        
    def build(self):
        Window.size = (900, 700)  # set initial window size
        return self.layout

if __name__ == '__main__':
    #/media/amiltra/BACKUP/vid/video9-20071.jpg
    threshold = 70000  
    mappings = {0: 'ACTIONS/jump', 1: "ACTIONS/left", 2: "ACTIONS/right", 
            3: "ACTIONS/noAction", 4: "ACTIONS/roll"}
            
    ensure_action_dirs_exist()
    load_necessary_files()
    ImageViewer().run()
