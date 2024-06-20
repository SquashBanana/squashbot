import discord

class HourTimer:
    def __init__(self, start_time, end_time, active_user, active_guild, active_channel):
        self.is_active: bool = True
        self.start_time: int = start_time
        self.end_time: int = end_time
        self.active_user: discord.User = active_user
        self.active_guild: discord.Guild = active_guild
        self.active_channel: discord.abc.Messageable = active_channel