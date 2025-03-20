import kivy 
from kivy.app import App 
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class home(App):
    def build(self):
        mainBox = BoxLayout(orientation = 'vertical')
        buttonsBox = BoxLayout(orientation = 'horizontal')

        btnHost = Button(
                text = 'host',
                font_size = "20sp",
                background_color = (256, 0 ,100 ,1),
                size = (32, 32),)
        btnClient = Button(
            text = 'client',
            font_size = "20sp",
            background_color = (0, 256 ,100 ,1),
            size = (32, 32),)

        buttonsBox.add_widget(btnHost)
        buttonsBox.add_widget(btnClient)

        homeText = Label(text = "you want to connetct to a server (client) or be one (host)?")

        mainBox.add_widget(homeText)
        mainBox.add_widget(buttonsBox)

        return mainBox 

fristapp().run()