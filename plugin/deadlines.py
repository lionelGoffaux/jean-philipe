from discord.ext import commands


class Deadlines(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("deadlines set up...")

    @commands.command()
    async def add(self, ctx):
        await ctx.send("added")


def setup(bot: commands.Bot):
    bot.add_cog(Deadlines(bot))
