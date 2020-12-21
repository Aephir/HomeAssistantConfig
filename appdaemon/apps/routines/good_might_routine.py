import hassapi as hass

class Routines(hass.Hass):

    def initialize(self):

        if 'event' in self.args:
            self.listen_event(self.button_click, self.args['event'])


    def button_click(self, event_name, data, kwargs):
        """
        data['event'] is in the format 'X00Y', where:

            1000    = Button down
            1002    = Button up
            1001    = Button hold
            1003    = Button hold up
        """
