from discord.ext import commands
from colorama import init, Fore, Style, Back
from datetime import datetime as dt
from os import listdir
from os.path import isfile, join
import discord, os, sys, traceback, asyncio

init(convert=True)

print(f"{Fore.GREEN}Starting up.")

# Grab the bot token from the token file
try:
    tokenFile = open("token", 'r')
    tokenForm = tokenFile.readline()
    token = str.strip(tokenForm)
except FileNotFoundError:
    print(f"{Fore.RED}Token file not found. Please create a file titled 'token' with the bot token on the first line.")
    sys.exit(1)


cogs_dir = "modules"

# Init bot
bot = commands.Bot(command_prefix="`", status=discord.Status.do_not_disturb, activity=discord.Streaming(name="Starting...", url="https://panel.mcprohosting.com/status"))
bot.remove_command("help")

# Handlers
initHandlers = ['statusHandler']

#Create a logs dir
print(f"{Fore.YELLOW}Checking for logs directory")
if not os.path.exists("logs"):
    print(f"{Fore.LIGHTRED_EX}logs directory not found, creating it.")
    os.makedirs("logs")
else:
    print(f"{Fore.GREEN}logs directory found!")

# Load all extensions automatically before starting bot
for extension in initHandlers:
    try:
        bot.load_extension(cogs_dir + "." + extension)
        print(f"{extension} loaded.")
    except commands.ExtensionAlreadyLoaded:
        print(f"The extension {extension} is already loaded.")
    except commands.ExtensionNotLoaded:
        bot.load_extension(cogs_dir + "." + extension)
    except commands.ExtensionNotFound:
        print(f"The extension {extension} was not found.")
    except commands.ExtensionFailed as error:
        print("{} cannot be loaded. [{}]".format(extension, error))


@bot.event
async def on_ready():
    print(f"{Fore.GREEN}MCProNodes Initialized\n")
    await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name="Stalking the nodes", url="https://panel.mcprohosting.com/status"))


#Add a shutdown system, only used for the main process
@bot.command()
@commands.has_permissions(manage_guild=True)
async def shutdown(ctx):
    await ctx.channel.send("Shutting down main process.")
    await bot.logout()

#Load cog command
@bot.command()
@commands.has_permissions(manage_guild=True)
async def load(ctx, extension):
    try:
        bot.load_extension(cogs_dir + "." + extension)
        await ctx.channel.send(f"{extension} loaded.")
    except commands.ExtensionAlreadyLoaded:
        await ctx.channel.send(f"The extension {extension} is already loaded.")
    except commands.ExtensionNotLoaded:
        bot.load_extension(cogs_dir + "." + extension)
    except commands.ExtensionNotFound:
        await ctx.channel.send(f"The extension {extension} was not found.")
    except commands.ExtensionFailed as error:
        await ctx.channel.send("{} cannot be loaded. [{}]".format(extension, error))

#Unload cog command
@bot.command()
@commands.has_permissions(manage_guild=True)
async def unload(ctx, extension):
    try:
        bot.unload_extension(cogs_dir + "." + extension)
        await ctx.channel.send(f"{extension} unloaded.")
    except commands.ExtensionNotFound:
        await ctx.channel.send(f"The extension {extension} was not found.")
    except commands.ExtensionFailed as error:
        await ctx.channel.send("{} cannot be unloaded. [{}]".format(extension, error))

#Reload cog
@bot.command()
@commands.has_permissions(manage_guild=True)
async def reload(ctx, extension):
    try:
        bot.reload_extension(cogs_dir + "." + extension)
        await ctx.channel.send(f"{extension} reloaded.")
    except commands.ExtensionAlreadyLoaded:
        await ctx.channel.send(f"The extension {extension} is already loaded.")
    except commands.ExtensionNotLoaded:
        bot.load_extension(cogs_dir + "." + extension)
    except commands.ExtensionNotFound:
        await ctx.channel.send(f"The extension {extension} was not found.")
    except commands.ExtensionFailed as error:
        await ctx.channel.send("{} cannot be reloaded. [{}]".format(extension, error))


#Handle command errors
@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    ignored = (commands.CommandNotFound, commands.UserInputError)

    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.')
    elif isinstance(error, commands.NotOwner):
        return await ctx.send(f'This command can only be ran by Discord MANAGERs.')
    elif isinstance(error, commands.MissingAnyRole):
        return await ctx.send(error)
    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f'{ctx.command} is on cooldown.')
    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f'{ctx.command} cannot be used in DMs')
        except discord.DiscordException:
            pass
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':
            return await ctx.send("I could not find that member. Please try again")
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



#Mark a command as complete once completed
@bot.event
async def on_command_completion(ctx):
    try:
        if isinstance(ctx.channel, discord.DMChannel):
            pass
        else:
            await ctx.message.add_reaction(u"\u2705")
            await asyncio.sleep(5)
            await ctx.message.clear_reactions()
    except RuntimeError:
        pass


bot.run(token)