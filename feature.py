from datetime import datetime, time
import pytz
import pickle


class Feature:
    def __init__(self, db_key):
        self.filename = "daily"
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

    def __get_db(self):
        infile = open(self.filename, 'rb')
        file_dict = pickle.load(infile)
        infile.close()
        return file_dict

    def __close_db(self, database):
        outfile = open(self.filename, 'wb')
        pickle.dump(database, outfile)
        outfile.close()
    
    def __db_to_log(self):
        db = self.__get_db()
        for key in db:
            print(f"{key} is set to {db[key]}")
    
    def get_CHANNELID(self):
        db = self.__get_db()
        if db[f"DAILY{self.__db_key}-CHANNELID"] is None:
            return None
        else:
            return int(db[f"DAILY{self.__db_key}-CHANNELID"])

    def set_CHANNELID(self, ID):
        db = self.__get_db()
        db[f"DAILY{self.__db_key}-CHANNELID"] = ID
        self.__close_db(db)

    def get_DAILY_STATE(self):
        db = self.__get_db()
        return db[f"DAILY{self.__db_key}-STATE"]

    def set_DAILY_STATE(self, boolean):
        db = self.__get_db()
        db[f"DAILY{self.__db_key}-STATE"] = boolean
        self.__close_db(db)

    def get_RUNTODAY(self):
        db = self.__get_db()
        return db[f"DAILY{self.__db_key}-RUNTODAY"]

    def set_RUNTODAY(self, boolean):
        db = self.__get_db()
        db[f"DAILY{self.__db_key}-RUNTODAY"] = boolean
        self.__close_db(db)

    def get_TODAY(self):
        db = self.__get_db()
        return db[f"{self.__db_key}-TODAY"]

    def set_TODAY(self, date):
        db = self.__get_db()
        db[f"{self.__db_key}-TODAY"] = str(date)
        self.__close_db(db)


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