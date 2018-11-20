# Warn me if "enitiy" is left "on" for more than 45 minutes.
# Again if it is still on after 1 hour.
# After 1.5 hours, turn off and notify.

import appdaemon.plugins.hass.hassapi as hass
import datetime

class ApplianceStatus(hass.Hass):


    def initialize(self):
        # Sets the initial value to make sure self.starttime exists, and is the correct format.
        self.starttime = datetime.datetime.now()
        # Set this up to be our global timer. "None" means that it is not started at this point.
        self.timer = None
        # Runs "StartTimer" when "entity" state changes.
        self.listen_state(self.StartTimer,self.args["entity"])

        # Set global variables for script (from yaml file, so I won't have to write "self.args["XXX"]" each time, but can write self.XXX)
        self.start_after = self.args["start_after"]
        self.time_between_notifications = self.args["time_between_notifications"]
        self.end_after = self.args["end_after"]
        self.switch_off = self.args["switch_off"]
        self.text_on_for = self.args["text_on_for"]
        self.text_time_unit = self.args["text_time_unit"]
        self.text_off = self.args["text_off"]
        self.text_data_telegram_warning = self.args["text_data_telegram_warning"]
        self.text_data_telegram_auto_off = self.args["text_data_telegram_auto_off"]
        self.notify_who = self.args["notify_who"]


    def StartTimer(self, entity, attribute, old, new, kwargs):
        # Stop the timer if the "entity" is switched "off".
        if new == "off":
            self.cancel_timer(self.timer)
        else:
            # Notes the current time.
            self.starttime = datetime.datetime.now()
            # "self.run_in" returns what "self.SendNotification" returns, a "handler" that can be used to cancel_timer
            self.timer = self.run_in(self.SendNotification,self.start_after)


    def SendNotification(self, kwargs):
        # if self.timer is not None:
        # See how long since "entity" was turned on. Wouldn't this just be "start_after"?
        timediff = datetime.datetime.now() - self.starttime
        # Converts time to minutes.
        minutes = round(timediff.seconds/60)
        # As long as no more than "end_after" seconds has elapsed, continue:
        if timediff.seconds < self.end_after:
            # Send message, and log it.
            # self.call_service(self.args["notify_who"], message=self.args["text_on_for"] + str(minutes) + self.args["text_time_unit"], data={self.args["text_data_telegram_warning"]}))
            self.call_service(self.notify_who, message=self.text_on_for + str(minutes) + self.text_time_unit, data={self.text_data_telegram_warning})
            # self.log(self.args["text_on_for"] + str(minutes) + self.args["text_time_unit"])
            self.log(self.text_on_for + str(minutes) + self.text_time_unit)
            # After "time_between_notifications", re-run this same function (so "SendNotification" restarts itself; loops until "end_time" has passed)
            # Needs 'self.timer =', otherwise the timer cannot be cancelled back in the StartTimer function.
            self.timer = self.run_in(self.SendNotification,self.time_between_notifications)
        else:
            # Checks if "switch_off" is "True". I'm guessing so I can use this app and sometimes turn off the switch after X minutes, sometimes not?
            if self.switch_off:
                self.turn_off(self.args["entity"])
                switchofftext = self.text_off
                # switchofftext = self.args["text_off"]
            else:
                switchofftext = "."
            # self.call_service(self.args["notify_who"], message=(self.args["text_on_for"] + str(minutes) + self.args["text_time_unit"] + switchofftext, data={self.args["text_data_telegram_auto_off"]}))
            self.call_service(self.notify_who, message=self.text_on_for + str(minutes) + self.text_time_unit + switchofftext, data={self.text_data_telegram_auto_off})
            # self.log(self.args["text_on_for"] + str(minutes) + self.args["text_time_unit"] + switchoffftext,)
            self.log(self.text_on_for + str(minutes) + self.text_time_unit + switchoffftext,)
