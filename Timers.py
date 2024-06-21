import discord
from discord.ext import tasks, commands
import time
import asyncio

from HourTimer import HourTimer

hourList = []
started_tasks = []

async def task_loop(ctx, start_time: int, end_time: int, active_user: discord.User, active_guild: discord.Guild, active_channel: discord.abc.Messageable):  # the function that will "loop"
    await active_channel.send(active_user.mention)

def task_generator(ctx, start_time: int, end_time: int, active_user: discord.User, active_guild: discord.Guild, active_channel: discord.abc.Messageable):
    task_time: float = end_time - start_time
    task_object = tasks.loop(seconds=task_time, count=2)(task_loop) # turns normal function into task
    started_tasks.append(task_object)
    task_object.start(ctx, start_time, end_time, active_user, active_guild, active_channel) # starts the task
    
def startTask(ctx, start_time: int, end_time: int, active_user: discord.User, active_guild: discord.Guild, active_channel: discord.abc.Messageable):
    task_generator(ctx, start_time, end_time, active_user, active_guild, active_channel)


class Timers(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

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
        
        if (yesORnoMessage.content.lower() == 'y'):
            await ctx.channel.send(f'Alright, I will ping you in {hourNum:g} hours!')
            hourList.append(HourTimer(start_epoch_time, end_epoch_time, ctx.author, ctx.guild, ctx.channel))
            startTask(ctx, start_epoch_time, end_epoch_time, ctx.author, ctx.guild, ctx.channel)

        elif (yesORnoMessage.content.lower() == 'n'):
            await ctx.channel.send(f"Alright, I won't set a timer for you.")
        else:
            await ctx.channel.send(f'Not a suitable answer, aborting task.')


    @commands.command()
    async def timers(self, ctx: commands.Context):
        timers_embed = discord.Embed(title="Your active timers:", color=discord.Color.orange())
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

        timers_embed = discord.Embed(title="Timers active in this server:", color=discord.Color.orange())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            if (ctx.guild == timer.active_guild):
                timerHour = (timer.end_time - timer.start_time) / 3600
                timers_embed.add_field(name=f'{timerHour:g} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>** \nTimer requested by: **{timer.active_user}**.", inline=False)
        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)
        await ctx.channel.send(embed=timers_embed)

        if (ctx.author.id != 400659477994536971):
            return
        for t in started_tasks:
            print(f"{t.seconds} === {t.current_loop}")
        print("---")
        for h in hourList:
            print(f"{h.start_time} === {h.end_time} === {h.end_time - h.start_time}")

    @commands.command()
    async def timersglobal(self, ctx: commands.Context):
        if (ctx.author.id != 400659477994536971):
            await ctx.channel.send("You're not Squash! Permission denied :x:")
            return

        timers_embed = discord.Embed(title="Timers active globally:", color=discord.Color.orange())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            timerHour = (timer.end_time - timer.start_time) / 3600
            timers_embed.add_field(name=f'{timerHour} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>** \nTimer requested by: **{timer.active_user}** in **{timer.active_guild.name}**.", inline=False)
        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)
        await ctx.channel.send(embed=timers_embed)


    @commands.command()
    async def stoptimers(self, ctx: commands.Context):

        await ctx.send(f":exclamation: This will remove *all* your currently active timers *in this server*, **are you sure?** (y/n) :exclamation:")

        def is_correct(message):
                return message.author == ctx.author
        try:
            yesORnoMessage: discord.Message = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send(f'Sorry, you took too long. (10 seconds)')
        
        if (yesORnoMessage.content.lower() == 'y'):  
            for i in range(len(started_tasks) - 1, -1, -1):
                if (hourList[i].active_user == ctx.author and hourList[i].active_guild == ctx.guild):
                    started_tasks[i].cancel()
                    del started_tasks[i]
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

        for i in range(len(started_tasks) - 1, -1, -1):
            if (hourList[i].active_guild == ctx.guild):
                started_tasks[i].cancel()
                del started_tasks[i]
                del hourList[i]
        await ctx.channel.send("Done deleting, ping no more!")

    @commands.command()
    async def stoptimersglobal(self, ctx: commands.Context):
        if (ctx.author.id != 400659477994536971):
            await ctx.channel.send("You're not Squash! Permission denied. :x:")
            return

        for i in range(len(started_tasks) - 1, -1, -1):
            started_tasks[i].cancel()
            del started_tasks[i]
            del hourList[i]
        await ctx.channel.send("Done deleting EVERYTHING, ping no more!")