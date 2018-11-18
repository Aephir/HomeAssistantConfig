# Warn me if "enitiy" is left "on" for more than 45 minutes.
# Again if it is still on after 1 hour.
# After 1.5 hours, turn off and notify.

import appdaemon.plugins.hass.hassapi as hass
import datetime

class ApplianeceStatus(hass.Hass):

    def initialize(self):

        # Wouldn't this set the starttime to be the time the app is initialized, not when it is triggered?
        self.starttime = datetime.datetime.now()

        # Set this up to be our global timer. "None" means that it is not started at this point.
        # What does it mean that "Assignments to None are illegal and raise SyntaxError"? See "None" here: https://docs.python.org/3.6/library/constants.html
        self.timer = None

        # Runs "StartTimer" when "entity" state changes.
        self.listen_state(self.StartTimer,self.args["entity"])

    # I'm guessing this sould be "def StartTimer()", not "def SendNotification()"?? I've changed it.
    def StartTimer(self, entity, attribute, old, new, kwargs):

        # Stop everything if the "entity" is switched "off".
        if new == "off":
            self.cancel_timer(self.timer)

        else:

            # Marks the current time.
            self.starttime = datetime.datetime.now()

            # after "start_after" seconds (2700 in this case), start the "SendNotification" function.
            self.run_in(self.SendNotification,self.args["start_after"])


    def SendNotification(self, kwargs):

        # See how long since "entity" was turned on. Wouldn't this just be "start_after"?
        timediff = datetime.datetime.now() - self.starttime

        # I get an error "AttributeError: 'datetime.timedelta' object has no attribute 'second'"
        minutes = round(timediff.seconds/60)

        # As long as no more than "end_after" seconds has elapsed, continue:
        if minutes < self.args["end_after"]:

            # Send message, and log it.
            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " mins", data={"inline_keyboard":"Turn Off:/espresso_off, I Know:/removekeyboard"})
            self.log("Espresso machine has been on for " + str(minutes) + " mins")

            # After "time_between_notifications", re-run this same function (so "SendNotification" restarts itself?)
            self.run_in(self.SendNotification,self.args["time_between_notifications"])

        else:

            # Checks if "switch_off" is "True". I'm guessing so I can use this app and sometimes turn off the switch after X minutes, sometimes not?
            if self.args["switch_off"]:
                self.turn_of(self.args["entity"])
                switchofftext = ", i turned it off"
            else:
                switchofftext = ""
            self.call_service("notify/home_aephir_bot", message="Espresso machine has been on for " + str(minutes) + " mins" + switchofftext, data={"inline_keyboard":"Turn back on:/espresso_on, OK, thanks!:/removekeyboard"})
            self.log("Espresso machine has been on for " + str(minutes) + " mins" + switchoffftext,)
