import discord
from discord.ext import tasks, commands
import time
import asyncio

from HourTimer import HourTimer

hourList = []

class Timers(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(description="Usage: ?timein <number of hours> \n\nOutputs a timezone-sensitive date when the specified number of hours will pass. Afterwards asks whether to set a timer for it or not. For when you don't wanna annoy yourself with timezones.")
    async def timein(self, ctx: commands.Context, hourNum: float):
        start_epoch_time = int(time.time())
        end_epoch_time = int(time.time() + hourNum * 3600)
        await ctx.send(f"The time in {hourNum} hours will be **<t:{end_epoch_time}:f>** \n**Set a timer for it?** (y/n) \n:exclamation: This feature doesn't work yet, so you will not be pinged at the end. :exclamation:")

        def is_correct(message):
                return message.author == ctx.author
        try:
            yesORnoMessage = await self.bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            return await ctx.channel.send(f'Sorry, you took too long. (10 seconds)')
        
        if (yesORnoMessage.content == 'y'):
            await ctx.channel.send(f'Alright, I will ping you in {hourNum} hours!')
            hourList.append(HourTimer(start_epoch_time, end_epoch_time, ctx.author, ctx.guild, ctx.channel))
        ### MAKE TASK AND PING IN THE END
        elif (yesORnoMessage.content == 'n'):
            await ctx.channel.send(f"Alright, I won't set a timer for you")
        else:
            await ctx.channel.send(f'Not a suitable answer, aborting task.')

    @commands.command()
    async def timers(self, ctx: commands.Context):
        timers_embed = discord.Embed(title="Timers active in this server:", color=discord.Color.orange())
        timers_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
        for timer in hourList:
            if (ctx.guild == timer.active_guild):
                timerHour = (timer.end_time - timer.start_time) / 3600
                timers_embed.add_field(name=f'{timerHour} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>** \nTimer requested by: **{timer.active_user}**.", inline=False)
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
            timerHour = (timer.end_time - timer.start_time) / 3600
            timers_embed.add_field(name=f'{timerHour} hour timer.', value=f"Ends at **<t:{timer.end_time}:f>** \nTimer requested by: **{timer.active_user}** in **{timer.active_guild.name}**.", inline=False)
        timers_embed.set_footer(text=f"Requested by {ctx.author}.", icon_url=ctx.author.avatar)

        await ctx.channel.send(embed=timers_embed)