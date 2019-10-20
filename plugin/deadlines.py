import sqlite3
import discord
from datetime import date
from discord.ext import commands, tasks

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
        print("deadlines set up...")

    @commands.command()
    async def addTask(self, ctx: discord.ext.commands.context.Context, id: int, date: str, *, task: str):
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        try:
            c.execute('''INSERT INTO `deadlines`(serverId, taskId, date, task)
                    VALUES(?, ?, ?, ?)
            ''', (ctx.guild.id, id, date, task))
            await ctx.send("task added")
        except sqlite3.IntegrityError as e:
            await ctx.send("this task id already exists")

        conn.commit()
        conn.close()

    @commands.command()
    async def listToDo(self, ctx: discord.ext.commands.context.Context, limit=5):
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute('''SELECT `taskId`, `date`, `task` FROM `deadlines` WHERE `serverId` = ? AND `done`=0 ORDER BY `date` LIMIT ?''',
                  (ctx.guild.id, limit))
        ronws = c.fetchall()

        conn.close()
        message = "```\n"
        for r in ronws:
            message += f'> ({r[1]}) {r[2]:35} [{r[0]}]\n'
        message += "```\n"

        await ctx.send(message)

    @commands.command()
    async def done(self, ctx: discord.ext.commands.context.Context, taskId: int):
        conn = sqlite3.connect(DB)
        c = conn.cursor()

        c.execute('''UPDATE `deadlines` SET `done`=1 WHERE `taskId`=?''', (taskId,))

        conn.commit()
        conn.close()

    @tasks.loop(seconds=10)
    async def alert(self):
        cur_date = date.today().strftime("%Y-%m-%d")
        print('check log')
        with open('deadlines.log') as log:
            if log.read() == cur_date:
                return

        with open('deadlines.log', 'w') as log:
            log.write(cur_date)

        print('rappel', cur_date)


def setup(bot: commands.Bot):
    bot.add_cog(Deadlines(bot))
