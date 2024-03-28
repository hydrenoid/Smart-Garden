from gpiozero import OutputDevice


class Relay(OutputDevice):
    def __init__(self, pin):
        super(Relay, self).__init__(pin)


HP1_RELAY = Relay(12)
HP2_RELAY = Relay(16)
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


# TODO: Turns all potted plants on
def potted_on():
    print('All potted pumps are on.')


# Turns all hydroponic pumps off
def hydroponics_off():
    HP1_RELAY.on()
    HP2_RELAY.on()
    print('All hydroponic pumps are off.')


# TODO: Turns all potted pumps off
def potted_off():
    print('All potted pumps are off.')
