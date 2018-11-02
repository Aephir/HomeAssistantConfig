import appdaemon.plugins.hass.hassapi as hass

# Call with argument "entity_id", e.g.:
# isState("light.dining_room_lights")
# returns on or off

    # This is a quick test to return a true/false if the device is on.
    def stateIs(entity_id):
        if self.get_state(entity_id) == 'on':
            return "on"
        elif self.get_state(entity_id) == 'off':
            return "off"
