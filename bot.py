from discord.ext import tasks, commands
import discord
from dataclasses import dataclass
import random
import time
from token_1 import DISCORD_TOKEN_IN_FILE
import asyncio

#import os
#BOT_TOKEN = os.environ.get('TOKEN', 0)
BOT_TOKEN = DISCORD_TOKEN_IN_FILE
CHANNEL_ID = 784043245465501696

class HourTimer:
    def __init__(self, start_time, end_time, active_user, active_guild, active_channel):
        self.is_active: bool = True
        self.start_time: int = start_time
        self.end_time: int = end_time
        self.active_user: discord.User = active_user
        self.active_guild: discord.Guild = active_guild
        self.active_channel: discord.abc.Messageable = active_channel

hourList = []

class BotListeners(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author == self.bot.user:
            return
        if message.content == self.bot.user.mention:
            await Information.help(self, message)



class Information(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name = "help",
                    description = "Displays information about the bot.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def help(self, message:discord.Message):
        help_embed = discord.Embed(title="Available commands and their usage:", color=discord.Color.orange())
        help_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        help_embed.add_field(name="?help", value="Shows this page.", inline=False)
        help_embed.add_field(name="?choose <any> <amount> <of> <choices>", value="Picks a random item from an infinite number of choices (with spaces between them). For when you wanna settle the score some other way.", inline=False)
        help_embed.add_field(name="?timein <number of hours>", value="Outputs a timezone-sensitive date when the specified number of hours will pass. Afterwards asks whether to set a timer for it or not. For when you don't wanna annoy yourself with timezones.", inline=False)
        help_embed.add_field(name="?timers", value="Shows a list of all timers set with **?timein** in this server.", inline=False)
        help_embed.set_footer(text=f"Requested by {message.author}.", icon_url=message.author.avatar)

        await message.channel.send(embed=help_embed)

    

class FunStuff(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.command(description="Usage: ?timein <number of hours> \n\nOutputs a timezone-sensitive date when the specified number of hours will pass. Afterwards asks whether to set a timer for it or not. For when you don't wanna annoy yourself with timezones.")
    async def timein(self, ctx: commands.Context, hourNum: float):
        time_now_since_epoch = int(time.time())
        future_time_since_epoch = int(time.time() + hourNum * 3600)
        await ctx.send("The time in " + str(hourNum) + " hours will be **<t:" + str(future_time_since_epoch) + ":f>** \n**Set a timer for it?** (y/n) \n:exclamation: This feature doesn't work yet, so you will not be pinged at the end. :exclamation:")

        def is_correct(m):
                return m.author == ctx.author
        try:
            yesornoTimer = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send(f'Sorry, you took too long. (10 seconds)')
        
        if (yesornoTimer.content == 'y'):
            await ctx.channel.send(f'Alright, I will ping you in {hourNum} hours!')
            hourList.append(HourTimer(time_now_since_epoch, future_time_since_epoch, ctx.author, ctx.guild, ctx.channel))
        ### MAKE TASK AND PING IN THE END
        elif (yesornoTimer.content == 'n'):
            await ctx.channel.send(f'Alright, no.')
        else:
            await ctx.channel.send(f'Not a suitable answer, aborting task.')

    @commands.command()
    async def timers(self, ctx: commands.Context):
        timers_embed = discord.Embed(title="Timers active in this server:", color=discord.Color.orange())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            if (ctx.guild == timer.active_guild):
                timerHour = (timer.end_time - timer.start_time) / 3600
                timers_embed.add_field(name=f'{timerHour} hour timer.', value="Ends at **<t:" + str(timer.end_time) + ":f>**", inline=False)
        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)

        await ctx.channel.send(embed=timers_embed)

    @commands.command()
    async def timersall(self, ctx: commands.Context):
        if (ctx.author.id != 400659477994536971):
            await ctx.channel.send("You're not Squash! Permission denied :x:")
            return

        timers_embed = discord.Embed(title="Timers active globally:", color=discord.Color.orange())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            if (ctx.guild == timer.active_guild):
                timerHour = (timer.end_time - timer.start_time) / 3600
                timers_embed.add_field(name=f'{timerHour} hour timer.', value="Ends at **<t:" + str(timer.end_time) + ":f>**", inline=False)
        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)

        await ctx.channel.send(embed=timers_embed)

    @commands.command(description="Usage: ?choose <any> <amount> <of> <choices> \n\nPicks a random choice from what's input. For when you wanna settle the score some other way.")
    async def choose(self, ctx, *choicelist: str):
        await ctx.send(f'I choose {random.choice(choicelist)}!')


bot = commands.Bot(command_prefix="?", description="Multi-purpose bot for Squash and friends." ,intents=discord.Intents.all())

bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.add_cog(FunStuff(bot))
    await bot.add_cog(Information(bot))
    await bot.add_cog(BotListeners(bot))

    print("Hello! I am alive")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("**Hell**o! I am alive :) \nsubcribe")


bot.run(BOT_TOKEN)
