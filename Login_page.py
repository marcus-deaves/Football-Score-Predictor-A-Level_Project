import PySimpleGUI as sg

sg.theme("DarkAmber")

layout = [
    [sg.Text("LOGIN OR REGISTER", font=("Bold", 25), pad=(30, 50), auto_size_text=True)],
    [sg.Text("Username:", pad=30), sg.In(s=30)],
    [sg.Text("Password:", pad=(30, None)), sg.In(password_char="*", s=30, pad=(7))],
    [sg.Button(button_text="Login", pad=(50, 40), size=10),
     sg.Button(button_text="Register", pad=(70, 40), size=10)]
]

window = sg.Window(title="Football Score Predictor", layout=layout, margins=(50, 75))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

window.close()
