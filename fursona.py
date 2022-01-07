import random

from feature import Feature
import responses


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
        response = ("https://thisfursonadoesnotexist.com/v2/jpgs-2x"
                    f"/seed{str(fursona)}.jpg")
        
        # Reset seed for next random operation
        random.seed()
        
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
        seed = arg.strip() if arg is not None else author
        url = self.__gen_fursona(seed)
        response_set = responses.fursona_seeded if arg is not None else responses.fursona_base

        response = random.choice(response_set)
        response = response.format(name=seed, url=url)
        
        return response
