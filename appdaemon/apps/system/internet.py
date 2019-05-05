import appdaemon.plugins.hass.hassapi as hass
import os

class SystemClass(hass.Hass):

    """
    Listen for whether access to router disappears.
    Listen for input_boolean to cancel the automatic reboot.
    """

    def initialize(self):

        self.listen_state(self.internetOut,'binary_sensor.ping_router', new='off', duration=600)
        self.listen_state(self.cancelTimer,'input_boolean.no_internet_reboot')

        self.timer = None


    def internetOut(self, entity, attribute, old, new, kwargs):
        """
        Reboot computer if no internet.
        Use input_boolean to decide if it should or not.
        Toggle input_boolean.
        """

        if self.get_state('input_boolean.no_internet_reboot') == 'on':
            self.timer = self.run_in(self.reboot, 90)


    def cancelTimer(self, entity, attribute, old, new, kwargs):
        """
        Cancel timer if I can still access Home Assistant via home network.
        """

        if new == 'off':
            self.cancel_timer(self.timer)


    def reboot(self):

        os.system("shutdown /r /t 1") # AppDaemon needs to be running as root. How to do that?
