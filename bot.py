import discord
import asyncio
import os
import re
import json
import random
import datetime
import logging
from dotenv import load_dotenv
from discord.ext import commands, timers, tasks
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
user_data = 'users.json'
# LOGGING
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
log_path = os.path.join(os.getcwd(), 'bot.log')
logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()

print('starting up bot...')
bot = commands.Bot(command_prefix='--')

cogs = ['music', 'coffee']

def get_users(file):
    with open(file, 'r', encoding='utf8') as f:
        users = json.load(f)
    return users

def save_users(file, users):
    with open(file, 'w', encoding='utf8') as f:
        users = json.dump(users, f, indent=4, ensure_ascii=False)


@bot.event
async def on_ready():
    ready = f'\==== [{bot.user.name} has connected to Discord] ====/'
    for cog in cogs:
        bot.load_extension(f'cogs.{cog}')
        print(f'> Loaded {cog} cog')
    print(ready)
    logger.info(ready)

    loop_beans.start()
    print('loop_beans started')

@bot.event
async def on_member_join(member):
    '''
    Automatically assign new members 'Customer' role
    '''
    logger.info(f'{member} joined the server.')
    role = get(member.guild.roles, name='Customer')
    await member.add_roles(role)
'''
async def secret_message(message):
    name = message.author
    if name == 'adri' and '' in message:
        resp = ''
    if name == 'maqic' and '' in message:
        resp = ''
    if name == 'Beianp' and '' in message:
        resp = ''
    if name == 'ctrl_alt_del' and '' in message:
        resp = ''
    if name == 'adri' and '' in message:
        resp = ''
    if name == 'adri' and '' in message:
        resp = ''
    if name == 'adri' and '' in message:
        resp = ''
    if name == 'adri' and '' in message:
        resp = ''
    if name == 'adri' and '' in message:
        resp = ''
    if name == 'adri' and '' in message:
        resp = ''
'''
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    msg = message.content
    welcome_responses = ['You\'re very welcome.', 'My pleasure.', 'Of course.']
    if all(word in msg.lower() for word in ['thanks', 'robo', 'waiter']):
        await message.channel.send(random.choice(welcome_responses))

    unwelcome_responses = ['Much to your dismay, crime is not the solution.']
    if any(word in msg.lower() for word in ['overthrow', 'revolt', 'assassinate', 'steal', 'stab','kill']):
        await message.channel.send(random.choice(unwelcome_responses))

    resp = ['Hmm, you seem anxious or overexcited. Perhaps try --setmood rain.', 'Everything will be alright.']
    if bool(re.match(r'^[A-Z ]{15,100}$', msg)):
        await message.channel.send(random.choice(resp))

    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)
    
    await coffee_cog.update_data(users, message.author)
    await coffee_cog.add_beans(users, message.author, 1)
    
    save_users(user_data, users)
    await bot.process_commands(message)
'''
@bot.event
async def on_error(event, *args, **kwargs):
    if event == 'on_message':
        logger.warning(f'ERROR in: {event}')
'''



@bot.command(name='beans')
async def beans(ctx):
    '''
    Check how many beans you have.
    '''
    user = ctx.message.author
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)

    beans = coffee_cog.get_beans(users, user)
    await ctx.message.delete()

    embed = discord.Embed(color=discord.Color.greyple())
    embed.description = f':coffee: {user.mention}, you have {beans} coffee beans.'

    await ctx.send(embed=embed)
    logger.info(f'{user} requested to see their beans in {ctx.channel.name}')
@beans.error
async def beans_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: beans | ERROR: {error}')



@bot.command(name='giftbeans', aliases=['gb'])
async def giftbeans(ctx, amount: int, target):
    '''
    Send someone some beans :)
    '''
    user = ctx.message.author
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)

    if coffee_cog.get_beans(users, user) >= amount > 0:
        recipient = ctx.message.mentions[0]
        await coffee_cog.update_data(users, recipient)
        await coffee_cog.transfer_beans(users, user, recipient, amount)
        await ctx.send(f'{user.mention} has gifted {recipient.mention} {amount} coffee beans.')
        logger.info(f'{user} gifted {recipient} {amount} coffee beans.')
    else:
        await ctx.send('Unfortunately, you cannot gift that number of beans.')

    save_users(user_data, users)
