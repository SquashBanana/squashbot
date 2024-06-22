from discord.ext import tasks, commands
import discord

class Information(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name = "help",
                    description = "Displays information about the bot.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, message:discord.Message, category:str=""):
        if (category.lower()==""):
            help_embed = discord.Embed(title="Command categories:", color=discord.Color.teal())
            help_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
            help_embed.add_field(name="Information", value="Commands to do with information about the bot.", inline=False)
            help_embed.add_field(name="Entertain", value="General commands for conversational use.", inline=False)
            help_embed.add_field(name="Timers", value="Commands to do with timers and *?timein*.", inline=False)
            help_embed.add_field(name="❔ **Use ?help <category> for more help!** ❔", value="", inline=False)
            help_embed.set_footer(text=f"Requested by {message.author}.", icon_url=message.author.avatar)
            await message.channel.send(embed=help_embed)
        
        elif (category.lower()=="information"):
            help_embed = discord.Embed(title="Available commands and their usage:", color=discord.Color.teal())
            help_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
            help_embed.add_field(name="?help", value="Use if you're confused about how to use this bot.", inline=False)
            help_embed.add_field(name="?version", value="Displays current bot version.", inline=False)
            help_embed.set_footer(text=f"Requested by {message.author}.", icon_url=message.author.avatar)
            await message.channel.send(embed=help_embed)

        elif (category.lower()=="entertain"):
            help_embed = discord.Embed(title="Available commands and their usage:", color=discord.Color.teal())
            help_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
            help_embed.add_field(name="?choose <any> <amount> <of> <choices>", value="Picks a random item from an infinite number of choices (with spaces between them). \n*For when you wanna settle the score some other way.*", inline=False)
            help_embed.set_footer(text=f"Requested by {message.author}.", icon_url=message.author.avatar)
            await message.channel.send(embed=help_embed)
        
        elif (category.lower()=="timers"):
            help_embed = discord.Embed(title="Available commands and their usage:", color=discord.Color.teal())
            help_embed.set_author(name="SquashBot", icon_url=self.bot.user.avatar)
            help_embed.add_field(name="?timein <number of hours>", value="Outputs a timezone-sensitive date when the specified number of hours will pass. \nIf it's 0.1 to 30 hours, the bot asks whether to set a timer for it. \n*For when you don't wanna annoy yourself with timezones.*", inline=False)
            help_embed.add_field(name="?timers", value="Shows a list of all timers you have set with **?timein** in this server.", inline=False)
            help_embed.add_field(name="?stoptimers", value="Stops all your timers on this server! Use with care. *(Squash was too lazy to program stopping select timers)*", inline=False)
            help_embed.set_footer(text=f"Requested by {message.author}.", icon_url=message.author.avatar)
            await message.channel.send(embed=help_embed)

        else:
            await message.channel.send(f"Sorry, **\"{category}\"** doesn't seem to be an existing category. Look at **?help** and try again!")

    @commands.command(name = "version",
                    description = "Displays bot version.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def version(self, ctx: commands.Context):
        await ctx.channel.send(f"This is **SquashBot v0.1**!")
