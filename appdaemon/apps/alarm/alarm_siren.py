# Play siren on repeat for 15 minutes

import appdaemon.plugins.hass.hassapi as hass
import datetime

## Alarm triggered. Notify us, sound alarm tts, flash lights.

class AlarmTriggered(hass.Hass):

    # Initialize
    def initialize(self):

        self.listen_event(self.soundSiren, event = "MODE_CHANGE", mode: 'siren')

    # Has the alarm been activated/triggered? Return True/False
    def soundSiren(self, entity_id):
        timestamp = datetime.datetime.now().strftime('%M')
        while (datetime.datetime.now().strftime('%M') - timestamp) < 15:
            self.call_service("media_player.volume_set", attributes = {"entity_id":"media_player.living_room_speaker","volume_level": "0.1"})
            self.call_service("media_player.play_media", attributes = {"entity_id":"media_player.living_room_speaker","media_content_id": "http://192.168.0.100:8123/local/audio/siren.mp3"})
