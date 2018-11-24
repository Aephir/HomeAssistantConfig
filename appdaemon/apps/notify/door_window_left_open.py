# Notify if we forget to close door/window if it is cold, windy, or there is high chance of significant amounth
# Use self.set_state("sensor.notify_message", state="blabla") from any other app
# See https://community.home-assistant.io/t/a-notify-function-that-does-more-then-just-1-notify/32483

import appdaemon.plugins.hass.hassapi as hass


class Notify(hass.Hass):

    def initialize(self):

        # Door and window sensors to monitor.
        self.sensor_ids = [
        'binary_sensor.door_window_sensor_158d0002286a78', # Bathroom Window
        'binary_sensor.door_window_sensor_158d00022b3b66', # Basement Door
        'binary_sensor.door_window_sensor_158d00022d0917', # Front Door
        'binary_sensor.door_window_sensor_158d000234dc7b', # Conservatory Door
        'binary_sensor.neo_coolcam_doorwindow_detector_sensor' # Shed Door
        ]

        # Temperature, precipitation and wind conditions to monitor.
        self.weather_ids = [
        'sensor.dark_sky_temperature', # Monitor temperature drops.
        'sensor.dark_sky_precip', # Monitor procipitation type.
        'sensor.dark_sky_wind_speed' # Monitor wind speed.
        ]

        # Set this to "None" initially.
        self.open = None

        # Run when state changes.
        for entity in self.sensor_ids:
            self.listen_state(self.MessageDoorWindow, entity)

        for entity in self.weather_ids:
            self.listen_state(self.MessageWeather, entity)


    def MessageDoorWindow (self, entity, attribute, old, new, kwargs):
        # Set to "None" if door/window closes. Otherwise, run function.
        if new == 'off':
            self.open = None
        else:
            self.run_in(self.SendNoticationDoorWindow, 900)

    def MessageWeather (self, entity, attribute, old, new, kwargs):
        #
        if entity == "sensor.dark_sky_temperature":
            if float(self.get_state("sensor.dark_sky_temperature")) > 18.0:
                self.open = None
            else:
                self.SendNoticationWeather(type="temperature")
        elif entity == "sensor.dark_sky_precip":
            if float(self.get_state("sensor.dark_sky_precip")) == "unknown":
                self.open = None
            elif float(self.get_state("sensor.dark_sky_precip_intensity")) > 4.0 and float(self.get_state("sensor.dark_sky_precip_probability")) > 25.0:
                self.SendNoticationWeather(type="precipitation")
        elif entity == "sensor.dark_sky_wind_speed":
            if float(self.get_state("sensor.dark_sky_wind_speed")) < 14.0:
                self.open = None
            else:
                self.SendNoticationWeather(type="wind")

    def isOpen(self, entity_id):
        return self.get_state(entity_id) == 'on'

    def ListOfOpen(self):
        count = 0
        for entity in self.sensor_ids:
            if self.IsOpen(entity):
                door_window_list += entity
                count += 1
        door_window_list.replace("binary_sensor.door_window_sensor_158d0002286a78","bathroom window, ")
        door_window_list.replace("binary_sensor.door_window_sensor_158d00022b3b66","basement door, ")
        door_window_list.replace("binary_sensor.door_window_sensor_158d00022d0917","front door, ")
        door_window_list.replace("binary_sensor.door_window_sensor_158d000234dc7b","conservatory door, ")
        door_window_list.replace("binary_sensor.neo_coolcam_doorwindow_detector_sensor","shed door, ")
        door_window_list = door_window_list[:-2]
        if count == 1:
            door_window_list += " is"
        else:
            door_window_list += " are"
        if count != 0:
            return door_window_list
        else:
            return None


    def SendNoticationDoorWindow(self, entity, attribute, old, new, kwargs):

        # Variables to get from HASS sensors.
        outdoor_temp = float(self.get_state("sensor.dark_sky_temperature"))
        precip_type = self.get_state("sensor.dark_sky_precip")
        precip_intensity = float(self.get_state("sensor.dark_sky_precip_intensity"))
        precip_probability = float(self.get_state("sensor.dark_sky_precip_probability"))
        precip_problem = ''
        wind_speed = float(self.get_state("sensor.dark_sky_wind_speed"))
        door_window = ''

        # Define a new friendly name for the sensor that triggered.
        if entity == "binary_sensor.door_window_sensor_158d0002286a78":
            door_window = "bathroom window"
        elif entity == "binary_sensor.door_window_sensor_158d00022b3b66":
            door_window = "basement door"
        elif entity == "binary_sensor.door_window_sensor_158d00022d0917":
            door_window = "front door"
        elif entity == "binary_sensor.door_window_sensor_158d000234dc7b":
            door_window = "conservatory door"
        elif entity == "binary_sensor.neo_coolcam_doorwindow_detector_sensor":
            door_window = "shed door"

        # If any type of precipitation is expected, make "True".
        if precip_type != "unknown" and precip_intensity > 4.0 and precip_probability > 25.0:
            precip_problem = True

        # Notify based on which sensor and what potential problem.
        if precip_problem:
            self.call_service("notify/home_aephir_bot", message="It might " + precip_type + ", and the " + door_window + "has been open for 15 minutes. Please close it!")
            # self.call_service("notify/ios_kristinas_iphone", message="It might " precip_type ", and the " + door_window + "has been open for 15 minutes. Please close it!")
        elif outdoor_temp < 18.0: # Temperature 18°C. Is this appropriate?
            self.call_service("notify/home_aephir_bot", message="It is cold, and the " + door_window + "has been open for 15 minutes. Please close it!")
            # self.call_service("notify/ios_kristinas_iphone", message="It is cold, and the " + door_window + "has been open for 15 minutes. Please close it!")
        elif wind_speed > 14.0: # Wind speed 14 m/s. Is this appropriate?
            self.call_service("notify/home_aephir_bot", message="It is windy, and the " + door_window + "has been open for 15 minutes. Please close it!")
            # self.call_service("notify/ios_kristinas_iphone", message="It is windy, and the " + door_window + "has been open for 15 minutes. Please close it!")


    def SendNoticationWeather(self, entity, attribute, old, new, type, kwargs):

        # Variables to get from HASS sensors.
        precip_type = self.get_state("sensor.dark_sky_precip")
        precip_problem = ''
        wind_speed = float(self.get_state("sensor.dark_sky_wind_speed"))
        door_window_list = self.ListOfOpen()

        # Define a new friendly name for the sensor that triggered.
        if door_window_list != None:
            if type == "temperature":
                self.call_service("notify/home_aephir_bot", message="It is getting cold outside, and the " + door_window_list + " still open.")
                # self.call_service("notify/ios_kristinas_iphone", message="It is getting cold outside, and the " + door_window_list + " still open.")
            elif type == "precipitation":
                self.call_service("notify/home_aephir_bot", message="It might start to" + precip_type + ", and the " + door_window_list + " still open.")
                # self.call_service("notify/ios_kristinas_iphone", message="It might start to" precip_type ", and the " + door_window_list + " still open.")
            elif type == "wind":
                self.call_service("notify/home_aephir_bot", message="It it getting windy, and the " + door_window_list + " still open.")
                # self.call_service("notify/ios_kristinas_iphone", message="It it getting windy, and the " + door_window_list + " still open.")
