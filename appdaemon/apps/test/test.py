# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass

class Test(hass.Hass):

    def initialize(self):

        self.listen_state(self.test_app, 'input_boolean.vacation_mode')

    def test_app(self, entity, attribute, old, new, kwargs):

        self.call_service('tts/google_translate_say', message='testing', entity_id='media_player.dining_room_speaker')
