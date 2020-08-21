"""
"""
import hassapi as hass

class Presence(hass.Hass):

    def initialize(self):

        self.device_trackers = [
            # 'device_tracker.meta_naia',
            'device_tracker.meta_emilie',
            'device_tracker.meta_walden',
            'device_tracker.meta_kristina'
            ]

        for tracker in self.device_trackers:
            self.listen_state(self.adjust_home, tracker, old='home')

        # self.listen_state(self.occupancy, 'sensor.occupancy', new = 'Unoccupied')


    def occupancy(self, entity):

        who = ''

        if entity == 'device_tracker.meta_emilie':
            who = 'notify.ios_emilie_iphone_xr'
        elif entity == 'device_tracker.meta_walden':
            who = 'notify/home_aephir_bot'
        elif entity == 'device_tracker.meta_kristina':
            who = 'notify/ios_kristinas_iphone'

        # # if not occupied:
        # self.call_service('notify/home_aephir_bot', message='Huset er nu tomt.')
        #         # self.call_service("notify/ios_kristinas_iphone", message='Babe, du smuttede hjemmefra, huset er nu tomt.')
        # # self.adjust_home(entity)

    def adjust_home(self, entity, attribute, old, new, kwarg):

        who             = self.occupancy(entity)
        title           = 'The house is now empty!'
        message         = ''
        temp            = []

        friendly_name   =

        lights          = [
            'light.dining_room_lights',
            'light.conservatory_lights'
            ]

        lights_on       = ''
        for light in lights:
            if self.get_state(light) == 'on':
                temp.append(light)
        for light in self.friendly_name(temp):
            lights_on  += light + ', '
        lights_on       = lights_on[:-2]

        door_window     = [
            'binary_sensor.openclose_basement_entrance_door',
            'binary_sensor.openclose_bathroom_window',
            'binary_sensor.openclose_bedroom_window_1',
            'binary_sensor.openclose_conservatory_door',
            'binary_sensor.openclose_front_door',
            'binary_sensor.openclose_washing_room_window_1'
            ]

        open            = ''
        for opening in door_window:
            if self.get_state(opening) == 'on':
                temp.append(opening)
        for opening in self.friendly_name(temp):
            open       += opening + ', '
        open            = open[:-2]

        media_players   = [
            'media_player.conservatory_speaker',    # Cast, conservatory
            'media_player.sonos_play_5_1',          # SONOS, conservatory
            'media_player.living_room_speaker',     # Google Home, dining room
            'media_player.ue46es8005',              # TV, top floor main
            'media_player.ue55nu7475xxc',           # TV, Emilie's room
            'media_player.upstairs_living_room_tv', # Cast, top floor main
            'media_player.spotify'                  # Spotify
            ]

        playing         = ''
        for media_player in media_players:
            if self.get_state(media_player) == 'on':
                temp.append(media_player)
        for media_player in self.friendly_name(temp):
            playing    += media_player + ', '
        playing         = playing[:-2]

        switches        = [
            'switch.top_floor_media',               # Top floor media center
            'switch.switch',                        # Espresso machine
            # 'switch.shed_main_power',               # Shed power
            'switch.fountain'                       # Fountain
            ]

        on              = ''
        for switch in switches:
            if self.get_state(switch) == 'on':
                temp.append(switch)
        for switch in self.friendly_name(temp):
            on         += switch + ', '
        on              = on[:-2]

        for light in lights:
            self.turn_off(light)

        for entity in media_players:
            self.turn_off(entity)

        for entity in switches:
            self.turn_off(entity)

        message = 'You have left the ' + open ' open. Please go back and close them!\n\n' + 'I have turned off the following, that were left on:\n\n' + 'The ' + on + ', the ' + playing + ', the ' + lights_on + '.'

        if entity == 'device_tracker.meta_walden':
            self.call_service('notify/home_aephir_bot', title=title, message=message)
        elif entity == 'device_tracker.meta_kristina':
            self.call_service('notify/ios_kristinas_iphone', title=title, message=message)
        elif entity == 'device_tracker.meta_emilie':
            self.call_service('notify.ios_emilie_iphone_xr', title=title, message=message) # Maybe just 'notify.ios_emilie_iphone'? Need to check!!


    def friendly_name(self, list):

        friendly_list   = []

        for item in list:
            friendly_list.append(self.friendly_name(item))

        return friendly_list
