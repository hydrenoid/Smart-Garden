import PySimpleGUI as sg
import time
import threading
import datetime
import waterPumps as pumps
import threading

class System:
    def __init__(self):
        schedule = read_schedule('../Config/Schedule.txt')
        curr_time = datetime.datetime.now()
        self.hydroponic_pump = 0
        self.hp_start_time = curr_time.minute
        self.potted_start_time = schedule[2]
        self.potted_end_time = schedule[3]
        self.pot_pump = 0
        self.lights = 0
        self.force_off = 1

    # if within 30 min turn on, otherwise turn off, time needs to just me minutes
    def check_hp_time(self, time):
        if self.hp_start_time < time: # TODO: fix this, needs to read from current time
            self.hydroponic_pump = 1
        else:
            self.hydroponic_pump = 0

    # TODO: needs time in full HH:MM format
    def check_pot_time(self, time):
        if self.potted_start_time < time < self.potted_end_time:
            self.pot_pump = 1
        else:
            self.pot_pump = 0

    def pumps_switch(self):
        if self.force_off == 1:
            # TODO: Turn all pumps off, then break out of method
            pumps.hydroponics_off()
            pumps.all_pumps_off()
            return

        if(self.hydroponic_pump == 1):
            #TODO: Turn hp pumps on
            pumps.hydroponics_on()
        else:
            #TODO: Turn hp pumps off
            pumps.hydroponics_off()

        if(self.pot_pump == 1):
            #TODO: turn pot pumps on
            pumps.potted_on()
        else:
            #TODO: turn pot pumps off
            pumps.potted_off()


    def toggle_force(self):
        if self.force_off == 1:
            self.force_off = 0
        else:
            self.force_off = 1



