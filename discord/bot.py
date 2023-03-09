"""Discord bot written by gremble"""
import datetime
import secrets
import discord
from playlist import Playlist
from commands import handle_command

class Bot:
    """Main class for running bot"""
    def __init__(self):
        commands = [
            "!ping",
            "!play",
            "!stop"
        ]
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.client = discord.Client(intents=self.intents)
        self.playlist = Playlist(self.client) # for !play command


        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            now = datetime.datetime.today().strftime("%Y/%m/%d %H:%M")
            print(f"{now} #{message.channel}, {message.author}: {message.content}")

            if message.content.split()[0] in commands:
                response = await handle_command(message, self.playlist)
                await message.channel.send(response)

    def run(self) -> None:
        """Runs bot"""
        self.client.run(secrets.DISCORD_TOKEN)

    # todo - migrate commands to bot class,
    #      - add dict for calling commands,
    #      - fix queueing songs in !play
    #      - add command for stopping bot remotely,
    #           - easier with commands in bot class
    #      - remove songs after played

if __name__ == "__main__":
    bot = Bot()
    bot.run()
