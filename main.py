import socket
import threading
import random
from finder import *  # ensure finder.py is available
from kivy.clock import Clock

# Global list to hold client numbers
nums = []

# Server IP and Port configuration
HOST = '0.0.0.0'
PORT = 6000

# --- Server Functions ---

def handle_client(conn, addr, num):
    print(f"Connection established with {addr}.")
    nums.append(num)
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                if num in nums:
                    nums.remove(num)
                break

            message = data.decode()
            print(f"Received from {addr}: {message}")

            if message == 'give me':
                conn.sendall(f"{num}".encode())

            elif message == 'I showed':
                # Remove the number so that only the first "I showed" counts.
                if num in nums:
                    nums.remove(num)
                current_min = get_min(nums)
                print("Remaining numbers:", nums, "Current min:", current_min)
                # If no numbers remain (or this was the smallest), then this client wins.
                if current_min is None or num < current_min:
                    conn.sendall("you are right\n".encode())
                else:
                    conn.sendall("you lose\n".encode())

        except ConnectionResetError:
            print(f"Client {addr} has disconnected.")
            if num in nums:
                nums.remove(num)
            break
    conn.close()
    print(f"Connection with {addr} closed.")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}...")
        code = find_code()
        print("Connect code:", code)
        
        while True:
            conn, addr = server_socket.accept()  # Accept a client connection
            thread = threading.Thread(target=handle_client, args=(conn, addr, random.randint(1, 1000000)))
            thread.start()
            print(f"Active connections: {threading.active_count() - 1}")


# --- Kivy UI Code ---

import kivy 
from kivy.app import App 
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

# Home Screen: choose between host (server) or client
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        mainBox = BoxLayout(orientation='vertical')
        buttonsBox = BoxLayout(orientation='horizontal')

        # Host button navigates to ServerScreen
        btnHost = Button(
            text='host',
            font_size="20sp",
            background_color=(1, 0, 0, 1),
            size_hint=(0.5, 1)
        )
        btnHost.bind(on_press=self.go_to_server)

        # Client side elements
        clientBox = BoxLayout(orientation='vertical')
        self.code_input = TextInput(hint_text='connect code (IP)', multiline=False)
        connect_button = Button(
            text='client',
            font_size="20sp",
            background_color=(0, 1, 0, 1),
            size_hint=(1, 0.5)
        )
        connect_button.bind(on_press=self.on_connect_press)
        clientBox.add_widget(connect_button)
        clientBox.add_widget(self.code_input)

        buttonsBox.add_widget(btnHost)
        buttonsBox.add_widget(clientBox)

        self.homeText = Label(text="Do you want to host (server) or connect as a client?",
                              font_size="18sp")

        mainBox.add_widget(self.homeText)
        mainBox.add_widget(buttonsBox)

        self.add_widget(mainBox)

    def go_to_server(self, instance):
        self.manager.current = 'server'

    def on_connect_press(self, instance):
        # Get the code as host (IP address) for client connection
        host = self.code_input.text.strip()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, PORT))
                client_socket.sendall("give me".encode())
                data = client_socket.recv(1024)
                number = data.decode()
                print("Received number:", number)
            
            # Switch to GameScreen and pass the number and connection details
            game_screen = self.manager.get_screen('game')
            game_screen.set_number(number)
            game_screen.set_connection(host, PORT)
            self.manager.current = 'game'
        
        except OSError as e:
            print(f"Error: {e}. Check the IP or network.")
            self.homeText.text = f"Error: {e}. Check the IP or network."

# Server Screen: start and monitor the server and auto-connect client on same device
class ServerScreen(Screen):
    def __init__(self, **kwargs):
        super(ServerScreen, self).__init__(**kwargs)
        self.server_thread = None

        layout = BoxLayout(orientation='vertical')
        self.info_label = Label(text="Press 'Start Server' to begin hosting", font_size="18sp")
        start_button = Button(text="Start Server", font_size="20sp", background_color=(0, 0, 1, 1))
        start_button.bind(on_press=self.start_server_thread)

        back_button = Button(text="Back to Home", font_size="18sp", background_color=(0.5, 0.5, 0.5, 1))
        back_button.bind(on_press=self.go_back)

        layout.add_widget(self.info_label)
        layout.add_widget(start_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def start_server_thread(self, instance):
        # Get the connect code (for example, from finder.find_code())
        code = find_code()
        self.info_label.text = f"Server started!\nConnect code: {code}\nListening on port {PORT}"
        # Start the server in a separate thread if not already running.
        if not self.server_thread or not self.server_thread.is_alive():
            self.server_thread = threading.Thread(target=start_server, daemon=True)
            self.server_thread.start()
        else:
            self.info_label.text = "Server already running."
        # Auto-connect as client after a short delay (using localhost)
        Clock.schedule_once(self.auto_connect_client, 1)

    def auto_connect_client(self, dt):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((f"{find_code()}", PORT))
                client_socket.sendall("give me".encode())
                data = client_socket.recv(1024)
                number = data.decode()
                print("Auto-connected; received number:", number)
            game_screen = self.manager.get_screen('game')
            game_screen.set_number(number)
            game_screen.set_connection(f"{find_code()}", PORT)
            self.manager.current = 'game'
        except Exception as e:
            self.info_label.text = f"Auto-connect failed: {e}"

    def go_back(self, instance):
        self.manager.current = 'home'

# Game Screen: used for the gameplay after connecting as a client
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.number = None
        self.host = None
        self.port = None

        self.layout = BoxLayout(orientation='vertical')
        self.layout.clear_widgets()
        self.number_label = Label(text="Your number: ", font_size="30sp")
        self.status_label = Label(text="Game in progress...", font_size="20sp")
        self.show_button = Button(
            text="SHOW",
            font_size="25sp",
            background_color=(0, 1, 0, 1),
            size_hint=(1, 0.3)
        )
        self.show_button.bind(on_press=self.on_show_press)
        self.back_button = Button(
            text="Back to Home",
            font_size="18sp",
            background_color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, 0.2)
        )
        self.back_button.bind(on_press=self.go_back)

        self.layout.add_widget(self.number_label)
        self.layout.add_widget(self.status_label)
        # self.layout.add_widget(self.show_button)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def set_number(self, number):
        self.number = number
        self.number_label.text = f"Your number: {self.number}"

    def set_connection(self, host, port):
        self.host = host
        self.port = port
        self.ipLable = Label(text=f"code:{self.host}")
        self.layout.add_widget(self.ipLable)


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

class HomeApp(App):
    def build(self):
        # Create the screen manager and add screens
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ServerScreen(name='server'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    HomeApp().run()
