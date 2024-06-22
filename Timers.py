import discord
from discord.ext import tasks, commands
import time
import asyncio

from HourTimer import HourTimer

hourList = []

class Timers(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @tasks.loop(seconds=3.0)
    async def task_loop():  # the function that will loop
        for i in range(len(hourList) - 1, -1, -1):
            if (hourList[i].end_time <= time.time()):
                await hourList[i].active_channel.send(f"{hourList[i].active_user.mention}, your timer has ended!")
                del hourList[i]

    @commands.command(description="Usage: ?timein <number of hours> \n\nOutputs a timezone-sensitive date when the specified number of hours will pass. Afterwards asks whether to set a timer for it or not. For when you don't wanna annoy yourself with timezones.")
    async def timein(self, ctx: commands.Context, hourNum: float):
        start_epoch_time = int(time.time())
        end_epoch_time = int(time.time() + hourNum * 3600)
        await ctx.send(f"The time in {hourNum:g} hours will be **<t:{end_epoch_time}:f>.**")
        
        if (hourNum < 0.1 or hourNum > 30):
            return

        await ctx.send(f"**Set a timer for it?** (y/n) *(This feature is still experimental, so please let Squash know of any bugs!)*")

        def is_correct(message):
                return message.author == ctx.author
        try:
            yesORnoMessage: discord.Message = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send(f'Sorry, you took too long. (10 seconds)')
        
        timer_counter: int = 0
        for timer in hourList:
            if (ctx.guild == timer.active_guild and ctx.author == timer.active_user and timer_counter < 5):
                timer_counter += 1
            elif (timer_counter >= 5):
                await ctx.channel.send(f"Sorry, you've already set the maximum amount of timers in this server. (5 timers)")
                return
        del timer_counter

        if (yesORnoMessage.content.lower() == 'y'):
            await ctx.channel.send(f'Alright, I will ping you in {hourNum:g} hour(s)!')
            hourList.append(HourTimer(start_epoch_time, end_epoch_time, ctx.author, ctx.guild, ctx.channel))

        elif (yesORnoMessage.content.lower() == 'n'):
            await ctx.channel.send(f"Alright, I won't set a timer for you.")
        else:
            await ctx.channel.send(f'Not a suitable answer, aborting task.')


    @commands.command()
    async def timers(self, ctx: commands.Context):
        timers_embed = discord.Embed(title="Your active timers:", color=discord.Color.teal())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            if (ctx.guild == timer.active_guild and ctx.author == timer.active_user):
                timerHour = (timer.end_time - timer.start_time) / 3600
                timers_embed.add_field(name=f'{timerHour:g} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>**", inline=False)
        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)
        await ctx.channel.send(embed=timers_embed)


    @commands.command()
    async def timersall(self, ctx: commands.Context):

        if (ctx.author.id != 400659477994536971):
            await ctx.channel.send("You're not Squash! Permission denied :x:")
            return

        timers_embed = discord.Embed(title="Timers active in this server:", color=discord.Color.teal())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            if (ctx.guild == timer.active_guild):
                timerHour = (timer.end_time - timer.start_time) / 3600
                timers_embed.add_field(name=f'{timerHour:g} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>** \nTimer requested by: **{timer.active_user}**.", inline=False)
        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)
        await ctx.channel.send(embed=timers_embed)

    @commands.command()
    async def timersglobal(self, ctx: commands.Context):
        if (ctx.author.id != 400659477994536971):
            await ctx.channel.send("You're not Squash! Permission denied :x:")
            return

        timers_embed = discord.Embed(title="Timers active globally:", color=discord.Color.teal())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            timerHour = (timer.end_time - timer.start_time) / 3600
            if (timer.active_guild):
                timers_embed.add_field(name=f'{timerHour} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>** \nTimer requested by: **{timer.active_user}** in **{timer.active_guild.name}**.", inline=False)
            else:
                timers_embed.add_field(name=f'{timerHour} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>** \nTimer requested by: **{timer.active_user}** in **direct messages**.", inline=False)

        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)
        await ctx.channel.send(embed=timers_embed)


    @commands.command()
    async def stoptimers(self, ctx: commands.Context):

        await ctx.send(f":exclamation: This will cancel *all* your currently active timers *in this server*, **are you sure?** (y/n)")

        def is_correct(message):
                return message.author == ctx.author
        try:
            yesORnoMessage: discord.Message = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send(f'Sorry, you took too long. (10 seconds)')
        
        if (yesORnoMessage.content.lower() == 'y'):  
            for i in range(len(hourList) - 1, -1, -1):
                if (hourList[i].active_user == ctx.author and hourList[i].active_guild == ctx.guild):
                    del hourList[i]

            await ctx.channel.send(f'Alright, if you had any active timers, they should be gone now!')

        elif (yesORnoMessage.content.lower() == 'n'):
            await ctx.channel.send(f"Alright, nothing was deleted.")
        else:
            await ctx.channel.send(f'Not a suitable answer, aborting task.')
        


    @commands.command()
    async def stoptimersall(self, ctx: commands.Context):
        if (ctx.author.id != 400659477994536971):
            await ctx.channel.send("You're not Squash! Permission denied. :x:")
            return

        for i in range(len(hourList) - 1, -1, -1):
            if (hourList[i].active_guild == ctx.guild):
                del hourList[i]
        await ctx.channel.send("Done deleting, ping no more!")

    @commands.command()
    async def stoptimersglobal(self, ctx: commands.Context):
        if (ctx.author.id != 400659477994536971):
            await ctx.channel.send("You're not Squash! Permission denied. :x:")
            return

        for i in range(len(hourList) - 1, -1, -1):
            del hourList[i]

        await ctx.channel.send("Done deleting EVERYTHING, ping no more!")