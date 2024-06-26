from gpiozero import OutputDevice

# 3rd relay to GPIO 20
# 4th relay to GPIO 21

class Relay(OutputDevice):
    def __init__(self, pin):
        super(Relay, self).__init__(pin)


# Set relays for each gpio pin
HP1_RELAY = OutputDevice(12,initial_value=None)
HP2_RELAY = OutputDevice(16,initial_value=None)
POT1_RELAY = OutputDevice(20,initial_value=None)
POT2_RELAY = OutputDevice(21,initial_value=None)
SECONDS_TO_WATER = 100


# Turns all pumps off
def all_pumps_off():
    hydroponics_off()
    potted_off()
    print('All pumps are off.')


# Turns all pumps on
def all_pumps_on():
    hydroponics_on()
    potted_on()
    print('All pumps are on.')


# Turns all hydroponic pumps on
def hydroponics_on():
    HP1_RELAY.off()
    HP2_RELAY.off()
    print('All hydroponic pumps are on.')


# Turns all potted plants on
def potted_on():
    POT1_RELAY.off()
    POT2_RELAY.off()
    print('All potted pumps are on.')


# Turns all hydroponic pumps off
def hydroponics_off():
    HP1_RELAY.on()
    HP2_RELAY.on()
    print('All hydroponic pumps are off.')


# Turns all potted pumps off
def potted_off():
    POT1_RELAY.on()
    POT2_RELAY.on()
    print('All potted pumps are off.')
