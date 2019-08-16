import appdaemon.plugins.hass.hassapi as has
from datetime import datetime

class Alarm(hass.Hass):

    def initialize(self):

        alarm = ["alarm_control_panel.house"]

        self.listen_state(self.alarm, alarm, new='triggered')



    def alarm(self, entity, attribute, old, new, kwargs):

        time = datetime.now().strftime("%H:%M")

        self.call_service('notify/home_aephir_bot', message='Alarm was triggered at ' + time + '.')
        self.call_service("notify/ios_kristinas_iphone", message='Alarm was triggered at ' + time + '.')

        # self.sound_alarm_on()

        # self.run_in(callback, 120, random_start = -60, **kwargs)


    def sound_alarm_on(self):

        media_players = [
            'media_player.conservatory_speaker',
            'media_player.living_room_speaker',
            'media_player.sonos_play_5_1'
            ]

        for media_player in media_players:

            self.call_service("media_player.volume_set", attributes = {"entity_id":media_player,"volume_level": "0.1"})
            self.call_service("media_player.play_media", attributes = {"entity_id":media_player,"media_content_id": "http://192.168.0.100:8123/local/audio/siren.mp3"})


    # def sound_alarm_off(self, entity, attribute, old, new, kwargs):
