# Warn me if "enitiy" is left "on" for too long.
# Warn again, until times out, then automatically turn off.

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


    def StartTimer(self, entity, attribute, old, new, kwargs):
        # Stop the timer if the "entity" is switched "off".
        if new == "off":
            self.cancel_timer(self.timer)
        else:
            # Notes the current time.
            self.starttime = datetime.datetime.now()
            # "self.run_in" returns what "self.SendNotification" returns, a "handler" that can be used to cancel_timer
            self.timer = self.run_in(self.SendNotification,self.args["start_after"])


    def SendNotification(self, kwargs):

        # See how long since "entity" was turned on. Convert to minutes.
        timediff = datetime.datetime.now() - self.starttime
        minutes = round(timediff.seconds/60)

        # Run until "end_after" seconds has elapsed:
        if timediff.seconds < self.args["end_after"]:
            # Send message, and log it.
            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " minutes", data={"inline_keyboard":"Turn Off:/espresso_off, I Know:/removekeyboard"})
            self.log("Espresso machine has been on for " + str(minutes) + " minutes")

            # After "time_between_notifications", re-run itself.
            self.timer = self.run_in(self.SendNotification,self.args["time_between_notifications"])
            # self.timer = self.run_in(self.ContinueTimer,self.args["time_between_notifications"])
        else:

            # Checks if "switch_off" is "True".
            if self.args["switch_off"]:
                self.turn_off(self.args["entity"])
                switchofftext = ", i turned it off."
            else:
                switchofftext = "."
            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " minutes" + switchofftext, data={"inline_keyboard":"Turn back on:/espresso_on, OK, thanks!:/removekeyboard"})
            self.log("Espresso machine has been on for " + str(minutes) + " minutes" + switchoffftext,)
