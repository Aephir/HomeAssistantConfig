import appdaemon.plugins.hass.hassapi as hass
import datetime

## Alarm triggered. Notify us, sound alarm tts, flash lights.

class AlarmClock(hass.Hass):

    # Initialize
    def initialize(self):

        self.listen_event(self.soundSiren, event = "MODE_CHANGE", mode: 'siren')

    # Has the alarm been activated/triggered? Return True/False
    def soundAlarm(self, entity_id):
        f = x
