from discord.ext import commands
import discord

from token_1 import DISCORD_TOKEN_IN_FILE

from Information import Information
from FunStuff import FunStuff
from BotListeners import BotListeners
from Timers import Timers
from Voice import Music

BOT_TOKEN = DISCORD_TOKEN_IN_FILE
BOT_VERSION = 0.1
CHANNEL_ID = 1253331751946944555

activity = discord.Activity(type=discord.ActivityType.listening, name="?help")
bot = commands.Bot(command_prefix="?", description="Multi-purpose bot for Squash and friends." ,intents=discord.Intents.all(), activity=activity)

bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.add_cog(Timers(bot))
    await bot.add_cog(FunStuff(bot))
    await bot.add_cog(Information(bot))
    await bot.add_cog(BotListeners(bot))
#    await bot.add_cog(Music(bot))
    Timers.task_loop.start()

    print("Hello world!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("SquashBot is now online! ✅")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if (isinstance(error, commands.CommandOnCooldown)):
        await ctx.send("**You're on a cooldown!** Try again in {:.2f} seconds.".format(error.retry_after))

bot.run(BOT_TOKEN)
