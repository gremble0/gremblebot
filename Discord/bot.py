import discord
import datetime
import secrets
from commands import handle_command

def run_bot():
	commands = [
		"!ping",
		"!play"
	]

	TOKEN = secrets.DISCORD_TOKEN
	intents = discord.Intents.default()
	intents.message_content = True
	client = discord.Client(intents=intents)

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
				response = await handle_command(client, message)
				await message.channel.send(response)
			except Exception as e:
				print("ERROOREROOOROEOOERORORORRRRR\n" + e)

	client.run(TOKEN)

if __name__ == "__main__":
	run_bot()
