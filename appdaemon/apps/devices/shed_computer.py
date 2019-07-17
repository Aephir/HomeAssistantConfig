import appdaemon.plugins.hass.hassapi as hass

class Computer:

    def initialize(self):

        self.listen_state(self.powerOffComputer, "MODE_CHANGE") # Can I use "MODE_CHANGE", new="pc_off"?

    def powerOffComputer(self, entity, attribute, old, new, kwargs):

        request.get('curl -k (url of links from step 4)') # Get correct url. If a secret, put in shell command, and use:
        # self.call_service('shell_command.power_off_shed_pc')