# todo imports
from console import update_message_display, run_gui
import time
import threading
import datetime
import waterPumps as pumps

# Create a thread to start the console and wait 10 seconds for them to load
gui_thread = threading.Thread(target=run_gui)
gui_thread.start()
time.sleep(10)

update_message_display("hello")


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




# todo Run diagnostic on hardware

# todo User chooses what areas will have plants

# todo are there areas not being used? (yes set those areas to off)

# todo Check water and food level

# todo are they full? (no prompt user to fill and wait for completion)

# todo show user how to plant their seeds

# Open main loop
while True:
    system = System()
    now = datetime.datetime.now()

    # Get current time
    current_time = datetime.now()

    # Format the time as a string in 24-hour format (HH:MM)
    time_string = current_time.strftime("%H:%M")

    # Extracting the hour and minute
    current_hour = now.hour
    current_minute = now.minute

    print(current_hour, ' : ', current_minute)

    # check if hp pumps should be running
    system.check_hp_time(current_minute)

    # check if pot plants should be on
    system.check_pot_time()

    # turn pumps on if they should be, or off if they should be off
    system.pumps_switch()


    # todo Take picture of plants and sparse out each one specifically

    # todo Process images and get health percentage

    # todo Update health percentage on display

    # todo is health < 80%? (yes, send notification to user)

    # wait 1 second
    time.sleep(1)