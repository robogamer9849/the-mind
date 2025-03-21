# from client import *

import kivy 
from kivy.app import App 
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import socket

# Home Screen
class HomeScreen(Screen):
        def __init__(self, **kwargs):
                super(HomeScreen, self).__init__(**kwargs)
                mainBox = BoxLayout(orientation='vertical')
                buttonsBox = BoxLayout(orientation='horizontal')

                btnHost = Button(
                        text='host',
                        font_size="20sp",
                        background_color=(256, 0, 100, 1),
                        size=(32, 32))
                
                btnClient = BoxLayout(orientation='vertical')

                self.code_input = TextInput(hint_text='connect code', multiline=False)
        
                connect_button = Button(
                        text='client',
                        font_size="20sp",
                        background_color=(256, 0, 100, 1),
                        size=(32, 32))
        
                # Bind the button press to the callback function
                connect_button.bind(on_press=self.on_connect_press)
        
                btnClient.add_widget(connect_button)
                btnClient.add_widget(self.code_input)
        
                buttonsBox.add_widget(btnHost)
                buttonsBox.add_widget(btnClient)

                self.homeText = Label(text="you want to connect to a server (client) or be one (host)?")

                mainBox.add_widget(self.homeText)
                mainBox.add_widget(buttonsBox)
        
                self.add_widget(mainBox)

        def on_connect_press(self, instance):
                # This function will be called when the client button is pressed
                host = f'{self.code_input.text}'
                port = 6000
        
                try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                                client_socket.connect((host, port))  # Connect to the server
                                client_socket.sendall("give me".encode())
                                data = client_socket.recv(1024)  # Receive the response from the server
                                number = data.decode()
                                print(number)
                        
                                # Switch to the game screen and pass the number and socket
                                game_screen = self.manager.get_screen('game')
                                game_screen.set_number(number)
                                game_screen.set_connection(host, port)
                                self.manager.current = 'game'
                        
                except OSError as e:
                        print(f"Error: {e}, probably the code is incorrect or you are not on the same network, try again")
                        self.homeText.text = f"Connection error: {e}. Please try again."

# Game Screen
class GameScreen(Screen):
        def __init__(self, **kwargs):
                super(GameScreen, self).__init__(**kwargs)
                self.number = None
                self.host = None
                self.port = None
        
                self.layout = BoxLayout(orientation='vertical')
        
                self.number_label = Label(text="Your number: ", font_size="30sp")
                self.status_label = Label(text="Game in progress...", font_size="20sp")
        
                self.show_button = Button(
                text="SHOW",
                font_size="25sp",
                background_color=(0, 256, 0, 1),
                size_hint=(1, 0.3)
                )  
                self.show_button.bind(on_press=self.on_show_press)
        
                self.back_button = Button(
                text="Back to Home",
                font_size="18sp",
                background_color=(100, 0, 256, 1),
                size_hint=(1, 0.2)
                )
                self.back_button.bind(on_press=self.go_back)
        
                self.layout.add_widget(self.number_label)
                self.layout.add_widget(self.status_label)
                self.layout.add_widget(self.show_button)
                self.layout.add_widget(self.back_button)
        
                self.add_widget(self.layout)

        def set_number(self, number):
                self.number = number
                self.number_label.text = f"Your number: {self.number}"

        def set_connection(self, host, port):
                self.host = host
                self.port = port

        def on_show_press(self, instance):
                try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                                client_socket.connect((self.host, self.port))
                                client_socket.sendall("I showed".encode())
                                data = client_socket.recv(1024)
                                response = data.decode()
                                self.status_label.text = f"Result: {response}"
                except Exception as e:
                        self.status_label.text = f"Error: {e}"

        def go_back(self, instance):
                self.manager.current = 'home'

class home(App):
        def build(self):
                # Create the screen manager
                sm = ScreenManager()
        
                # Add the home screen
                home_screen = HomeScreen(name='home')
                sm.add_widget(home_screen)
        
                # Add the game screen
                game_screen = GameScreen(name='game')
                sm.add_widget(game_screen)
        
                return sm

if __name__ == "__main__":
        home().run()
