#todo imports
from console import update_message_display, run_gui
import time
import threading

# Create a thread to start the console and wait 10 seconds for them to load
gui_thread = threading.Thread(target=run_gui)
gui_thread.start()
time.sleep(10)

update_message_display("hello")


#todo Run diagnostic on hardware

#todo User chooses what areas will have plants

#todo are there areas not being used? (yes set those areas to off)

#todo Check water and food level

#todo are they full? (no prompt user to fill and wait for completion)

#todo show user how to plant their seeds

# Open main loop
while True:
    continue
    #todo Check schedule configuration

    #todo is it time to water? (yes turn pumps on/keep on; no turn off)

    #todo is it time for light? (yes turn light on/keep on; no turn off)

    #todo Take picture of plants and sparse out each one specifically

    #todo Process images and get health percentage

    #todo Display health percentage to user

    #todo is health < 80%? (yes, send notification to user)

    #todo wait five minutes
