import json
import os
import sys
import discord
from discord.ext import commands

#
# CONFIG
#

config = {
    # Don't add your token here. Run the app and complete the config.json file.
    'discord_token': 'YOUR_TOKEN',
    'admins': []
}


# create a new config file
def create_config():
    with open('config.json', 'w') as config_file:
        config_file.write(json.dumps(config, indent=4, separators=(',', ': ')))
    sys.exit('No Config found.\nconfig.json was created. Please add your informations in it')


# import configuration
def load_config():
    if not os.path.exists('config.json'):
        create_config()

    with open('config.json') as config_file:
        config_loaded = json.loads(config_file.read())

    for key, value in config_loaded.items():
        config[key] = value


#
# BOT 
#


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("bot started and ready to work...")


@bot.command()
async def ping(ctx: discord.ext.commands.context.Context):
    await ctx.send('pong')




#
# Plugins
#


def load_plugins(client: commands.Bot):
    for file in os.listdir(os.path.join(".", "plugin")):
        if file.endswith('.py'):
            client.load_extension(f"plugin.{file[:-3]}")


if __name__ == "__main__":
    load_config()
    load_plugins(bot)
    bot.run(config['discord_token'])
