from discord.ext import commands
import discord

from token_1 import DISCORD_TOKEN_IN_FILE

from Information import Information
from FunStuff import FunStuff
from BotListeners import BotListeners
from Timers import Timers

BOT_TOKEN = DISCORD_TOKEN_IN_FILE

CHANNEL_ID = 784043245465501696

activity = discord.Activity(type=discord.ActivityType.listening, name="?help")
bot = commands.Bot(command_prefix="?", description="Multi-purpose bot for Squash and friends." ,intents=discord.Intents.all(), activity=activity)

bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.add_cog(Timers(bot))
    await bot.add_cog(FunStuff(bot))
    await bot.add_cog(Information(bot))
    await bot.add_cog(BotListeners(bot))
    Timers.task_loop.start()
    
    print("Hello world!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("SquashBot is now online! ✅")

bot.run(BOT_TOKEN)
