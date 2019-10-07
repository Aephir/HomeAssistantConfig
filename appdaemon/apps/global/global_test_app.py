# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass
import global_functions_app

class Test(hass.Hass):

    def initialize(self):

        # self.log(self.args["test"])

        self.listen_state(self.test_app, 'input_boolean.vacation_mode')

    def test_app(self, entity, attribute, old, new, kwargs):

        # self.log('Testing function is running (method 1)... Will it call from different app?')
        # self.global_functions   = self.get_app('global_functions_app')  # Gets the class where the functions are?
        # test = self.global_functions.test_function()                    # Get the actual function
        # self.log(test)

        # self.log('Testing function is running (method 2)... Will it call from different app?')
        # test = self.get_app('global_functions_app').test_function() # app.function.
        # self.log(test)

        # self.log('Testing function is running (method 3)... Will it call from different app?')
        # test = self.get_app("global_functions_app")     # Get App
        # classtoget = test.Global()            # Get class
        # func = classtoget.test_function()               # Get function
        # self.log(func)

        # self.log('Testing function is running (method 4)... Will it call from different app?')
        # test = self.get_app("global_functions_app")     # Get App
        # func = test.test_function()                     # Get function
        # self.log(func)

        # self.log('Testing function is running (method 5)... Will it call from different app?')
        # test = self.get_app("global_functions_app")     # Get App
        # func = test.test_function()                     # Get function
        # # func = test.Global()                            # Get class
        # self.log(func)

        # self.log('Testing function is running (method 6)... Will it call from different app?')
        # get_app = self.get_app("global_functions_app")     # Get App
        # get_class = get_app.Global()            # Get class
        # get_func = get_class.test_function()               # Get function
        # self.log(get_func)

        self.log('Testing function is running (method 7, import)... Will it call from different app?')
        test = global_functions_app.Global().test_function()
        # test2 = global_test_app.test_function()
        self.log("test1", test)
        # self.log("test2", test2)
