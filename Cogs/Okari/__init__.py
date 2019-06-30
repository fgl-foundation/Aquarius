import discord
from discord.ext import commands
import os
from . import SQLWorker
from . import PictureCreator

class Okari(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="count", help="Выводит статистику посещения сервера, а именно сколько пришло, сколько осталось и сколько ушло человек.",brief="Cтатистика посещения сервера")
    async def count(self,ctx):
        stat=SQLWorker.GetStat(ctx.guild.id)
        embed=discord.Embed(title="Я запомнил "+str(stat[0])+" чел.", description="На данный момент")
        embed.add_field(name="Ушло", value=str(stat[1])+" чел.")
        embed.add_field(name="Осталось", value=str(stat[2])+" чел." )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:        
            path=PictureCreator.AddMember(member)
            file=discord.File(path,filename="MemJoin.png")
            await member.guild.get_channel(SQLWorker.GetInfoChan(member.guild.id)).send(file=file)
            os.remove(path)
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        try:
            await member.guild.fetch_ban(member)
        except discord.NotFound:
            if not member.bot:
                path=PictureCreator.LostMember(member)
                file=discord.File(path,filename="MemRemove.png")
                await member.guild.get_channel(SQLWorker.GetInfoChan(member.guild.id)).send(file=file)
                os.remove(path)

def setup(client):
    client.add_cog(Okari(client))