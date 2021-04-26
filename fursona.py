from datetime import time
import pytz
from replit import db
import random

import responses


class Fursona:
    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self, prefix, ctx=None):
        self.__PREFIX = prefix
        self.__TZARIZONA = pytz.timezone('US/ARIZONA')
        self.__CTX = ctx

        # time() obj = midnight + one second
        self.__tasktime = time().replace(hour=0, minute=0, second=1, microsecond=0, tzinfo=self.__TZARIZONA) # TODO: implement time argument

    #####################
    # GETTERS & SETTERS #
    #####################
    def get_CTX(self):
        return self.__CTX

    def set_CTX(self, ctx):
        self.__CTX = ctx

    def get_CHANNELID(self):
        if db["DAILYFURSONA-CHANNELID"] is None:
            return None
        else:
            return int(db["DAILYFURSONA-CHANNELID"])

    def set_CHANNELID(self, ID):
        db["DAILYFURSONA-CHANNELID"] = ID

    def get_DAILY_STATE(self):
        return db["DAILYFURSONA-STATE"]

    def set_DAILY_STATE(self, boolean):
        db["DAILYFURSONA-STATE"] = boolean

    def get_tasktime(self):
        return self.__tasktime

    def set_tasktime(self, time):
        self.__tasktime = time

    def get_RUNTODAY(self):
        return db["DAILYFURSONA-RUNTODAY"]

    def set_RUNTODAY(self, boolean):
        db["DAILYFURSONA-RUNTODAY"] = boolean

    def get_TZARIZONA(self):
        return self.__TZARIZONA

    def get_TODAY(self):
        return db["FURSONA-TODAY"]

    def set_TODAY(self, date):
        db["FURSONA-TODAY"] = str(date)

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

    def __db_to_log(self):
        for key in db:
            print(f"{key} is set to {db[key]}")

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
