import hassapi as hass

class TextToSpeak(hass.Hass):

    def initialize(self):
        """
        Initialize and listen for opening s of security fences.
        """

        self.sensors = [
            'binary_sensor.baby_safety_dining_room'
            ]

        self.timer_downstairs = None

        for sensor in self.sensors:
            self.listen_state(self.timer_function, sensor)


    def timer_function(self, entity, attribute, old, new, kwargs):

        if self.now_is_between("07:00:00","20:30:00"):

            if new == 'on' and entity == 'binary_sensor.baby_safety_dining_room':
                self.timer_downstairs = self.run_in(self.speak, 10)
                # self.speak()
            elif new == 'off' and entity == 'binary_sensor.baby_safety_dining_room':
                self.timer_downstairs = self.cancel_timer(self.timer_downstairs)

    def speak(self, kwargs):
        #
        # self.call_service('tts/google_translate_say', message="Hey motherfucker", entity_id='media_player.conservatory_speaker') # media_player.living_room_speaker
        # self.call_service('tts/google_translate_say', message="Don't kill the baby", entity_id='media_player.conservatory_speaker') # media_player.living_room_speaker
        # self.call_service('tts/google_translate_say', message="Close the security fence please", entity_id='media_player.conservatory_speaker') # media_player.living_room_speaker

        self.call_service('tts/google_translate_say', message="Hey motherfucker, close the security fence", entity_id='media_player.conservatory_speaker') # media_player.living_room_speaker
