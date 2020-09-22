import os
import json
from datetime import datetime, timedelta
from discord.ext import commands
import discord
from discord import Embed

DATETIME_FORMAT = '%Y-%m-%d %H:%M'

class CoffeeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def update_data(self, users, user):
        DATETIME_DEFAULT = datetime(2000, 1, 1, 0, 0).strftime(DATETIME_FORMAT)
        
        # initialize user if not in json file yet
        if not str(user.id) in users:
            users[user.id] = {}
            users[user.id]['name'] = str(user)
            users[user.id]['nickname'] = str(user.nick)
            users[user.id]['beans'] = 0
            users[user.id]['last_daily'] = DATETIME_DEFAULT
            users[user.id]['last_rob'] = DATETIME_DEFAULT
            users[user.id]['inventory'] = {}

    async def migrate_user(self, users, user):

        #users[str(user.id)['nickname'] = str(user.nick)
        try:
            users[str(user.id)]['net_gamble'] = 0
        except KeyError as e:
            pass
    
    @staticmethod
    def get_beans(users, user):
        return users[str(user.id)]['beans']
    
    @staticmethod
    def get_net_gamble(users, user):
        return users[str(user.id)]['net_gamble']


    @staticmethod
    def get_lb(users):
        lb = []
        for user in users:
            if users[user]['beans'] > 0:
                lb.append((users[user]['name'], users[user]['beans']))
        leaderboard = sorted(lb, key=lambda v: v[1], reverse=True)
        return leaderboard


    @staticmethod
    def next_daily_available_in(users, user):
        next_daily = datetime.strptime(users[str(user.id)]['last_daily'], DATETIME_FORMAT) + timedelta(hours=22)
        now = datetime.now()
        time_diff = next_daily - now
        return (time_diff.total_seconds() / 3600)

    async def add_beans(self, users, user, amount):
        try:
            users[str(user.id)]['beans'] = int(CoffeeCog.get_beans(users, user)) + amount
        except Exception as e:
            print('exception', e)
            pass
    async def update_net_gamble(self, users, user, amount):
        try:
            users[str(user.id)]['net_gamble'] = int(CoffeeCog.get_net_gamble(users, user)) + amount
        except Exception as e:
            print('exception', e)
            pass
    
    async def transfer_beans(self, users, sender, recipient, amount):
        try:
            users[str(sender.id)]['beans'] = int(users[str(sender.id)]['beans']) - amount
            users[str(recipient.id)]['beans'] = int(users[str(recipient.id)]['beans']) + amount
        except Exception as e:
            print('exception', e)
            pass

    async def reset_time(self, users, user, attribute):
        attributes = ['last_daily', 'last_rob']
        if attribute in attributes:
            users[str(user.id)][attribute] = datetime.now().strftime(DATETIME_FORMAT)

def setup(bot):
    bot.add_cog(CoffeeCog(bot))