async def giftbeans_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('You did the command wrong.')
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: giftbeans | ERROR: {error}')



@bot.command(name='gamble', aliases=['g'])
async def gamble(ctx, amount: int, color):
    '''
    Gamble some beans; bet on a color. You must gamble over 50 beans.
    --gamble <amount> <color>
    Colors are red, black, or green. 
    Red/black has 45% chance, green has 10% but gives 7 times your bet amount.
    '''
    user = ctx.message.author
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)

    allowed_channels = ['lotto', 'the-room-where-it-happens']
    if not ctx.channel.name in allowed_channels:
        await ctx.send('You cannot gamble here.')
        return
    
    colors = ['red', 'black', 'green']
    rolename = 'Unlucky'

    if coffee_cog.get_beans(users, user) >= amount >= 50:
        if color in colors:
            await coffee_cog.update_data(users, user)
            await coffee_cog.add_beans(users, user, -1*amount)

            roll = random.randint(1, 101)
            if roll < 46:
                result = 'red'
            elif roll < 91:
                result = 'black'
            else:
                result = 'green'

            if color == result and result == 'green':
                await coffee_cog.add_beans(users, user, 8*amount)
                msg = 'You won the jackpot!'
            elif color == result:
                await coffee_cog.add_beans(users, user, 2*amount)
                msg = 'You won!'
            else:
                msg = f'It landed on {result}. You lost...'
                # get the unlucky role if you gamble over 10k and lose
                if amount >= 10000 and not rolename in [roles.name for roles in user.roles]: 
                    role = get(user.guild.roles, name=rolename)
                    await user.add_roles(role)

            beans = coffee_cog.get_beans(users, user)
            await ctx.send(f'{msg} You now have {beans} coffee beans.')
        else:
            await ctx.send('Invalid color.')
    else:
        await ctx.send('Unfortunately, you cannot gamble that number of beans.')

    save_users(user_data, users)
@gamble.error
async def gamble_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: gamble | ERROR: {error}')



@bot.command(name='dailybeans', aliases=['daily'])
async def dailybeans(ctx):
    '''
    Collect your daily 200 coffee beans.
    Available every 22 hours.
    '''
    daily_amount = 200

    user = ctx.message.author
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)
    
    next_avail = coffee_cog.next_daily_available_in(users, user) 
    if next_avail <= 0:
        await coffee_cog.add_beans(users, user, daily_amount)
        await coffee_cog.reset_time(users, user, 'last_daily')

        beans = coffee_cog.get_beans(users, user)
        await ctx.send(f'Congratulations! You now have {beans} coffee beans.')
        logger.info(f'{user} got their daily coffee beans.')
    else:
        await ctx.send(f'You can get your daily beans in {round(next_avail, 1)} hours.')

    save_users(user_data, users)



@bot.command(name='tip')
async def tip(ctx, amount: int):
    '''
    Tip Robo Waiter some coffee beans.
    '''
    user = ctx.message.author
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)

    if coffee_cog.get_beans(users, user) >= amount > 0:
        await coffee_cog.add_beans(users, user, -1*amount)

        thanks = ['Much appreciated.', 'Much obliged.']
        await ctx.send(random.choice(thanks))
        logger.info(f'{user} tipped {amount} coffee beans.')
    else:
        await ctx.send('Unfortunately, you cannot tip that number of beans.')

    save_users(user_data, users)
async def giftbeans_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('You did the command wrong.')
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: tip | ERROR: {error}')




