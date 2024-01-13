# gremblebot
This is the repo for gremblebot, a chatbot written in python implemented on two platforms, twitch and discord.

The bots features on each platform are very different. I will give an explanation of each of them.

## Discord
The discord bot is mostly focused on playing audio through discords voice client. It has 2 versions, the old one `discordold/` is ran through 2 classes, with an object oriented architecture. `bot.py` the main class for running the bot and `messages.py` the class used for handling commands through messages. The newer version under `discordnew/` is partly a refactor after i realized the object oriented nature of its architecture was unnecessarily constraining combined with a migration to discords new api `nextcord`.

The discord bot has the following features:
- Connection to discord using discords python library.
- Coroutines started for each command.
- Play audio through the discord client. This feature includes:
    - Download songs based on user input.
    - Queue up songs that automatically play after the previous one finishes.
    - Automatically disconnect from the voice client once the queue is empty.
    - Skip song on user input.
    - Leave voice channel on user input.


## Twitch
The twitch bot is non functioning at the moment, because I accidentally deleted some of the project files 
(mostly date formatting for logging, but still enough to brick the program unless i change it or add it back).
To run the bot you would have to set up the sql database and fix that.

The twitch bot consists mostly of global variables and functions looped in a while True loop for running the bot. This bot was one 
of my first programming projects so its mostly just used for learning programming through different commands.

The twitch bot has the following features:
- Manual connection to twitch using a socket
- Multiple API parsing commands using pythons requests library
- Full logging of all chat messages (in all the channels the bot is specified to be in) through a local sql database. 
    - Some of the commands also selects and returns data from this database on demand.
- Permissions for commands (this data is also stored in the database)
- Many other commands such as: sending a notification to someone the next time they sent a message, evaling files, 
getting a youtube url to a random song, check your followage to a twitch channel, and many more!
