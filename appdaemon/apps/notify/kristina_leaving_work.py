import hassapi as hass

class Notify(hass.Hass):

    def initialize(self):

        self.listen_state(self.notify, 'device_tracker.meta_kristina', new='away')

    def notify(self, entity, attribute, old, new, kwargs):

        if old == 'work':

            self.call_service("notify/ios_kristinas_iphone", title='Kaffe', message='Husk Kaffe!!')
