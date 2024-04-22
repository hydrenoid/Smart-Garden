from gpiozero import OutputDevice


class Relay(OutputDevice):
    def __init__(self, pin):
        super(Relay, self).__init__(pin)


LIGHTS_RELAY = OutputDevice(26,initial_value=None)

# Turns lights relay on
def lights_on():
    LIGHTS_RELAY.on()

# Turns lights relay off
def lights_off():
    LIGHTS_RELAY.off()