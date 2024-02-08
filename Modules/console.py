
import PySimpleGUI as sg

# Define the window's contents
layout = [[sg.Text("What's your name?")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Window Title', layout)
window2 = sg.Window('Window Title2', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    event2, values2 = window2.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()
window2.close()

#TODO: This method initializes the windows to be displayed and shows them
def initialize_windows():
    True


#TODO: This method closes the windows
def close_windows():
    True


#TODO: This method receives a notification with inputs ("be skipped?" bool, "Title" string, "Description" string)
def check_notifications(skippable, title, description):
    True


#TODO: This method removes a certain notification.
def rem_notification(int):
    True