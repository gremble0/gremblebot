"""Discord bot written by gremble"""
import datetime
import secrets
import discord
from playlist import Playlist
from commands import handle_command

def run_bot():
    """Main method for running bot"""
    commands = [
        "!ping",
		"!play"
	]

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    playlist = Playlist(client) # for !play command

    @client.event
    async def on_ready():
        print(f'{client.user} is running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        now = datetime.datetime.today().strftime("%Y/%m/%d %H:%M")
        print(f"{now} #{message.channel}, {message.author}: {message.content}")

        if message.content.split()[0] in commands:
            try:
                response = await handle_command(message, playlist)
                await message.channel.send(response)
            except Exception as err:
                print("ERROOREROOOROEOOERORORORRRRR\n", err)

    client.run(secrets.DISCORD_TOKEN)

if __name__ == "__main__":
    run_bot()
