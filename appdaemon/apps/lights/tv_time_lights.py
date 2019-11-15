# Dim lights for movie nights

import appdaemon.plugins.hass.hassapi as hass


class MotionClass(hass.Hass):

    def initialize(self):

        self.tv = [
            'media_player.ue46es8005', # Old Samsung TV
            'media_player.conservatory_tv' # Chromecast
            ]

        self.motionSensors = [
            'binary_sensor.presence_conservatory', # Conservatory
            'binary_sensor.conservatory_motion_sensor_aeotec' # Conservatory 2
            ]

        for entity in self.tv:
            self.listen_state(self.dimLights, entity)

    def dimLights(self, entity, attribute, old, new, kwargs):

        sensor_1_state = self.get_state('media_player.ue46es8005') == 'on' # Old Samsung TV
        sensor_2_state = self.get_state('media_player.conservatory_tv') == 'playing' # Chromecast

        ## Update "movie_night" with real entity_id once applicable. ##
        movie_night = False # self.isOn("media_player.tv_room_tv") # Are we using the TV lounge?

        if any([sensor_1_state, sensor_2_state]):
            if self.get_state('light.conservatory_lights') == 'on':
                self.turn_off('light.conservatory_reading')
                self.turn_on('light.conservatory_couch',brightness=15,kelvin=2200)
        #     else:
        #         self.turn_on("light.basement_hallway",brightness=75,kelvin=2200)
        #
        # elif not all([sensor_1_state, sensor_2_state, sensor_3_state, sensor_4_state]):
        #     self.turn_off("light.basement_hallway")
