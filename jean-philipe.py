import json
import os
import sys
import discord

config = {
    # Don't add your token here. Run the app and coplete the config.json file.
    'discord_token': 'YOUR_TOKEN',
}

# create a new config file
def create_config():
    with open('config.json', 'w') as config_file:
        config_file.write(json.dumps(config, sort_keys=True, indent=4, separators=(',', ': ')))
    sys.exit('No Config found.\nconfig.json was created. Please add your informations in it')


# import configuration
def load_config():
    if not os.path.exists('config.json'):
        create_config()

    config_loaded = {}
    with open('config.json') as config_file:
        config_loaded = json.loads(config_file.read())
    
    for key, value in config_loaded.items():
        config[key] = value


if __name__ == "__main__":
    load_config()
