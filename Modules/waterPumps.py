from gpiozero import OutputDevice

HP1_RELAY = Relay(12)
HP2_RELAY = Relay(16)
SECONDS_TO_WATER = 100


class Relay(OutputDevice):
    def __init__(self, pin):
        super(Relay, self).__init__(pin)

# Remember off and on are switched for the relay
HP1_RELAY = Relay(12)
HP2_RELAY = Relay(16)
SECONDS_TO_WATER = 100



# TODO: Turns all pumps off
def all_pumps_off():


    print('All pumps are off.')


# TODO: Turns all pumps on
def all_pumps_on():
    print('All pumps are on.')


# TODO: Turns all hydroponic pumps on
def hydroponics_on():
    HP1_RELAY.off()
    HP2_RELAY.off()
    print('All hydroponic pumps are on.')


# TODO: Turns all potted plants on
def potted_on():
    print('All potted pumps are on.')


# TODO: Turns all hydroponic pumps off
def hydroponics_off():
    HP1_RELAY.on()
    HP2_RELAY.on()
    print('All hydroponic pumps are off.')


# TODO: Turns all potted pumps off
def potted_off():
    print('All potted pumps are off.')


# TODO: Turns off a specific pump
def pump_off(int):
    print('Pump ' + int + ' was turned off.')


# TODO: Turns on a specific pump
def pump_on(int):
    print('Pump ' + int + ' was turned on.')
