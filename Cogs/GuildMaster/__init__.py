import discord
from discord.ext import commands
import datetime
from . import SQLWorker

class GuildMaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            jr= SQLWorker.GetJoinRole(member.guild.id)
            if jr:
                await member.add_roles(member.guild.get_role(int(jr)))

            for i in SQLWorker.GetRoles(member.guild.id,member.id):
                await member.add_roles(member.guild.get_role(int(i[0])))

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if len(before.roles)< len(after.roles):
            for i in after.roles:
                if not i in before.roles and not SQLWorker.CheckRole(after.guild.id,after.id,i.id):
                    SQLWorker.AddRoles(after.guild.id,after.id,i.id)
        if len(before.roles)> len(after.roles):
            for i in before.roles:
                if not i in after.roles:
                    SQLWorker.DelRole(i.id)


    @commands.Cog.listener()
    async def on_guild_emojis_update(self,guild, before, after):
        if len(before)< len(after):
            for i in after:
                if not i in before and not SQLWorker.CheckEmoji(guild.id,i.id):
                    SQLWorker.AddEmoji(guild.id,i.id)
        if len(before)> len(after):
            for i in before:
                if not i in after:
                    SQLWorker.DelEmoji(i.id)

def setup(client):
    client.add_cog(GuildMaster(client))