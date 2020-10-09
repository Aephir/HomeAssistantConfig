import hassapi as hass

class TextToSpeak(hass.Hass):

    def initialize(self):
        """
        Initialize and listen for opening s of security fences.
        """

        self.sensors = [
            'binary_sensor.baby_safety_dining_room'
            ]

        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])

        self.timer_downstairs = None

        self.volume = None

        for sensor in self.sensors:
            self.listen_state(self.timer_function, sensor)


    def timer_function(self, entity, attribute, old, new, kwargs):

        if self.now_is_between("07:00:00","20:30:00"):

            if new == 'on' and entity == 'binary_sensor.baby_safety_dining_room':
                self.timer_downstairs = self.run_in(self.speak, 8)
            elif new == 'off' and entity == 'binary_sensor.baby_safety_dining_room':
                self.timer_downstairs = self.cancel_timer(self.timer_downstairs)


    def button_click(self, event_name, data, kwargs):

        if data['id'] == self.args['id']: # Dimmer Switch 1
            if data['event'] == 3002: # Button 3 up
                self.timer_downstairs = self.cancel_timer(self.timer_downstairs)

    def speak(self, kwargs):

        # # Get current state of lights. Get both state and attributes
        # dining_room = self.get_state('light.dining_room_lights')

        # Get previous volume
        self.volume = self.get_state('media_player.dining_room_speaker', attribute='volume_level')

        # Speak the notification
        self.call_service("media_player/volume_set", entity_id="media_player.dining_room_speaker", volume_level=0.8)
        self.call_service("tts/google_translate_say", message="Hey motherfucker. Close the security fence", entity_id="media_player.dining_room_speaker")

        # self.listen_state(self.reset_volume, 'media_player.dining_room_speaker', new='idle', oneshot=True)
        self.listen_state(self.reset_volume, 'media_player.dining_room_speaker', new='idle')
        # self.call_service('media_player/volume_set', entity_id='media_player.dining_room_speaker', volume_level=volume)

        # Flash lights
        # Return to pre-flash state

    def reset_volume(self, entity, attribute, old, new, kwargs):

        if self.volume != None:
            self.call_service('media_player/volume_set', entity_id='media_player.dining_room_speaker', volume_level=self.volume)
