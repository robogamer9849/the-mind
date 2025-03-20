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
                background_color = (256, 0, 100, 1),
                size = (32, 32))
                
        btnClient = BoxLayout(orientation = 'vertical')

        self.code_input = TextInput(hint_text = 'connect code', multiline = False)
        
        connect_button = Button(
                text = 'client',
                font_size = "20sp",
                background_color = (256, 0, 100, 1),
                size = (32, 32))
        
        # Bind the button press to the callback function
        connect_button.bind(on_press=self.on_connect_press)
        
        btnClient.add_widget(connect_button)
        btnClient.add_widget(self.code_input)
        
        buttonsBox.add_widget(btnHost)
        buttonsBox.add_widget(btnClient)

        homeText = Label(text = "you want to connect to a server (client) or be one (host)?")

        mainBox.add_widget(homeText)
        mainBox.add_widget(buttonsBox)

        return mainBox

    def on_connect_press(self, instance):
        # This function will be called when the client button is pressed
        code = self.code_input.text
        thread = threading.Thread(target=start_client, args=(code,))
        thread.daemon = True
        thread.start()

home().run()
