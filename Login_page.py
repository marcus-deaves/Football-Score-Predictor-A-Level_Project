import PySimpleGUI as sg
import re
import bcrypt
from Private_info import salt
import csv


def password_checker(password1, password2):  # checks password validity and returns True or False
    if password1 != password2:
        sg.popup(custom_text="Passwords do not match", any_key_closes=True)

    else:  # using https://www.geeksforgeeks.org/python-program-check-validity-password/ I constructed a way of
        # checking passwords for containing special characters, uppercase letters, lowercase letters and numbers.
        password = password1
        flag = 0
        while True:
            if len(password) < 8:
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[_@$!£%^&*()?:<>,./'~}{]", password):
                flag = -1
                break
            elif re.search("\s", password):
                flag = -1
                break
            else:
                flag = 0
                return True

        if flag == -1:
            sg.popup(custom_text="Password invalid, Please include at least 8 characters, upper and lowercase "
                                 "letters, numbers and special characters.")
            return False


def handle_user_info(user_info_raw):  # handles user information from registration page.
    # puts most of it in a text file and hashes the password for security
    user_info = user_info_raw
    # hashing algorithm
    password = user_info[5].encode("utf-8")
    hashed_password = bcrypt.hashpw(password, salt)
    print(hashed_password)
    user_info[5] = str(hashed_password)
    print(user_info)

    with open("User_Information.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(user_info)

    Login_page()


def registration_page():  # Allows the user to register and outputs user info and passwords to relevant functions
    sg.theme("DarkAmber")

    layout = [[sg.Text("First Name:"), sg.In(size=30, pad=(10, 5), key=1)],
              [sg.Text("Last Name:"), sg.In(size=30, pad=(10, 5), key=2)],
              [sg.Text("Username:"), sg.In(size=30, pad=(10, 5), key=3)],
              [sg.Text("Favourite Team"), sg.In(size=30, pad=(10, 5), key=4)],
              [sg.Text("Email:"), sg.In(size=30, pad=(10, 5), key=5)],
              [sg.Text("Password:"), sg.In(size=30, pad=(10, 5), key=6, password_char="·")],
              [sg.Text("Confirm password"), sg.In(size=30, pad=(10, 5), key=7, password_char="·")],
              [sg.Button("Register", size=20, pad=(100, 10))]
              ]
    window = sg.Window(title="Registration Page", layout=layout, margins=(50, 50), element_justification="r",
                       element_padding=(10, 5))
    while True:
        event, values = window.read()

        if event == "Register":
            user_info = []
            for x in range(1, 7):
                user_info.append(values[x])
            if password_checker(values[6], values[7]):
                window.close()
                handle_user_info(user_info)
            else:
                pass

        if event == sg.WIN_CLOSED:
            break

    window.close()


def Login_page():
    sg.theme("DarkAmber")

    layout = [
        [sg.Text("LOGIN OR REGISTER", font=("Bold", 25), auto_size_text=True)],
        [sg.Text("Username:"), sg.In(s=30)],
        [sg.Text("Password:"), sg.In(password_char="*", s=30, pad=8)],
        [sg.Button(button_text="Login", size=10),
         sg.Button(button_text="Register", size=10)]
    ]

    window = sg.Window(title="Football Score Predictor", layout=layout, margins=(50, 75), element_justification="c")

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Login":

            user_info_dict = []

            username = values[0]
            password = values[1]

            password = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(password, salt)

            with open('User_Information.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    user_info_dict.append(row)
            success = False
            for x in range(len(user_info_dict)):
                if user_info_dict[x]["Username"] == username and user_info_dict[x]["password"] == str(hashed_password):
                    sg.popup(custom_text="Login Successful", any_key_closes=True)
                    success = True
                    window.close()
            if not success:
                sg.popup(custom_text="Username or Password invalid. Please try again or register an account.")

        if event == "Register":
            window.close()
            registration_page()

    window.close()
