import random

from feature import Feature
import responses


class Waifu(Feature):
    ###############
    # CONSTRUCTOR #
    ###############
    def __init__(self, prefix, ctx=None):
        super().__init__(db_key="WAIFU")
        self.__PREFIX = prefix
        self.__CTX = ctx

        # self.__DWSTATE = db["DWSTATE"]


    #################
    # CLASS METHODS #
    #################
    def __gen_waifu(self, seed):
        random.seed(seed)
        slider = random.randint(3, 20) * 0.1
        slider = format(slider, '.1f')
        waifu = str(random.randint(0, 99999)).zfill(5)
        response = ("https://thisanimedoesnotexist.ai/results"
                    f"/psi-{str(slider)}/seed{str(waifu)}.png")
                    
        # Reset seed for next next random operation
        random.seed()

        return response

    def arg_resolve(self, ctx, commandArg):
        response = ""
        # Argument resolution
        if commandArg == "on":
            if self.get_DAILY_STATE():
                response = f"Daily Waifu feature is already on...\nTry using '{self.__PREFIX}dailywaifu check' first next time."
            # turn on feature
            else:
                self.set_DAILY_STATE(True)
                self.set_CHANNELID(ctx.channel.id)
                response = "Daily Waifu feature is now on."

                # log print db values
                self.__db_to_log()

        elif commandArg == "off":
            if not self.get_DAILY_STATE():
                response = f"Daily Waifu feature is already off...\nTry using '{self.__PREFIX}dailywaifu check' first next time."
            # turn off feature
            else:
                self.set_DAILY_STATE(False)
                self.set_CHANNELID(None)
                self.set_TODAY(None)
                response = "Daily Waifu feature is now off."

                # log print db values
                self.__db_to_log()

        elif commandArg == "check":
            # Message the state of the daily waifu feature
            if self.get_DAILY_STATE():
                response = "The Daily Waifu feature is currently on."
            else:
                response = "The Daily Waifu feature is currently off."

        else:
            # Display usable arguments
            response = (f"Please use '{self.__PREFIX}dailywaifu ' followed by:\n"
                        "'on' - To turn on the daily waifu feature.\n"
                        "'off' - to turn off the daily waifu feature.\n"
                        "'check' - to check whether the dailywaifu feature is on or off.")
        return response

    def return_response(self, author, arg=None):
        # If an arg was provided then use that instead of author
        seed = arg.strip() if arg is not None else author
        print("return_response() seed:", seed)
        url = self.__gen_waifu(seed)
        response_set = responses.waifu_seeded if arg is not None else responses.waifu_base
        
        response = random.choice(response_set)
        response = response.format(name=seed, url=url)

        return response
    
    #######################
    # OLD & TESTING BELOW #
    #######################
    # Maybe implement a more dynamic way to check the time later
    # def get_tomorrow_morning(self):
    #     now = datetime.datetime.now(self.__TZARIZONA)
    #     tomorrowMorning = now.replace(hour=0, minute=0, second=1, microsecond=0) + datetime.timedelta(days=1)
    #     delta = tomorrowMorning - now
    #     deltaSeconds = delta.total_seconds()
    #     return deltaSeconds

    # async def daily_waifu_loop(self):
    #     nextTaskTime = self.get_tomorrow_morning()
    #     print(f"Waiting {nextTaskTime} seconds until next daily Waifu...")
    #     await asyncio.sleep(nextTaskTime)

    #     if self.__DWSTATE:
    #         waifuDateName = datetime.datetime.now(self.__TZARIZONA).strftime("%m/%d/%Y")
    #         response = __GenWaifu(waifuDateName)
    #         response = f"This is {waifuDateName}, a {response}"
    #         await self.__CTX.send(response)
    #         print(f"Daily waifu {waifuDateName} sent.")
    #     else:
    #         pass
