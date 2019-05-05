import appdaemon.plugins.hass.hassapi as hass

class DetectNetworkedDevices(hass.Hass):

    """
    If RPi running HASS.io for Miflora sensors disappears (ping sensor, pinging every 5 minutes).
    Power cycle by switching off WeMo, then switching on 5 seconds later.
    """

    def initialize(self):

        self.listen_state(self.hassioUnreachable,self.args["ping_sensor"], new='off', duration=self.args["duration"])


    def hassioUnreachable(self, entity, attribute, old, new, kwargs):

        self.turn_off(self.args["switch"])
        self.run_in(self.turn_on(self.args["switch"]), 5)
