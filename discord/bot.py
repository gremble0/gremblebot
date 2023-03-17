"""Discord bot written by gremble"""
import datetime
import secrets
import discord
from commands import CommandHandler


class Bot:
    """
    Main class for running bot

    Attributes
    ----------
    commands : str[]
        list of supported commands
    client : discord.Client()
        client for connecting to discord server
    voice_client : None
        client for connecting to discord voice servers
        starts uninstantiated, but becomes type : discord.VoiceClient
        once connected to a voice channel
    """

    def __init__(self):
        self.commands = [
            "%ping",
            "%play",
            "%stop",
            "%join",
            "%connect",
            "%leave",
            "%boobs",
        ]
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.voice_client = None
        self.command_handler = CommandHandler(self)

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            now = datetime.datetime.today().strftime("%Y/%m/%d %H:%M")
            print(f"{now} #{message.channel}, {message.author}: {message.content}")

            self.command_handler.message = message
            message_split = message.content.split()
            if message_split[0] in self.commands:
                await self.command_handler.handle_command()

    def run(self) -> None:
        """Runs bot"""
        self.client.run(secrets.DISCORD_TOKEN)

    # todo:
    #      - remove songs after they have been played
    #           - maybe stream instead of download? dont think possible
    #      - add permissions to !stop
    #      - rename downloaded files to url of video
    #      - if multiple commands need to download: shorten _play method,
    #        merge _connect and _play_queue into _play and make _download


if __name__ == "__main__":
    bot = Bot()
    bot.run()
