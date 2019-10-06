import appdaemon.plugins.hass.hassapi as hass

# Call with argument "entity_id", e.g.:
# isOn("light.dining_room_lights")
# returns True or False

    # This is a quick test to return a true/false if the device is on.
    def isOn(entity_id):
        return self.get_state(entity_id) == 'on'
