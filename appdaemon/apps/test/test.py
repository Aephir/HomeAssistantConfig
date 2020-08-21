# Notify upon problems with plants

import appdaemon.plugins.hass.hassapi as hass

class Test(hass.Hass):

    def initialize(self):

        # self.log(self.args["test"])

        self.listen_state(self.test_app, 'input_boolean.vacation_mode')

    def test_app(self, entity, attribute, old, new, kwargs):

        self.toggle('light.dining_table_lights')



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


        self.log('Testing function is running (method 7)... Will it call from different app?')
        x = self.GlobalFunctions.testFunction()
        self.log(x)

        # self.log('Testing function is running (method 4)... Will it call from different app?')
        # test = self.get_app("global_functions_app")     # Get App
        #     # Nothing to get class???
        # classtoget = test.Global()            # Get class
        # # moduletoget = classtoget.global_functions()           # Get module
        # func = classtoget.test_function()               # Get function
        # self.log(func)

        # self.listen_event(self.receive_telegram_callback, 'telegram_callback')

    # def receive_telegram_callback(self, event_id, payload_event, *args):
    #
    #     data_callback   = payload_event['data']
    #     callback_id     = payload_event['id']
    #     message_id      = payload_event['message_id']
    #     chat_id         = payload_event['user_id']
    #
    #     self.log(payload_event)
    #
    #     if payload_event['data'] == '/removekeyboard':
    #
    #         self.call_service(
    #             'telegram_bot/answer_callback_query',
    #             message='OK',
    #             callback_query_id=callback_id
    #             )
    #
    #         self.call_service(
    #             'telegram_bot.edit_replymarkup',
    #             message_id=message_id,
    #             chat_id=user_id,
    #             inline_keyboard=[]
    #             )
