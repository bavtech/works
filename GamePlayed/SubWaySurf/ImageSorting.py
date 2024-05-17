from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
import os 
import shutil 



mappings =  {0:'ACTIONS/jump',1:"ACTIONS/left",2:"ACTIONS/right",3:"ACTIONS/noAction",4:"ACTIONS/roll"}

class ImageViewer(App):
    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(**kwargs)
        self.images = ["SHOTS/"+i for i in os.listdir("SHOTS")] # Add your image paths here
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


    def onDelete(self, instance):
        os.remove(self.images[self.current_image_index])
        self.current_image_index +=1 
        self.image.source  =  self.images[self.current_image_index]
         
    
    def Action(self, instance):
        shutil.move(self.image.source,mappings[3])
        self.current_image_index += 1
        self.image.source = self.images[self.current_image_index]

    def move_left(self, instance):
        
        shutil.move(self.image.source,mappings[1])
        self.current_image_index += 1
        self.image.source = self.images[self.current_image_index]

    def move_right(self, instance):
        shutil.move(self.image.source,mappings[2])
        self.current_image_index += 1
        self.image.source = self.images[self.current_image_index]

    def jump_image(self, instance):
        shutil.move(self.image.source,mappings[0])
        self.current_image_index += 1
        self.image.source = self.images[self.current_image_index]

    def roll_images(self, instance):
        shutil.move(self.image.source,mappings[4])
        self.current_image_index += 1
        self.image.source = self.images[self.current_image_index]

    def build(self):
        Window.size = (900, 700)  # set initial window size
        return self.layout


if __name__ == '__main__':
    ImageViewer().run()
