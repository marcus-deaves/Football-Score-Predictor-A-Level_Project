import Login_page
import PySimpleGUI as sg
import csv

y = Login_page.Login_page()

user_info_dict = []

with open("User_Information.csv", "r") as f:
    csv_reader=csv.DictReader(f)
    for row in csv_reader:
        user_info_dict.append(row)

current_user_info_dict = user_info_dict[y]
print(current_user_info_dict)
sg.theme("DarkAmber")

x = current_user_info_dict["Username"]

layout = [[sg.Text(f"Hello {x}")]]


window = sg.Window(title="Football Score Predicter", layout=layout, margins=(50, 50), element_justification="c", finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        quit()
