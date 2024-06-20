import discord
from discord.ext import commands
import random

class FunStuff(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(description="Usage: ?choose <any> <amount> <of> <choices> \n\nPicks a random choice from what's input. For when you wanna settle the score some other way.")
    async def choose(self, ctx, *choicelist: str):
        await ctx.send(f'I choose **{random.choice(choicelist)}**!')
