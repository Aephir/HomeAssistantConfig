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
                self.timer_downstairs = self.run_in(self.speak, 8)
                # self.speak()
            elif new == 'off' and entity == 'binary_sensor.baby_safety_dining_room':
                self.timer_downstairs = self.cancel_timer(self.timer_downstairs)

    def speak(self, kwargs):

        # # Get current state of lights. Get both state and attributes
        # dining_room = self.get_state('light.dining_room_lights')

        # Speak the notification
        self.call_service('tts/google_translate_say', message="Hey motherfucker. Close the security fence", entity_id='media_player.dining_room_speaker') # media_player.living_room_speaker

        # Flash lights


        # Return to pre-flash state
