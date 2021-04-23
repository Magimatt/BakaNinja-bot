import os
import sys
import discord
from discord.ext import commands
import random
from waifu import waifu
import asyncio
from datetime import datetime#, date, timedelta

##################
# Bot properties #
##################
TOKEN = os.getenv('TOKEN')
PREFIX = "~"
bot = commands.Bot(command_prefix=PREFIX, description='A bot to do stupid and cringy weeb things.\nWritten by Magimatt.')
waifu = waifu(PREFIX)


#############
# Bot logic #
#############
def GenFursona(seed):
    salt = "391110"
    print(seed + salt)
    random.seed(seed + salt)
    fursona = str(random.randint(0, 99999)).zfill(5)
    response = "sexy and totally not super monsterous eldritch nightmare beast fursona! \nhttps://thisfursonadoesnotexist.com/v2/jpgs-2x/seed" + str(fursona) + ".jpg"
    return response

async def daily_waifu_loop():    
    while True:
        # fail open check
        # check date and set if not today (plus activate daily waifu)
        if not waifu.get_DWSTATE() or waifu.get_CHANNELID is None or datetime.now(waifu.get_TZARIZONA()).strftime("%m/%d/%Y") == waifu.get_TODAY():
            await asyncio.sleep(10)
            return

        # do the things
        await bot.wait_until_ready()
        waifudatename = datetime.now(waifu.get_TZARIZONA()).strftime("%m/%d/%Y")
        print(f"waifudatename is {waifudatename}")
        ID = waifu.get_CHANNELID()
        print(f"{ID}, is type {type(ID)}")
        channel = bot.get_channel(ID)
        print(f"Channel {channel} gotten!")

        async with channel.typing(): # this does ctx.trigger_typing() without the ctx parameter
            await asyncio.sleep(3)
            await channel.send(waifu.send_waifu("No author", waifudatename))
        print(f"Daily waifu {waifudatename} sent.")

        waifu.set_TODAY(waifudatename)
        print(f"Today has been set to {waifu.get_TODAY()}.")

async def bot_is_typing(ctx):
    await ctx.trigger_typing()
    await asyncio.sleep(3)


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
    await bot_is_typing(ctx)
    await ctx.send("Konnichiwa! I'm BakaNinja Bot!")

# ~waifu command
@bot.command()
async def waifu(ctx, *, arg=None):
    await bot_is_typing(ctx)
    author = ctx.author.mention
    await ctx.send(waifu.send_waifu(author, arg))

# ~fursona command
@bot.command()
async def fursona(ctx, *, arg=None):
    await bot_is_typing(ctx)
    author = ctx.author.mention
    if arg is None:
        response = GenFursona(author)
        response = f"{author}, I found your {response}"
    else:
        response = GenFursona(arg.strip())
        response = f"This is {arg}, a {response}"
    await ctx.send(response)

# ~dailywaifu command, starts a daily waifu message sent in the channel it originated from
@bot.command()
async def dailywaifu(ctx, arg):
    await bot_is_typing(ctx)
    response = waifu.arg_resolve(ctx, arg)
    await ctx.send(response)

#################
# START THE BOT #
#################
def initialize_bot():
    bot.loop.create_task(daily_waifu_loop()) # adds the infinite asychio loop to the bot.run()
    print("Starting bot...")
    bot.run(TOKEN)

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