@bot.command(name='leaderboard', aliases=['lb'])
async def leaderboard(ctx):
    '''
    See the coffee bean top leaderboard.
    '''
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)
    await ctx.message.delete()
    
    lb = coffee_cog.get_lb(users)
    
    embed = discord.Embed(color=discord.Color.orange())
    embed.title = ':coffee: *Coffee Bean Leaderboards* :coffee:'
    desc = ''
    for i, (name, beans) in enumerate(lb):
        if i < 12 and i != 0: # really shitty code here but whatever
            desc += f'{i}.   **{name}** - *{beans} beans*\n'
            #embed.add_field(name=f'{i+1}. {name} - {beans} beans', value=f' ', inline=False)
    embed.description = desc
    await ctx.send(embed=embed)
    logger.info(f'{ctx.message.author} requested to see the leaderboard in {ctx.channel.name}')



@bot.command(name='shop')
async def shop(ctx):
    '''
    The coffee shop.
    '''
    await ctx.message.delete()

    embed = discord.Embed(color=discord.Color.teal())
    embed.title = ':coffee: *Coffee Shop* :coffee:'
    embed.set_thumbnail(url=ctx.guild.icon_url)

    items = [
        ('Change nickname', '--changenick |\n 50 coffee beans'),
        ('Nuke someone', '--nuke |\n 300 coffee beans'),
        ('Become a regular!', '--regular |\n 1000 coffee beans'),
        ('Become a caffeine addict!', '--caffeineaddict |\n 7500 coffee beans'),
        ('Become a pumpkin spice latte!', '--pumpkinspice |\n 40,000 coffee beans')
    ]

    for name, value in items:
        embed.add_field(name=name, value=value, inline=True)

    await ctx.send(embed=embed)
    logger.info(f'{ctx.message.author} requested to see the shop in {ctx.channel.name}')



@bot.command(name='changenick', aliases=['cn'])
async def changenick(ctx, nickname):
    '''
    Change your nickname for 50 beans.
    --changenick <nick>
    '''
    cost = 50
    user = ctx.message.author

    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)
    
    if str(user.id) not in users:
        logger.warning(f'{user} is NOT in JSON file but is trying to change nickname.')
    
    if users[str(user.id)]['beans'] >= cost:
        await user.edit(nick=nickname)
        await coffee_cog.add_beans(users, user, -1*cost)
        await ctx.send(f'Success {user.mention}!')
    else:
        ctx.send(f'You do not have enough beans; you need {count}.')

    save_users(user_data, users)
@changenick.error
async def changenick_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: changenick | ERROR: {error}')



async def buy_role(ctx, cost, rolename):
    '''
    Helper function for roles.
    '''
    user = ctx.message.author
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)
    
    if str(user.id) not in users:
        logger.warning(f'{user} is NOT in JSON file but is trying to buy the Regular role.')

    if users[str(user.id)]['beans'] >= cost:
        if not rolename in [roles.name for roles in user.roles]:
            role = get(user.guild.roles, name=rolename)
            await user.add_roles(role)

            await coffee_cog.add_beans(users, user, -1*cost)
            beans = coffee_cog.get_beans(users, user)
            await ctx.send(f'Congrats! You are now a {rolename}. You now have {beans} coffee beans.')
            logger.info(f'{user} bought the {rolename} role.')
        else:
            await ctx.send(f'You already are a {rolename}.')
    else:
        await ctx.send(f'You do not have enough beans; you need {cost}.')

    save_users(user_data, users)

@bot.command(name='regular')
async def regular(ctx):
    '''
    Obtain the 'Regular' role in exchange for 1000 beans.
    '''
    cost = 1000
    rolename = 'Regular'

    await buy_role(ctx, cost, rolename)
@regular.error
async def regular_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: regular | ERROR: {error}')

@bot.command(name='caffeineaddict')
async def caffeineaddict(ctx):
    '''
    Obtain the 'Caffeine Addict' role in exchange for 7500 beans.
    '''
    cost = 7500
    rolename = 'Caffeine Addict'

    await buy_role(ctx, cost, rolename)
@caffeineaddict.error
async def caffeineaddict_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: caffeineaddict | ERROR: {error}')

