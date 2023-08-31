# PungeounBot

A small bot for a private discord server. 

## Features

**Slash commands:**
### _Roll_
**Description:** Standard D&D dice roll (1d2, 3d6 etc)
**Signature**: /roll [dice] 

### _Add user_
**Description:** Add your own user for timezone-based tools

**Signature:** /add_user [Europe / America] [City]

### _Suggest time_
**Description:** Suggest a time and see what time it is for everybody else

**Signature:** /suggest_time [yyyy-mm-dd hh:MM]

## Libraries & dependencies
* Made using [discord.py by Rapptz](https://github.com/Rapptz/discord.py/tree/master)
* Written in Python 3.10.11
* See requirements.txt for all requirements and use `pip install -r requirements.txt`

## How to use
1. Clone the repo and navigate to it
2. Add a `.secrets/` folder to the root directory of your project `mkdir .secrets/`
    1. Add two files: `touch .secrets/config.json` and `touch .secrets/users.json`
    2. Add an empty JSON object to `users.json` or add a list of users with their timezone if you don't want to add them with commands
    3. Follow the example for the config. You need a discord bot token and a guild ID for testing  
3. Run using `python3.10 PungeounBot.py` or the Dockerfile provided
