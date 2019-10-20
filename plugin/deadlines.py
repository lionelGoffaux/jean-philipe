import sqlite3
import discord
import asyncio
import re
import os
from datetime import date
from discord.ext import commands

DB = 'deadlines.sql3'

conn = sqlite3.connect(DB)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS `deadlines`
                (`serverId` BIGINT NOT NULL,
                 `taskId` SMALLINT NOT NULL,
                 `date`       DATE NOT NULL,
                 `task`  VARCHAR(255) NOT NULL,
                 `done`     BOOLEAN DEFAULT 0,
                 
                 CONSTRAINT `dl_pk` PRIMARY KEY (`serverId`, `taskId`))
            ''')

conn.commit()
conn.close()


class Deadlines(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.check())
        print("deadlines set up...")

    @commands.command(aliases=['add'])
    async def addt(self, ctx: discord.ext.commands.context.Context, date: str, *, task: str):

        if not re.search('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date):
            await ctx.send("date format is not good\nplease use YYYY-MM-DD")
            return

        conn = sqlite3.connect(DB)
        c = conn.cursor()

        id = 0

        c.execute("""SELECT MAX(`taskId`) FROM `deadlines` WHERE `serverId`=?""",
                  (ctx.guild.id,))
        data = c.fetchall()
        if len(data) != 0:
            id = data[0][0] + 1

        c.execute('''INSERT INTO `deadlines`(serverId, taskId, date, task)
                VALUES(?, ?, ?, ?)
        ''', (ctx.guild.id, id, date, task))
        await ctx.send("task added")

        conn.commit()
        conn.close()

    @commands.command(aliases=['ls', 'todo'])
    async def lstodo(self, ctx: discord.ext.commands.context.Context, limit=5):
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute('''SELECT `taskId`, `date`, `task` FROM `deadlines` WHERE `serverId` = ? AND `done`=0 ORDER BY `date` LIMIT ?''',
                  (ctx.guild.id, limit))
        ronws = c.fetchall()

        conn.close()
        if len(ronws) == 0:
            return

        message = "```\n"
        for r in ronws:
            message += f'> ({r[1]}) {r[2]:35} [{r[0]}]\n'
        message += "```\n"

        await ctx.send(message)

    @commands.command()
    async def done(self, ctx: discord.ext.commands.context.Context, taskId: int):
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute('''UPDATE `deadlines` SET `done`=1 WHERE `taskId`=? AND `serverId`=?''', (taskId, ctx.guild.id))

        conn.commit()
        conn.close()

        await ctx.send("gg wp!")

    async def check(self):
        time_sleep = 600
        while True:
            cur_date = date.today().strftime("%Y-%m-%d")

            if 'deadlines.log' not in os.listdir('./'):
                f = open('deadlines.log', 'w')
                f.close()

            with open('deadlines.log') as log:
                if log.read() == cur_date:
                    await asyncio.sleep(time_sleep)
                    continue

            with open('deadlines.log', 'w') as log:
                log.write(cur_date)

            for guild in self.bot.guilds:
                conn = sqlite3.connect(DB)
                c = conn.cursor()

                c.execute('''SELECT `taskId`, `date`, `task` FROM `deadlines` WHERE `date` <= ? AND `serverId` = ? AND `done`=0''',
                          (cur_date, guild.id))

                ronws = c.fetchall()
                conn.close()

                if len(ronws) == 0:
                    continue

                message = "```----------TASK FOR TODAY----------\n\n"
                for r in ronws:
                    message += f'> ({r[1]}) {r[2]:35} [{r[0]}]\n'
                message += "```\n"

                await guild.text_channels[0].send(message)

            await asyncio.sleep(time_sleep)


def setup(bot: commands.Bot):
    cogs = Deadlines(bot)
    bot.add_cog(cogs)
