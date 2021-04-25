import random

from feature import Feature

class Fursona(Feature):
    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self, prefix, ctx=None):
        super().__init__(db_key="FURSONA")
        self.__PREFIX = prefix
        self.__CTX = ctx


    #################
    # CLASS METHODS #
    #################
    def __gen_fursona(self, seed):
        salt = "391110"         # so I can be pretty catboi
        # print(seed + salt)    # for testing
        random.seed(seed + salt)
        fursona = str(random.randint(0, 99999)).zfill(5)
        response = ("sexy and totally not super monsterous eldritch nightmare beast fursona!\n"
                    f"https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed{str(fursona)}.jpg")
        
        return response

    def arg_resolve(self, ctx, commandArg):
        response = ""
        # Argument resolution
        if commandArg == "on":
            if self.get_DAILY_STATE():
                response = ("Daily Fursona feature is already on...\n"
                            f"Try using '{self.__PREFIX}dailyfursona check' first next time.")
            else:
                # turn on feature
                self.set_DAILY_STATE(True)
                self.set_CHANNELID(ctx.channel.id)
                response = "Daily Fursona feature is now on."

                # log print db values
                self.__db_to_log()

        elif commandArg == "off":
            if not self.get_DAILY_STATE():
                response = ("Daily Fursona feature is already off...\n"
                            f"Try using '{self.__PREFIX}dailyfursona check' first next time.")
            else:
                # turn off feature
                self.set_DAILY_STATE(False)
                self.set_CHANNELID(None)
                self.set_TODAY(None)
                response = "Daily Fursona feature is now off."

                # log print db values
                self.__db_to_log()

        elif commandArg == "check":
            # Message the state of the daily Fursona feature
            if self.get_DAILY_STATE():
                response = "The Daily Fursona feature is currently on."
            else:
                response = "The Daily Fursona feature is currently off."

        else:
            # Display usable arguments
            response = (f"Please use '{self.__PREFIX}dailyfursona ' followed by:\n"
                        "'on' - To turn on the daily fursona feature.\n"
                        "'off' - to turn off the daily fursona feature.\n"
                        "'check' - to check whether the daily fursona feature is on or off.")
        
        return response

    def return_response(self, author, arg=None):
        if arg is None:
            response = self.__gen_fursona(author)
            response = f"{author}, I found your {response}"
        else:
            response = self.__gen_fursona(arg.strip())
            response = f"This is {arg}, a {response}"
        
        return response
