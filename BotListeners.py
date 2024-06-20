from discord.ext import tasks, commands
import discord
from Information import Information

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