# Read the schedule from the file into an array (Light Start = 0, Light End = 1, Water Start = 2, Water End = 3)
def read_schedule(filename):
    try:
        with open(filename, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()

            return file_contents.split()

    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        file_contents = ['08:00', '20:00', '08:00', '20:00']
        return file_contents
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        file_contents = ['08:00', '20:00', '08:00', '20:00']
        return file_contents


# Save the new schedule to the config file, newSchedule needs to be in array format of strings
def save_schedule(filename, newSchedule):
    try:
        # Open the file in write mode to overwrite the content
        with open(filename, 'w') as file:
            # Write each word/element on its own line
            for line in newSchedule:
                file.write(line + '\n')
        print("Content modified and saved successfully!")
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

system = System()

schedule = read_schedule('../Config/Schedule.txt')

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

layout_window4 = [
    [sg.Text('Lights Schedule.txt')],
    [sg.Text('Start Time'), sg.InputText(schedule[0], size=(10, 1), key='-LIGHTS_START-'),
     sg.Button('+', key='-LIGHTS_START_INC'), sg.Button('-', key='-LIGHTS_START_DEC')],
    [sg.Text('End Time  '), sg.InputText(schedule[1], size=(10, 1), key='-LIGHTS_END-'),
     sg.Button('+', key='-LIGHTS_END_INC'), sg.Button('-', key='-LIGHTS_END_DEC')],
    [sg.Text('')],
    [sg.Text('Water Pumps Schedule.txt')],
    [sg.Text('Start Time'), sg.InputText(schedule[2], size=(10, 1), key='-PUMPS_START-'),
     sg.Button('+', key='-PUMPS_START_INC'), sg.Button('-', key='-PUMPS_START_DEC')],
    [sg.Text('End Time  '), sg.InputText(schedule[3], size=(10, 1), key='-PUMPS_END-'),
     sg.Button('+', key='-PUMPS_END_INC'), sg.Button('-', key='-PUMPS_END_DEC')],
    [sg.Button('Save'), sg.Button('Exit')]
]


# Function to update the message display
def update_message_display(message):
    window3['-MESSAGES-'].print(message)



# Create the windows
window1 = sg.Window('Percentage Value', layout_window1, finalize=True)
window2 = sg.Window('Control Panel', layout_window2)
window3 = sg.Window('Message Display', layout_window3)
window4 = sg.Window('Garden Control Panel', layout_window4)


while True:

    now = datetime.datetime.now()

    # Get current time
    current_time = datetime.datetime.now()

    # Format the time as a string in 24-hour format (HH:MM)
    time_string = current_time.strftime("%H:%M")

    # Extracting the hour and minute
    current_hour = now.hour
    current_minute = now.minute

    print(current_hour, ' : ', current_minute)

    # check if hp pumps should be running
    system.check_hp_time(current_minute)

    # check if pot plants should be on
    system.check_pot_time(time_string)

    # turn pumps on if they should be, or off if they should be off
    system.pumps_switch()




    event, values = window1.read(timeout=100)  # Timeout for non-blocking read

    # Check if the window is closed
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    # Update the percentage value (random value for demonstration)
    percentage_value = 75  # Example value (you can replace this with your actual value)
    window1['-PERCENTAGE-'].update(f'{percentage_value}%', text_color='green' if percentage_value > 80 else 'red')

    # Handle events for window 2
    event2, values2 = window2.read(timeout=100)  # Timeout for non-blocking read
    if event2 == sg.WINDOW_CLOSED:
        break
    elif event2 == 'Stop Pumps':
        system.toggle_force()
        print('Pumps switched')  # Example action (replace with your code)
        update_message_display('Pumps switched')  # Update message display when pumps are stopped
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

    event4, values4 = window4.read(timeout=100)

    if event4 == sg.WIN_CLOSED or event4 == 'Exit':
        break
    # Handling button clicks to increment and decrement times
    if event4 == '-LIGHTS_START_INC':
        current_time = values4['-LIGHTS_START-'] if values4['-LIGHTS_START-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) + 1) % 60).zfill(2)
        hour = str((int(hour) + (int(minute) == 0)) % 24).zfill(2)
        window4['-LIGHTS_START-'].update(f"{hour}:{minute}")
    elif event4 == '-LIGHTS_START_DEC':
        current_time = values4['-LIGHTS_START-'] if values4['-LIGHTS_START-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) - 1) % 60).zfill(2)
        hour = str((int(hour) - (int(minute) == 59)) % 24).zfill(2)
        window4['-LIGHTS_START-'].update(f"{hour}:{minute}")
    elif event4 == '-LIGHTS_END_INC':
        current_time = values4['-LIGHTS_END-'] if values4['-LIGHTS_END-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) + 1) % 60).zfill(2)
        hour = str((int(hour) + (int(minute) == 0)) % 24).zfill(2)
        window4['-LIGHTS_END-'].update(f"{hour}:{minute}")
    elif event4 == '-LIGHTS_END_DEC':
        current_time = values4['-LIGHTS_END-'] if values4['-LIGHTS_END-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) - 1) % 60).zfill(2)
        hour = str((int(hour) - (int(minute) == 59)) % 24).zfill(2)
        window4['-LIGHTS_END-'].update(f"{hour}:{minute}")
    elif event4 == '-PUMPS_START_INC':
        current_time = values4['-PUMPS_START-'] if values4['-PUMPS_START-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) + 1) % 60).zfill(2)
        hour = str((int(hour) + (int(minute) == 0)) % 24).zfill(2)
        window4['-PUMPS_START-'].update(f"{hour}:{minute}")
    elif event4 == '-PUMPS_START_DEC':
        current_time = values4['-PUMPS_START-'] if values4['-PUMPS_START-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) - 1) % 60).zfill(2)
        hour = str((int(hour) - (int(minute) == 59)) % 24).zfill(2)
        window4['-PUMPS_START-'].update(f"{hour}:{minute}")
    elif event4 == '-PUMPS_END_INC':
        current_time = values4['-PUMPS_END-'] if values4['-PUMPS_END-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) + 1) % 60).zfill(2)
        hour = str((int(hour) + (int(minute) == 0)) % 24).zfill(2)
        window4['-PUMPS_END-'].update(f"{hour}:{minute}")
    elif event4 == '-PUMPS_END_DEC':
        current_time = values4['-PUMPS_END-'] if values4['-PUMPS_END-'] else '00:00'
        hour, minute = current_time.split(':')
        minute = str((int(minute) - 1) % 60).zfill(2)
        hour = str((int(hour) - (int(minute) == 59)) % 24).zfill(2)
        window4['-PUMPS_END-'].update(f"{hour}:{minute}")

    # Handle saving the schedule
    elif event4 == 'Save':
        lights_start = values4['-LIGHTS_START-']
        lights_end = values4['-LIGHTS_END-']
        pumps_start = values4['-PUMPS_START-']
        pumps_end = values4['-PUMPS_END-']
        print(f"Lights Schedule.txt: {lights_start} - {lights_end}")
        print(f"Water Pumps Schedule.txt: {pumps_start} - {pumps_end}")
        new_schedule = [lights_start, lights_end, pumps_start, pumps_end]
        save_schedule('../Config/Schedule.txt', new_schedule)

# Close the windows
window1.close()
window2.close()
window3.close()
window4.close()
