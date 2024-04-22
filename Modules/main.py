import PySimpleGUI as sg
import datetime
import waterPumps as pumps
import growLights as lights
import camera as camera


# This class handles variables for the system, specifically lights and pumps, checking if they should be on or not
class System:
    def __init__(self):
        schedule = read_schedule('../Config/Schedule.txt')
        curr_time = datetime.datetime.now()
        self.hydroponic_pump = 0  # if hydroponic pumps should be on (1 or 0)
        self.hp_start_time = curr_time.minute  # time the hydroponics should turn on
        self.potted_start_time = schedule[2]  # time the potted pumps should turn on
        self.potted_end_time = schedule[3]  # time the potted pumps should turn off
        self.pot_pump = 0  # if potted pumps should be on (1 or 0)
        self.light_start = schedule[0]  # time the lights should turn on
        self.light_end = schedule[1]  # time the lights should turn off
        self.lights = 0  # if the lights should be on (1 or 0)
        self.pump_force_off = 1  # forces all pumps off if 1
        self.light_force_off = 1  # forces all lights off if 1
        self.picture_file = '../Images/Originals/resized.png'  # file path to display in console

    # turn lights on if they need to be or turn them off
    def lights_switch(self):
        if self.lights:
            print('Turned lights on')
            lights.lights_on()
        else:
            print('Turned lights off')
            lights.lights_off()

    # Turn lights on if within schedule, otherwise turn them off
    def check_lights(self, time):
        print('Current time -- ' + time)
        print('Start light -- ' + self.light_start)
        print('End light -- ' + self.light_end)
        if self.light_force_off:
            self.lights = 0
            return
        elif self.light_start < time < self.light_end:
            self.lights = 1
            print('Lights should be on')
        else:
            self.lights = 0
            print('Lights should be off')

    # if within 30 min turn on, otherwise turn off, time needs to just be minutes
    def check_hp_time(self, time):
        print(time)
        print(self.hp_start_time)
        elapsed_time = (time - self.hp_start_time) % 60
        print(elapsed_time)
        if elapsed_time < 30:
            self.hydroponic_pump = 1
        else:
            self.hydroponic_pump = 0

    # needs time in full HH:MM format
    def check_pot_time(self, time):
        if self.potted_start_time < time < self.potted_end_time:
            self.pot_pump = 1
        else:
            self.pot_pump = 0

    # turns pumps on or off as set by time and force off
    def pumps_switch(self):
        if self.pump_force_off == 1:
            # Turn all pumps off, then break out of method
            pumps.hydroponics_off()
            pumps.all_pumps_off()
            return

        if self.hydroponic_pump == 1:
            # Turn hp pumps on
            pumps.hydroponics_on()
        else:
            # Turn hp pumps off
            pumps.hydroponics_off()

        if self.pot_pump == 1:
            # Turn pot pumps on
            pumps.potted_on()
        else:
            # turn pot pumps off
            pumps.potted_off()

    # toggles the force pump off variable
    def toggle_force(self):
        if self.pump_force_off == 1:
            self.pump_force_off = 0
            return 0
        else:
            self.pump_force_off = 1
            return 1

    # Toggles the force lights off variable
    def toggle_lights(self):
        if self.light_force_off == 1:
            self.light_force_off = 0
            return 0
        else:
            self.light_force_off = 1
            return 1


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
def save_schedule(filename, new_schedule):
    try:
        # Open the file in write mode to overwrite the content
        with open(filename, 'w') as file:
            # Write each word/element on its own line
            for line in new_schedule:
                file.write(line + '\n')
        print("Content modified and saved successfully!")
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Initialize the system
system = System()

# read the schedule into the system
schedule = read_schedule('../Config/Schedule.txt')

# Define the layout for the windows

# Window 1: Display percentage value
layout_window1 = [
    [sg.Image(key="-IMAGE-", filename=system.picture_file)]
]

# Window 2: Buttons to stop pumps and turn off lights
layout_window2 = [
    [sg.Button('Toggle All Pumps', key="-BUTTON1-", button_color=('white', 'blue'))],
    [sg.Button('Hydroponic Pumps On')],
    [sg.Button('Toggle Lights', key="-BUTTON3-", button_color=('white', 'blue'))],
    [sg.Button('Take Picture')]
]

# Window 3: Display messages
layout_window3 = [
    [sg.Multiline('', size=(30, 10), key='-MESSAGES-')],
    [sg.InputText(key='-INPUT-', size=(20, 1)), sg.Button('Send')]
]

# Window 4: Sets schedule
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
window1 = sg.Window('NDVI Image', layout_window1, location=(0,0), finalize=True)
window2 = sg.Window('Control Panel', layout_window2, size=(600, 200), location=(0, 330))
window3 = sg.Window('Message Display', layout_window3, size=(300, 200), location=(640, 375))
window4 = sg.Window('Schedule Panel', layout_window4, size=(300, 275), location=(630, 0))


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

    # check if lights should be on
    system.check_lights(time_string)

    # check if pot plants should be on
    system.check_pot_time(time_string)

    # turn pumps on if they should be, or off if they should be off
    system.pumps_switch()

    # turn lights on if they should be on, or turn them off
    system.lights_switch()

    event, values = window1.read(timeout=100)  # Timeout for non-blocking read

    # Check if the window is closed
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    # Update the percentage value (random value for demonstration)
    # percentage_value = 75  # Example value (you can replace this with your actual value)
    # window1['-PERCENTAGE-'].update(f'{percentage_value}%', text_color='green' if percentage_value > 80 else 'red')

    # Handle events for window 2
    event2, values2 = window2.read(timeout=100)  # Timeout for non-blocking read
    if event2 == sg.WINDOW_CLOSED:
        break
    elif event2 == 'Toggle All Pumps':
        toggle = system.toggle_force()

        if toggle:
            print('All pumps are now enabled')
            window2["-BUTTON1-"].update(button_color=('black', 'yellow'))
            update_message_display('All pumps are now enabled')
        else:
            print('All pumps are now disabled')
            update_message_display('All pumps are now disabled')
            window2["-BUTTON1-"].update(button_color=('white', 'blue'))

    elif event2 == 'Toggle Lights':
        toggle = system.toggle_lights()

        if toggle:
            print('Lights are on')
            window2["-BUTTON3-"].update(button_color=('black', 'yellow'))
            update_message_display('Lights are on')
        else:
            print('Lights are off')
            update_message_display('Lights are off')
            window2["-BUTTON3-"].update(button_color=('white', 'blue'))

    elif event2 == 'Hydroponic Pumps On':
        print('Hydroponic Pumps Turned On')
        system.hp_start_time = current_minute
        update_message_display('Hydroponic Pumps On')
    elif event2 == 'Take Picture':
        print('Taking picture')
        camera.take_picture()
        update_message_display('Picture taken')
        window1["-IMAGE-"].update(filename=system.picture_file)

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
