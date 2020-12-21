import hassapi as hass

class Presence(hass.Hass):

    def initialize(self):

        self.set_boolean('', '', '', '', '')

        self.device_trackers = ['device_tracker.meta_naia', 'device_tracker.meta_emilie']

        for device in self.device_trackers:
            self.listen_state(self.set_boolean, device)

    def set_boolean(self, entity, attribute, old, new, kwargs):

        naia    = self.get_state('device_tracker.meta_naia') == 'Home'
        emilie  = self.get_state('device_tracker.meta_emilie') == 'Home'
        who_is_home = ''

        if naia and emilie:
            who_is_home = 'Naia & Emilie'
        elif naia:
            who_is_home = 'Naia'
        elif emilie:
            who_is_home = 'Emilie'
        else:
            who_is_home = 'Maybe Luca?'


        if naia or emilie:
            self.set_state('input_boolean.kids_home', state = 'on', attributes={'who_is_home': who_is_home})
        else:
            self.set_state('input_boolean.kids_home', state = 'off', attributes={'who_is_home': who_is_home})
