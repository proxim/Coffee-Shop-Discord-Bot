import asyncio
import os
import json
import logging
import random
from datetime import datetime, timedelta
from discord.ext import commands
import discord
from discord import Embed

DATETIME_FORMAT = '%Y-%m-%d %H:%M'
# LOGGING
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
log_path = os.path.join(os.getcwd(), 'bot.log')
logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dopamine')
    async def dopamine(self, ctx):
        '''
        Get a hit of dopamine, with help from Robo.
        '''
        await asyncio.sleep(random.randint(5, 10))
        await ctx.send(f'{ctx.message.author.mention} <3')


    @commands.command(name='8ball')
    async def eball(self, ctx):
        '''
        Get a yes or no from Robo Waiter.
        '''
        responses = ['Most certainly.', 'Most definitely not.']
        await ctx.message.delete()
        await ctx.send(random.choice(responses))
    @eball.error
    async def eball_error(self, ctx, error):
        logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: rng | ERROR: {error}')

    @commands.command(name='rng')
    async def rng(self, ctx, start: int, end: int):
        '''
        Generates a random integer in interval [start, end].
        '''
        embed = discord.Embed()
        embed.title = 'Your Random Number'
        embed.description = random.randint(start, end)
        await ctx.send(embed=embed)
    @rng.error
    async def rng_error(self, ctx, error):
        logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: rng | ERROR: {error}')

    @commands.command(name='quote')
    async def quote(self, ctx, quote_type):
        '''
        Outputs a random quote of specified type.
        Great for when you're bored or feeling experimental.
        Options include: 'funny', 'motivational'
        '''
        quote_types = ['funny', 'motivational']
        if quote_type in quote_types:
            with open(f'quotes/{quote_type}_quotes.txt', 'r', encoding='utf8') as f:
                quotes = f.readlines()
            random_int = random.randint(0,len(quotes)-1)

            if quote_type == 'funny':
                if random_int % 2 == 1:
                    random_int -= 1
                q = f'{quotes[random_int]}{quotes[random_int+1]}'
            elif quote_type == 'motivational':
                q = f'{quotes[random_int]}'

            await ctx.send(q)
            logger.info(f'{ctx.message.author} requested a {quote_type} quote in {ctx.channel.name}.')
        else:
            await ctx.send(f'My apologies. I couldn\'t find a "{quote_type}" quote.')
    @quote.error
    async def quote_error(self, ctx, error):
        logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: quote | ERROR: {error}')


    @commands.command(name='ustoopid')
    async def ustoopid(self, ctx):
        '''
        A cleaner way to point out another's intelligence or lack thereof.
        '''
        await ctx.message.delete()
        await ctx.send('Not quite the sharpest tool in the shed I see.')

    @commands.command(name='yep')
    async def yep(self, ctx):
        '''
        When you need Robo Waiter to confirm.
        '''
        choices = ['Indubitably.', 'Certainly.', 'Indeed.', 'Undoubtedly.', 'Assuredly.']
        await ctx.message.delete()
        await ctx.send(random.choice(choices))

    @commands.command(name='helpme')
    async def helpme(self, ctx):
        '''
        Sends a helpful link when someone calls for help.
        '''
        embed = discord.Embed(color=discord.Color.green())
        embed.title = 'Somebody call for help?'
        embed.description = '[Try this helpful link.](https://www.youtube.com/watch?v=dQw4w9WgXcQ)'
        await ctx.send(embed=embed)
    @helpme.error
    async def helpme_error(self, ctx, error):
        logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: helpme | ERROR: {error}')


    @commands.command(name='cap')
    async def cap(self, ctx):
        '''
        Stop the cap.
        '''
        await ctx.message.delete()
        msg = await ctx.send('Halt thy headwear.')
        emoji = '\N{billed cap}'
        await msg.add_reaction(emoji)

    @commands.command(name='doubt')
    async def doubt(self, ctx):
        '''
        Press X to doubt.
        '''
        await ctx.message.delete()
        msg = await ctx.send('Press X to doubt.')
        emoji = '\N{cross mark}'
        await msg.add_reaction(emoji)


def setup(bot):
    bot.add_cog(MiscCog(bot))