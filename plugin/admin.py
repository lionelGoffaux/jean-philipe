import json
import discord
from discord.ext import commands


with open('config.json') as config_file:
    config = json.loads(config_file.read())


def is_admin(ctx: discord.ext.commands.context.Context):
    return ctx.author.id in config['admins']


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Admin set up...")

    @commands.command()
    @commands.check(is_admin)
    async def logout(self, ctx: discord.ext.commands.context.Context):
        '''logout the bot properly'''
        print("logout...")
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Admin(bot))
