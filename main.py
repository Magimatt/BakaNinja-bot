import os
import sys
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
from waifu import Waifu
from fursona import Fursona
from ask import Ask
from datetime import datetime#, date, timedelta
import re as regex


#########################
# Global bot properties #
#########################
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WOLFRAM_ALPHA_TOKEN = os.getenv('WOLFRAM_ALPHA_TOKEN')
# TOKEN = os.environ['TOKEN'] # per REPLIT this is the way to access the environment variables...
PREFIX = "~"
bot = commands.Bot(command_prefix=PREFIX, description='A bot to do stupid and cringy weeb things.\nWritten by Magimatt.')
w = Waifu(PREFIX)
f = Fursona(PREFIX)
a = Ask(PREFIX)

#############
# Bot logic #
#############
async def daily_loop(feature):
    while True:
        # fail open check
        # check date and set if not today (plus activate daily waifu)
        if (not feature.get_DAILY_STATE()
                or feature.get_CHANNELID is None
                or feature.get_current_date_string() == feature.get_TODAY()):
            
            await asyncio.sleep(10)
        else:
            await bot.wait_until_ready()
            waifudatename = feature.get_current_date_string()
            print(f"waifudatename is {waifudatename}")
            ID = feature.get_CHANNELID()
            print(f"{ID}, is type {type(ID)}")
            channel = bot.get_channel(ID)
            print(f"Channel {channel} get!")

            async with channel.typing(): # this does ctx.trigger_typing() without the ctx parameter
                await asyncio.sleep(3)
                await channel.send(feature.return_response("No author", waifudatename))
            print(f"Daily waifu {waifudatename} sent.")

            feature.set_TODAY(waifudatename)
            print(f"Today has been set to {feature.get_TODAY()}.")

# possibly obsolete
# async def daily_waifu_loop():
#     while True:
#         # fail open check
#         # check date and set if not today (plus activate daily waifu)
#         if (not w.get_DAILY_STATE() or
#         w.get_CHANNELID is None or
#         datetime.now(w.get_TZARIZONA()).strftime("%m/%d/%Y") == w.get_TODAY()):
#             await asyncio.sleep(10)
#         else:
#             await bot.wait_until_ready()
#             waifudatename = datetime.now(w.get_TZARIZONA()).strftime("%m/%d/%Y")
#             print(f"waifudatename is {waifudatename}")
#             ID = w.get_CHANNELID()
#             print(f"{ID}, is type {type(ID)}")
#             channel = bot.get_channel(ID)
#             print(f"Channel {channel} get!")

#             async with channel.typing(): # this does ctx.trigger_typing() without the ctx parameter
#                 await asyncio.sleep(3)
#                 await channel.send(w.return_response("No author", waifudatename))
#             print(f"Daily waifu {waifudatename} sent.")

#             w.set_TODAY(waifudatename)
#             print(f"Today has been set to {w.get_TODAY()}.")

# async def daily_fursona_loop():
#     while True:
#         # fail open check
#         # check date and set if not today (plus activate daily fursona)
#         if (not f.get_DAILY_STATE() or
#         f.get_CHANNELID is None or
#         datetime.now(f.get_TZARIZONA()).strftime("%m/%d/%Y") == f.get_TODAY()):
#             await asyncio.sleep(10)
#         else:
#             await bot.wait_until_ready()
#             fursonadatename = datetime.now(f.get_TZARIZONA()).strftime("%m/%d/%Y")
#             print(f"fursonadatename is {fursonadatename}")
#             ID = f.get_CHANNELID()
#             print(f"{ID}, is type {type(ID)}")
#             channel = bot.get_channel(ID)
#             print(f"Channel {channel} get!")

#             async with channel.typing(): # this does ctx.trigger_typing() without the ctx parameter
#                 await asyncio.sleep(3)
#                 await channel.send(f.return_response("No author", fursonadatename))
#             print(f"Daily fursona {fursonadatename} sent.")

#             w.set_TODAY(fursonadatename)
#             print(f"Today has been set to {f.get_TODAY()}.")

def must_bang(arg): # for cow mom (aka Jacob)
    # Discord adds a '!' to member mention IDs (e.g. <@!123456789012>)
    # if they have a nickname set in the guild. This produces an
    # inconsistent seed if the member does not have a nickname set.
    if not regex.match(r'<@\d{17,18}>', arg):
        return arg
    else:
        splitArg = list(arg)
        splitArg.insert(2, "!")
        joinArg = ''.join(splitArg)
        return joinArg

async def bot_is_typing(ctx, responselength):
    seconds = 2  # minimun trigger_typing amount
    # Else calculate a percentage of the total message characters to 10 seconds
    if responselength > 200:
        seconds = (responselength / 2000) * 10
    
    # trigger_typing() goes for 10 seconds or until a context.send() is called
    await ctx.trigger_typing()
    await asyncio.sleep(seconds)

async def bot_respond(ctx, response):
    # Discord limits response size to 2000 characters or less
    # splitresponse() will split up the response into 2000 char length chunks
    def splitresponse(str, chunk=2000):
        return [ str[start:start+chunk] for start in range(0, len(str), chunk) ]
    
    print(f"BakaNinja-bot is trying to type: {response}")  # Debug

    if len(response) <= 2000 and len(response) != 0:
        await bot_is_typing(ctx, len(response))
        await ctx.send(response)
    else:
        responselist = splitresponse(response)
        for chunk in responselist:
            if len(chunk) != 0:
                await bot_is_typing(ctx, len(chunk))
                await ctx.send(chunk)


################
# Bot Commands #
################
@bot.event
async def on_ready():
    print(f'Python version: {sys.version}')
    print(f'Discord API version: {discord.__version__}')
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready!')

