import discord
import commands

async def send_message(message):
    try:
        response = commands.handle_command(message.content)
        await message.channel.send(response)

    except Exception as e:
        print(e)
        

def run_discord_bot():
	commands = [
		"!ping",
		"!roll",
		"!help"
	]

	TOKEN = ""
	intents = discord.Intents.default()
	intents.message_content = True
	client = discord.Client(intents=intents)

	@client.event
	async def on_ready():
		print(f'{client.user} is now running!')

	@client.event
	async def on_message(message):
		if message.author == client.user:
			return

		#voice_client = discord.VoiceClient(client, message.channel)
		sender = str(message.author)
		content = message.content
		channel = str(message.channel)

		print(f"#{channel}, {sender}: {content}")
		
		if content.split()[0] in commands:
			await send_message(message)

	client.run(TOKEN)
