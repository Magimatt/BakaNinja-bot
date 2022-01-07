from datetime import datetime, time
import pytz
from replit import db

class Feature:
    def __init__(self, db_key):
        self.__db_key = db_key
        
        self.__timezone = pytz.timezone('US/ARIZONA')

        # time() obj = midnight + one second
        # TODO: implement time argument
        self.__tasktime = time().replace(hour=0,
                                         minute=0,
                                         second=1,
                                         microsecond=0,
                                         tzinfo=self.__timezone)
    #####################
    # GETTERS & SETTERS #
    #####################

    def get_CTX(self):
        return self.__CTX

    def set_CTX(self, ctx):
        self.__CTX = ctx


    ####################
    # DATABASE METHODS #
    ####################
    
    def __db_to_log(self):
        for key in db:
            print(f"{key} is set to {db[key]}")
    
    def get_CHANNELID(self):
        if db[f"DAILY{self.__db_key}-CHANNELID"] is None:
            return None
        else:
            return int(db[f"DAILY{self.__db_key}-CHANNELID"])

    def set_CHANNELID(self, ID):
        db[f"DAILY{self.__db_key}-CHANNELID"] = ID

    def get_DAILY_STATE(self):
        return db[f"DAILY{self.__db_key}-STATE"]

    def set_DAILY_STATE(self, boolean):
        db[f"DAILY{self.__db_key}-STATE"] = boolean

    def get_RUNTODAY(self):
        return db[f"DAILY{self.__db_key}-RUNTODAY"]

    def set_RUNTODAY(self, boolean):
        db[f"DAILY{self.__db_key}-RUNTODAY"] = boolean

    def get_TODAY(self):
        return db[f"{self.__db_key}-TODAY"]

    def set_TODAY(self, date):
        db[f"{self.__db_key}-TODAY"] = str(date)


    ###################
    # UTILITY METHODS #
    ###################

    def get_tasktime(self):
        return self.__tasktime

    def set_tasktime(self, time):
        self.__tasktime = time

    def get_current_date_string(self):
        return datetime.now(self.__timezone).strftime("%m/%d/%Y")


    ##############
    # INTERFACES #
    ##############

    def __db_to_log(self):
        return None

    def arg_resolve(self, ctx, commandArg):
        return None

    def return_response(self, author, arg=None):
        return None