import appdaemon.plugins.hass.hassapi as hass

# UNTESTED!

# Call with:
# triggeredEntity()
# Returns entidi_id, e.g. binary_sensor.presence_top_floor_bathroom

# Get Data from Automation Trigger
    def triggeredEntity(self):
        return data.get('entity_id')