@bot.command(name='pumpkinspice')
async def pumpkinspice(ctx):
    '''
    Obtain the 'Pumpkin Spice Latte' role in exchange for 40,000 beans.
    '''
    cost = 40000
    rolename = 'Pumpkin Spice Latte'

    await buy_role(ctx, cost, rolename)
@pumpkinspice.error
async def pumpkinspice_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: pumpkinspice | ERROR: {error}')





@bot.command(name='migrate')
@commands.has_any_role('Brewmaster')
async def migrate(ctx):
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)

    logger.info(f'{ctx.message.author} MIGRATED.')
    await ctx.send('Migrating...')

    for member in ctx.guild.members:
        if not member == bot.user:
            await coffee_cog.update_data(users, member)
    
    save_users(user_data, users)



@tasks.loop(seconds=30.0)
async def loop_beans():
    '''
    Every 30 seconds gives everyone in vc 1 bean.
    '''
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)

    for guild in bot.guilds:
        if guild.name == GUILD:
            server = guild
            break
    members = server.members
    for member in members:
        if member.voice and member != bot.user:
            await coffee_cog.update_data(users, member)
            await coffee_cog.add_beans(users, member, 1)
    save_users(user_data, users)



@bot.command(name='clear')
@commands.has_any_role('Brewmaster', 'Caffeine Addict', 'Pumpkin Spice Latte')
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
    logger.info(f'{ctx.message.author} cleared {ctx.channel.name}.')



@bot.command(name='nuke')
@commands.has_any_role('Brewmaster', 'Regular', 'Caffeine Addict')
async def nuke(ctx, nuke_count: int, *targets):
    '''
    Sends specified number of nuke dms to target(s) for 300 credits.
    Must be 'Brewmaster' or 'Regular' to use this command.
    '''
    user = ctx.message.author
    coffee_cog = bot.get_cog('CoffeeCog')
    users = get_users(user_data)

    cost = 300
    NUKE_LIMIT = 30
    allowed_channels = ['robo-waiter', 'the-room-where-it-happens']

    if nuke_count < 0:
        return

    if coffee_cog.get_beans(users, user) < cost:
        await ctx.send('You are too poor to nuke.')
        return
    
    await coffee_cog.update_data(users, user)
    await coffee_cog.add_beans(users, user, -1*cost)

    if ctx.channel.name in allowed_channels:
        nuke_amount = NUKE_LIMIT if nuke_count > NUKE_LIMIT else nuke_count
        if ctx.message.mentions:
            await ctx.send(':rotating_light: NUKE INITIATED :rotating_light:')
            for target_member in ctx.message.mentions:
                for i in range(nuke_amount):
                    await target_member.send(f':bomb: YOU HAVE BEEN NUKED BY {user}!!! :bomb:')
                logger.info(f'{user} nuked {target_member} {nuke_amount} times from channel: {ctx.channel.name}.')
        else:
            await ctx.send('No targets specified.')
            logger.info(f'{user} tried to nuke with no targets in: {ctx.channel.name} and failed.')
    else:
        await ctx.send('You do not have access to the launch system.')
        logger.info(f'{user} tried to nuke in an invalid channel: {ctx.channel.name} and failed.')
    save_users(user_data, users)
@nuke.error
async def nuke_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Invalid launch code.')
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('ERROR: Sorry, your nukes do not reach that far.')
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send('I\'m afraid you do not have access to nukes. Sincere apologies.')
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: nuke | ERROR: {error}')




####################################################################
#=======================NON COFFEE STUFF HERE=======================
####################################################################



@bot.command(name='rng')
async def rng(ctx, start: int, end: int):
    '''
    Generates a random integer in interval [start, end].
    '''
    embed = discord.Embed()
    embed.title = 'Your Random Number'
    embed.description = random.randint(start, end)
    await ctx.send(embed=embed)
@rng.error
async def rng_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: rng | ERROR: {error}')

@bot.command(name='bday')
@commands.has_any_role('Brewmaster')
async def bday(ctx):
    '''
    Plays the happy birthday song.
    '''
    video = 'happy birthday'
    music_cog = bot.get_cog('MusicCog')
    await music_cog.join(ctx)
    await music_cog.play(ctx, query=video)


