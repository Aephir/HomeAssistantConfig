"""
"""
import appdaemon.plugins.hass.hassapi as hass

class Presence(hass.Hass):

    def initialize(self):

        self.device_trackers = [
            # 'device_tracker.meta_naia',
            # 'device_tracker.meta_emilie',
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        # for tracker in self.device_trackers:
        #     self.listen_state(self.occupancy, tracker, new='off')

        self.listen_state(self.occupancy, 'sensor.occupancy', new = 'Unoccupied')


    def occupancy(self, entity, attribute, old, new, kwargs):

        # occupied = None
        #
        # for tracker in self.device_trackers:
        #     if self.get_state(tracker) == 'off':
        #         occupied = False
        #     else:
        #         occupied = True
        #         break
        #
        # self.log("Unoccupied")

        # if not occupied:
        self.call_service('notify/home_aephir_bot', message='Huset er nu tomt.')
                # self.call_service("notify/ios_kristinas_iphone", message='Babe, du smuttede hjemmefra, huset er nu tomt.')
        # self.adjust_home(entity)

    def adjust_home(self, entity):

        lights          = 'light.all_lights'
        media_players   = [
            'media_player.conservatory_speaker',    # Cast, conservatory
            'media_player.sonos_play_5_1',          # SONOS, conservatory
            'media_player.living_room_speaker',     # Google Home, dining room
            'media_player.ue46es8005',              # TV, top floor main
            'media_player.ue55nu7475xxc',           # TV, Emilie's room
            'media_player.upstairs_living_room_tv', # Cast, top floor main
            'media_player.spotify'                  # Spotify
            ]
        switches        = [
            'switch.top_floor_media',               # Top floor media center
            'switch.switch',                        # Espresso machine
            # 'switch.shed_main_power',               # Shed power
            'switch.fountain'                       # Fountain
            ]

        self.turn_off(lights)

        for entity in media_players:
            self.turn_off(entity)

        for entity in switches:
            self.turn_off(entity)