# bot test command
@bot.command()
async def hello(ctx):
    hello = "Konnichiwa! I'm BakaNinja Bot!"
    await bot_respond(ctx, hello)

# ~waifu command
@bot.command(name='waifu',
             aliases=['w'],
             help='Generate a waifu with the ~waifu command alone or with any argument after (E.g. ~waifu weeb)',
             brief='Use with or without a following argument.')
async def waifu(ctx, *, arg=None):
    print(f"ID: {ctx.author.id}\n" +
          f"Mention: {ctx.author.mention}\n" +
          f"Nickname: {ctx.author.nick}\n" +
          f"Name: {ctx.author.name}")
    author = must_bang(ctx.author.mention)
    modified_arg = must_bang(arg) if arg is not None else None
    response = w.return_response(author, modified_arg)
    await bot_respond(ctx, response)

# ~fursona command
@bot.command(name='fursona',
             aliases=['f'],
             help='Generate a fursona with the ~fursona command alone or with any argument after (E.g. ~fursona furry)',
             brief='Use with or without a following argument.')
async def fursona(ctx, *, arg=None):
    author = must_bang(ctx.author.mention)
    modified_arg = must_bang(arg) if arg is not None else None
    response = f.return_response(author, modified_arg)
    await bot_respond(ctx, response)

# ~dailywaifu command, starts a daily waifu message sent in the channel it originated from
@bot.command(name='dailywaifu',
             aliases=['dw'],
             help='Bakaninja can provide you with endless waifu everyday! Use the argument "check" to see if the feature is on. "on" will turn it on and "off" wil turn it off. Amazing!',
             brief='Use arguments "on" and "off". "check" will tell you the status')
async def dailywaifu(ctx, arg=None):
    response = w.arg_resolve(ctx, arg) # sends a confirmation message as well as activates/deactivates the feature
    await bot_respond(ctx, response)

# ~dailyfursona command, starts a daily fursona message sent in the channel it originated from
@bot.command(name='dailyfursona',
             aliases=['df'],
             help='Bakaninja can provide you with endless waifu everyday! Use the argument "check" to see if the feature is on. "on" will turn it on and "off" wil turn it off. Amazing!',
             brief='Use arguments "on" and "off". "check" will tell you the status')
async def dailyfursona(ctx, arg=None):
    response = f.arg_resolve(ctx, arg) # sends a confirmation message as well as activates/deactivates the feature
    await bot_respond(ctx, response)

@bot.command(name='question',
             aliases=['ask', 'q', '?'],
             help='Bakaninja know soooo much! Try asking it a question like "~question How many molecules are in a mole?"',
             brief='Type the command followed by your question.')
async def question(ctx, *, arg=None):
    await bot_respond(ctx, "Hmmm... let me think.")
    response = await a.return_response_ask(arg)

    await bot_respond(ctx, response)

#################
# START THE BOT #
#################
def initialize_bot():
    # add infinite asyncio loops to the bot.run()
    bot.loop.create_task(daily_loop(w))
    bot.loop.create_task(daily_loop(f))

    print("Starting bot...")
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    initialize_bot()



#####\/\/\/\/ OLD STUFF & TESTING BELOW \/\/\/\/#####

# import os
# import sys
# import discord
# from discord.ext import commands
# from dotenv import load_dotenv
# import random

# def main():
#   while True:
#     success, seed = GetSeed()
#     if success:
#       URLSeed = GenWaifuSeed(seed)
#     if not success:
#       URLSeed = GenFursonaSeed(seed)
#     print(URLSeed)


# def GetSeed():
#   while True:
#     command = input("Command?: ")
#     if command == "!waifu":
#       seedInput = input("Input waifu seed: ")
#       return (True, seedInput)
#     elif command == "!fursona":
#       seedInput = input("Input fursona seed: ")
#       return (False, seedInput)
#     else:
#       print("Invalid command")


# def GenWaifuSeed(inputSeed):
#   random.seed(inputSeed)
#   slider = random.randint(3, 21) * 0.1
#   slider = format(slider, '.1f')
#   waifu = str(random.randint(0, 100000)).zfill(5)
#   return "@{username}, I've got your cute and totally not super cursed waifu right here!\nhttps://thisanimedoesnotexist.ai/results/psi-" + str(slider) + "/seed" + str(waifu) + ".png"


# def GenFursonaSeed(inputSeed):
#   random.seed(inputSeed)
#   fursona = str(random.randint(0, 100000)).zfill(5)
#   return "@{username}, Ok, here is your sexy and totally not super monsterous eldritch nightmare beast fursona... Yeah. It's probably fine. https://thisfursonadoesnotexist.com/v2/jpgs-2x/seed" + str(fursona) + ".jpg"
  

# # if __name__ == "__main__":
# #   main()


# ##################
# # Discord stuffs #
# ##################

# # Private token Initialization
# load_dotenv()
# TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# # Prefix + description
# bot = commands.Bot(command_prefix="!", description="A bot to do stupid and cringy otaku things.")

###############################

# client = discord.Client()
 
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('~hello'):
#         await message.channel.send('Konnichiwa! I\'m BakaNinja Bot!')

# ############
# # COMMANDS #
# ############

# @bot.event
# async def on_ready():
#   print("Python version", sys.version)
#   print("Discord API version: " + discord.__version__)
#   print("Logged in as", bot.user.name)
#   print("Bot is ready!")

# @bot.command()
# async def hello():
#   bot.msg = await bot.say("Konnichiwa! My name is " + NAME)

# @bot.command()
# async def waifu():
#   #this does a things
#   remove = "this"

# @bot.command()
# async def fursona():
#   remove = "this"


# bot.run(TOKEN)
