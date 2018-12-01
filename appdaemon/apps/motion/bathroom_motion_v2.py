import appdaemon.plugins.hass.hassapi as hass
import datetime
import time

def toInt(inString):
    try:
        return int(inString)
    except ValueError:
        return 0

class MotionClass(hass.Hass):
    def initialize(self):
        # list of lights that are turned on by the motion.
        self.light_entity_ids = [
            'light.bathroom' ]

        # list of motion sensors that trigger the automation.
        self.motion_entity_ids = [
            'binary_sensor.motion_sensor_158d000210ca6e',
            'binary_sensor.motion_sensor_158d000236a22f' ]

        # list of illumination sensors
        self.illumination_sensors = [
            'sensor.illumination_158d000236a22f' ]

        # create the listeners for each motion sensor.
        for entity in self.motion_entity_ids:
            self.listen_state(self.motion_trigger, entity) # motion sensors

        for entity in self.illumination_sensors:
            self.listen_state(self.illumination_trigger, entity) # motion sensors

    def isOn(self, entity_id):
        return self.get_state(entity_id) == 'on'

    def lights_on(self, **kwargs):
        """ iterates through lights and turns them on"""
        for entity in self.light_entity_ids:
            self.turn_on(entity, **kwargs)

    def lights_off(self):
        """ iterates through lights and turns them off"""
        for entity in self.light_entity_ids:
            self.turn_off(entity)

    def lights_on_time(self, illumination):
        if self.now_is_between("07:00:00", "21:00:00") and illumination < 50:
            self.turn_on_light_entities(brightness=255, kelvin=2700)
        elif self.now_is_between("21:00:00", "22:00:00") and illumination < 50:
            if any([ isOn(entity_id) for entity_id in ['light.dining_table_lights', 'light.conservatory_lights']):
                self.lights_on(brightness=255, kelvin=2200)
            else:
                self.lights_on(brightness=255, rgb_color=[255,0,0])
        else: # everything between 22 and 7
            if isOn('light.dining_table_lights'):
                self.lights_on(brightness=255, kelvin=2200)
            else:
                self.lights_on(brightness=255, rgb_color=[255,0,0])

    def illumination_trigger(self, entity, attribute, old, new, kwargs):
        # using any again...
        if any([ isOn(entity_id) for entity_id in self.motion_entity_ids ]):  # if we have motion
            # get the illumination from OTHER sensors (not the triggered).
            illumination_list = [ toInt(self.get_state(entity_id)) for entity_id in self.illumination_sensors if entity != entity_id ]

            # get the darkest part of the room.
            illumination = min(illumination_list + [ toInt(new) ] ) if illumination_list else toInt(new)

            # turn on our lights depending on the time of day.
            self.lights_on_time(illumination)
        else: # there isn't motion.
            self.lights_off()

    def motion_trigger(self, entity, attribute, old, new, kwargs):
        # this will be triggered by
        if new == 'on': # if we got motion.
            # get illumination from our illumination sensors.
            illumination = max([ toInt(self.get_state(entity_id)) for entity_id in self.illumination_sensors ])
            # turn on our lights depending on the time of day.
            self.lights_on_time(illumination)
        else: # we got no motion.
            self.lights_off()
