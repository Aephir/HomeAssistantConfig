import appdaemon.plugins.hass.hassapi as hass
import os

class SystemClass(hass.Hass):

    """
    Listen for whether access to router disappears.
    Run test at boot.
    """

    def initialize(self):

        self.listen_state(self.routerOut,'binary_sensor.ping_router', new='off', duration=600)
        self.routerOutInit()


    def routerOut(self, entity, attribute, old, new, kwargs):

        os.system("shutdown /r /t 1") # AppDaemon needs to be running as root. How to do that? == 'on':


    def routerOutInit(self):

        if self.get_state('binary_sensor.ping_router') == 'off':
            os.system("shutdown /r /t 1") # AppDaemon needs to be running as root. How to do that?
