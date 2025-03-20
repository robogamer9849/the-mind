from client import *
import threading

import kivy 
from kivy.app import App 
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class home(App):
    def build(self):
        mainBox = BoxLayout(orientation = 'vertical')
        buttonsBox = BoxLayout(orientation = 'horizontal')

        btnHost = Button(
                text = 'host',
                font_size = "20sp",
                background_color = (256, 0 ,100 ,1),
                size = (32, 32),)
        btnClient = BoxLayout(orientation = 'vertical',)

        code = TextInput(hint_text = 'connect code', multiline = False)
        
        btnClient.add_widget(Button(
                text = 'client',
                font_size = "20sp",
                background_color = (256, 0 ,100 ,1),
                size = (32, 32),
                on_press = self.start_client(code = code.text)))
        
        btnClient.add_widget(code)
        

        buttonsBox.add_widget(btnHost)
        buttonsBox.add_widget(btnClient)

        homeText = Label(text = "you want to connetct to a server (client) or be one (host)?")

        mainBox.add_widget(homeText)
        mainBox.add_widget(buttonsBox)

        return mainBox

    def start_client(self, code):
        thread = threading.Thread(target=start_client, args=(code))

home().run()