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
                background_color = (1, 0, 0.39, 1),  # Fixed color values (0-1 range)
                size_hint = (1, 1))
                
        btnClient = BoxLayout(orientation = 'vertical')

        self.code_input = TextInput(hint_text = 'connect code', multiline = False)
        
        client_button = Button(
                text = 'client',
                font_size = "20sp",
                background_color = (1, 0, 0.39, 1),  # Fixed color values
                size_hint = (1, 1))
        
        # Set the callback properly
        client_button.bind(on_press=self.start_client)
        
        btnClient.add_widget(client_button)
        btnClient.add_widget(self.code_input)
        
        buttonsBox.add_widget(btnHost)
        buttonsBox.add_widget(btnClient)

        homeText = Label(text = "Do you want to connect to a server (client) or be one (host)?")

        mainBox.add_widget(homeText)
        mainBox.add_widget(buttonsBox)

        return mainBox

    def start_client(self, instance):
        # Get the code from the TextInput when the button is pressed
        code = self.code_input.text
        # Start the client in a separate thread
        thread = threading.Thread(target=start_client, args=(code,))
        thread.daemon = True  # Make thread exit when main program exits
        thread.start()

home().run()