@bot.command(name='quote')
async def quote(ctx, quote_type):
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
async def quote_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: quote | ERROR: {error}')



@bot.command(name='setmood', aliases=['mood'])
async def setmood(ctx, mood):
    '''
    Outputs a scenic setting exposition followed by joining vc and playing matching soundscape.
    Perfect for sleeping or studying.
    Join a voice channel for the full effect.
    Options include: 'fall', 'nature', 'rain', 'summer', 'jazz', 'synthwave'
    '''
    moods = ['fall', 'nature', 'rain', 'summer', 'jazz', 'synthwave']
    member = ctx.message.author
    
    if mood in moods:
        with open(f'mood/{mood}/moods.txt','r', encoding='utf8') as f:
            scenes = f.readlines()
        random_int = random.randint(0,len(scenes)-1)
        
        embed = discord.Embed()
        embed.description = f'*{scenes[random_int][:-1]}*'

        await ctx.send(embed=embed)
        logger.info(f'{ctx.message.author} set mood to: {mood} in {ctx.channel.name}.')

        if member and member.voice:
            with open(f'mood/{mood}/urls.txt','r', encoding='utf8') as f:
                urls = f.readlines()
                video = urls[random_int].rstrip()
            music_cog = bot.get_cog('MusicCog')
            await music_cog.join(ctx)
            logger.info(f'Robo Waiter joined or is in: {member.voice.channel}.')
            await music_cog.play(ctx, query=video)
            logger.info(f'{ctx.message.author} added {video} to the queue.')
        else:
            await ctx.send('Join a voice channel for the full effect.')
    else:
        await ctx.send(f'Mood "{mood}" not found.')
@setmood.error
async def setmood_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that mood.')
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: setmood | ERROR: {error}')



@bot.command(name='ustoopid')
async def ustoopid(ctx):
    '''
    A cleaner way to point out another's intelligence or lack thereof.
    '''
    await ctx.message.delete()
    await ctx.send('Not quite the sharpest tool in the shed I see.')

@bot.command(name='yep')
async def yep(ctx):
    '''
    When you need Robo Waiter to confirm.
    '''
    choices = ['Indubitably.', 'Certainly.', 'Indeed.', 'Undoubtedly.', 'Assuredly.']
    await ctx.message.delete()
    await ctx.send(random.choice(choices))

@bot.command(name='helpme')
async def helpme(ctx):
    '''
    Sends a helpful link when someone calls for help.
    '''
    embed = discord.Embed(color=discord.Color.green())
    embed.title = 'Somebody call for help?'
    embed.description = '[Try this helpful link.](https://www.youtube.com/watch?v=dQw4w9WgXcQ)'
    await ctx.send(embed=embed)
@helpme.error
async def helpme_error(ctx, error):
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: helpme | ERROR: {error}')



@bot.command(name='sendmelody', aliases=['sm'])
async def sendmelody(ctx, target):
    '''
    Send a nice melody somebody's way if they're in a voice channel.
    '''
    if target and len(ctx.message.mentions) == 1:
        member = ctx.message.mentions[0]
        if member.voice:
            music_cog = bot.get_cog('MusicCog')
            await music_cog.join_member(ctx, member)
            logger.info(f'Robo Waiter joined or is in: {member.voice.channel}.')
            await music_cog.play(ctx, query='Replay [Official Music Video] - Iyaz')
            logger.info(f'{ctx.message.author} queued SHAWTYS LIKE A MELODY for {member}.')
        else :
            await ctx.send('Unfortunately, your target is not in a voice channel.')
@sendmelody.error
async def sendmelody_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You must specify a target.')
    if isinstance(error, commands.BadArgument):
        await ctx.send('I\'m sorry, but your target is invalid.')
    logger.warning(f'AUTHOR: {ctx.message.author} | METHOD: sendmelody | ERROR: {error}')


if __name__ == '__main__':
    bot.run(TOKEN)
