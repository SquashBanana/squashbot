from discord.ext import tasks, commands
import discord

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
        help_embed.add_field(name="?choose <any> <amount> <of> <choices>", value="Picks a random item from an infinite number of choices (with spaces between them). \n*For when you wanna settle the score some other way.*", inline=False)
        help_embed.add_field(name="?timein <number of hours>", value="Outputs a timezone-sensitive date when the specified number of hours will pass. \nIf it's 0.1 to 30 hours, the bot asks whether to set a timer for it. \n*For when you don't wanna annoy yourself with timezones.*", inline=False)
        help_embed.add_field(name="?timers", value="Shows a list of all timers you have set with **?timein** in this server.", inline=False)
        help_embed.add_field(name="?stoptimers", value="Stops all your timers on this server! Use with care. *(Squash was too lazy to program deleting select timers)*", inline=False)
        help_embed.set_footer(text=f"Requested by {message.author}.", icon_url=message.author.avatar)

        await message.channel.send(embed=help_embed)