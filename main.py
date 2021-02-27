import discord
import os
import sys
from discord.ext import commands
import random

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

# Bot logic
def GenWaifu(seed):
    random.seed(seed)
    slider = random.randint(3, 20) * 0.1
    slider = format(slider, '.1f')
    waifu = str(random.randint(0, 99999)).zfill(5)
    response = " cute and totally not super cursed waifu! \nhttps://thisanimedoesnotexist.ai/results/psi-" + str(slider) + "/seed" + str(waifu) + ".png"
    return response

def GenFursona(seed):
    salt = "391110"
    print(seed + salt)
    random.seed(seed + salt)
    fursona = str(random.randint(0, 99999)).zfill(5)
    response = "sexy and totally not super monsterous eldritch nightmare beast fursona! \nhttps://thisfursonadoesnotexist.com/v2/jpgs-2x/seed" + str(fursona) + ".jpg"
    return response


# Prefix + description
bot = commands.Bot(command_prefix="~", description='A bot to do stupid and cringy weeb things.\nWritten by Dingo87.')

# Bot Commands
@bot.event
async def on_ready():
    print('Python version', sys.version)
    print('Discord API version: ' + discord.__version__)
    print('Logged in as', bot.user.name)
    print('Bot is ready!')

@bot.command()
async def hello(ctx):
    await ctx.send('Konnichiwa! I\'m BakaNinja Bot!')

# ~waifu command that takes arguments
@bot.command()
async def waifu(ctx, *, arg=None):
    _name = ctx.author.mention
    if arg is None:
        response = GenWaifu(_name)
        response = _name + ", I found your " + response
    else:
        response = GenWaifu(arg.strip())
        response = "This is " + arg + ", a" + response
    await ctx.send(response)

# ~fursona command
@bot.command()
async def fursona(ctx, *, arg=None):
    _name = ctx.author.mention
    if arg is None:
        response = GenFursona(_name)
        response = _name + ", I found your " + response
    else:
        response = GenFursona(arg.strip())
        response = "This is " + arg + ", a " + response
    await ctx.send(response)

print("Starting bot...")
bot.run(os.getenv('TOKEN'))


#####\/\/\/\/\/\/\/\/\/\/ TESTING BELOW \/\/\/\/\/\/\/\/\/\/#####

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
