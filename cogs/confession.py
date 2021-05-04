import asyncio
import discord
from discord.ext import commands
from discord.utils import get

class ConfessionCog(commands.Cog, name="Confessions"):
    def __init__(self, bot):
        self.bot = bot
        self.guild = get(self.bot.guilds, name='Coffee Shop')
        self.channel = get(self.guild.channels, name='expresso-corner')
        self.log_channel = get(self.guild.channels, name='logs')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if not isinstance(message.channel, discord.channel.DMChannel):
            return
        msg = message.content
        if not msg.startswith('confess: '):
            return
        confession = msg[9:]
        embed = discord.Embed()
        embed.title = '*Confession*'
        embed.description = confession
        await self.channel.send(embed=embed)
        await self.log_channel.send(f'from: message.author', embed=embed)

    @commands.command(name='confess')
    async def confess(self, ctx):
        await ctx.send('Send me a direct message starting with "confess: " followed by your confession.')

def setup(bot):
    bot.add_cog(ConfessionCog(bot))
