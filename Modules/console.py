import PySimpleGUI as sg
import threading

# Define the layout for the windows

# Window 1: Display percentage value
layout_window1 = [
    [sg.Text('Percentage Value:', size=(15, 1), justification='center')],
    [sg.Text('', size=(15, 1), justification='center', key='-PERCENTAGE-')]
]

# Window 2: Buttons to stop pumps and turn off lights
layout_window2 = [
    [sg.Button('Stop Pumps')],
    [sg.Button('Turn Off Lights')]
]

# Window 3: Display messages
layout_window3 = [
    [sg.Multiline('', size=(30, 10), key='-MESSAGES-')],
    [sg.InputText(key='-INPUT-', size=(20, 1)), sg.Button('Send')]
]


# Function to update the message display
def update_message_display(message):
    window3['-MESSAGES-'].print(message)


def run_gui():
    global window3
    # Create the windows
    window1 = sg.Window('Percentage Value', layout_window1, finalize=True)
    window2 = sg.Window('Control Panel', layout_window2)
    window3 = sg.Window('Message Display', layout_window3)

    # Event loop to handle interactions with the windows
    while True:
        event, values = window1.read(timeout=100)  # Timeout for non-blocking read

        # Check if the window is closed
        if event == sg.WINDOW_CLOSED:
            break

        # Update the percentage value (random value for demonstration)
        percentage_value = 85  # Example value (you can replace this with your actual value)
        window1['-PERCENTAGE-'].update(f'{percentage_value}%', text_color='green' if percentage_value > 80 else 'red')

        # Handle events for window 2
        event2, values2 = window2.read(timeout=100)  # Timeout for non-blocking read
        if event2 == sg.WINDOW_CLOSED:
            break
        elif event2 == 'Stop Pumps':
            print('Pumps stopped')  # Example action (replace with your code)
            update_message_display('Pumps stopped')  # Update message display when pumps are stopped
        elif event2 == 'Turn Off Lights':
            print('Lights turned off')  # Example action (replace with your code)
            update_message_display('Lights turned off')  # Update message display when lights are turned off

        # Handle events for window 3
        event3, values3 = window3.read(timeout=100)  # Timeout for non-blocking read
        if event3 == sg.WINDOW_CLOSED:
            break
        elif event3 == 'Send':
            message = values3['-INPUT-']
            window3['-INPUT-'].update('')  # Clear the input field after sending
            update_message_display(message)  # Update message display when a new message is sent

    # Close the windows
    window1.close()
    window2.close()
    window3.close()

# Create a thread to run the GUI
# gui_thread = threading.Thread(target=run_gui)
# gui_thread.start()

# Main program continues to run concurrently with the GUI
# You can put your main program logic here
# This part of the code will run independently of the GUI

