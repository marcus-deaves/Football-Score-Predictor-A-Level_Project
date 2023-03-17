import Login_page
import PySimpleGUI as sg
import csv

Current_Player_Username = Login_page.Login_page()


class Main_Page():
    def __init__(self, Username):
        self.Username = Username

    def Layout_of_page(self):
        sg.theme_global("BlueMono")
        quick_user_info_layout = [
            [sg.Column(layout=[
                [sg.Text(text=self.Username)]
            ]), sg.Column(layout=[
                [sg.Text("Points")]
            ]), sg.Column(layout=[
                [sg.Text("global leaderboard")]
            ])]
        ]
        quick_user_info = [[sg.Frame(title="Quick Info", layout=quick_user_info_layout)]]
        whole_layout = [[sg.Column(quick_user_info), sg.Column([[sg.Text("marcusisfat")]])]]
        window = sg.Window(title="Football Score Predictor", layout=whole_layout, margins=(50, 50))
        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                quit()


Application = Main_Page(Current_Player_Username)
Application.Layout_of_page()
