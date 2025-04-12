from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.clock import Clock
import threading
import socket
import random

PORT = 6000
HOST = '0.0.0.0'
max_number = 100
nums = {}

HELP_TEXT = "🎮 THE MIND - WHERE TELEPATHY MEETS FUN! 🎮\n..."


# --- Server Logic (same as in your Toga code) ---

def find_code():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def handle_client(conn, addr, num):
    print(f"Connection with {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            if message == 'give me':
                if addr[0] not in nums:
                    nums[addr[0]] = num
                conn.sendall(f"{nums[addr[0]]}".encode())
            elif message == 'I showed':
                min_num = min(nums.values())
                if nums[addr[0]] == min_num:
                    conn.sendall("You won!".encode())
                    nums.pop(addr[0])
                else:
                    conn.sendall("You lost!".encode())
                    nums.clear()
    except Exception as e:
        print("Client error:", e)
    finally:
        conn.close()

def start_server():
    print("Server starting...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr, random.randint(1, max_number)), daemon=True).start()


# --- Kivy Screens ---

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="🎮 Ready to play?\nLet's go! 🎲", font_size='24sp'))

        self.code_input = TextInput(hint_text="Enter host IP")
        connect_btn = Button(text="Connect", on_press=self.connect_to_server)
        host_btn = Button(text="Host Game", on_press=self.start_host)

        layout.add_widget(self.code_input)
        layout.add_widget(connect_btn)
        layout.add_widget(host_btn)
        layout.add_widget(Label(text=HELP_TEXT, font_size='14sp'))

        self.add_widget(layout)

    def connect_to_server(self, instance):
        host = self.code_input.text.strip()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, PORT))
                s.sendall("give me".encode())
                data = s.recv(1024)
                number = data.decode()
                self.manager.get_screen('game').set_number(number, host)
                self.manager.current = 'game'
        except Exception as e:
            print("Error connecting:", e)

    def start_host(self, instance):
        threading.Thread(target=start_server, daemon=True).start()
        Clock.schedule_once(lambda dt: self.auto_connect_client(), 1)

    def auto_connect_client(self):
        host = find_code()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, PORT))
                s.sendall("give me".encode())
                number = s.recv(1024).decode()
                self.manager.get_screen('game').set_number(number, host)
                self.manager.current = 'game'
        except Exception as e:
            print("Auto-connect failed:", e)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.number = ""
        self.host = ""

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.number_label = Label(text="Your number: ", font_size='24sp')
        self.status_label = Label(text="Game in progress...", font_size='18sp')
        self.show_button = Button(text="SHOW", on_press=self.show_number)

        self.layout.add_widget(self.number_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.show_button)
        self.add_widget(self.layout)

    def set_number(self, number, host):
        self.number = number
        self.host = host
        self.number_label.text = f"Your number: {number}"
        self.status_label.text = "Game in progress..."

    def show_number(self, instance):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, PORT))
                s.sendall("I showed".encode())
                result = s.recv(1024).decode()
                self.status_label.text = result
        except Exception as e:
            self.status_label.text = f"Error: {e}"

class TheMindApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    TheMindApp().run()
