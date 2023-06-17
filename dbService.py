import argparse
# from datetime import datetime, time
# import pytz
import pickle

_FRESHDB = {'DAILYWAIFU-CHANNELID': None, 'DAILYWAIFU-STATE': False,
               'DAILYWAIFU-RUNTODAY': False, 'DAILYFURSONA-CHANNELID': None,
               'DAILYFURSONA-STATE': False, 'DAILYFURSONA-RUNTODAY': False,
               'WAIFU-TODAY': None, 'FURSONA-TODAY': None}

parser = argparse.ArgumentParser(prog='dbService', description='Service BakaNinja database')
parser.add_argument('-r', '--reset', action='store_true',
                    help="Resets the daily database to default values.")
parser.add_argument('-p', '--print', action='store_true',
                    help="Prints the daily database to console.")
args = parser.parse_args()

if args.reset:
    outfile = open('daily','wb')
    pickle.dump(_FRESHDB, outfile)
    outfile.close()
    print("BakaNinja database succesfully reset.")
elif args.print:
    infile = open('daily', 'rb')
    dbDict = pickle.load(infile)
    infile.close()
    print(dbDict)
else:
    print("Invaild command-line argument.\nPlease use --help for valid arguments.")