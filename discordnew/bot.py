from nextcord import Interaction, Intents, Client, VoiceClient, Message
from nextcord.ext import commands
from dotenv import load_dotenv
from os import getenv

class Bot:
    def __init__(self) -> None:
        intents = Intents.default()
        intents.message_content = True

        self.client: Client = commands.Bot()
        self.voice_Client: VoiceClient | None = None

        @self.client.event
        async def on_message(message: Message):
            if message.author == self.client.user: return

            print(f"#{message.channel}, {message.author}: {message.content}")
            await self.handle_message(message)

        @self.client.slash_command(guild_ids=[978053854878904340], description="test command")
        async def test(interaction: Interaction):
            await interaction.response.send_message("test")

    def run(self) -> None:
        load_dotenv(dotenv_path=".env")
        DISCORD_TOKEN: str | None = getenv("DISCORD_TOKEN")

        if not DISCORD_TOKEN:
            print("Couldn't find discord token")
        else:
            self.client.run(DISCORD_TOKEN)

    async def handle_message(self, message: Message):
        pass
            
if __name__ == "__main__":
    bot = Bot()
    bot.run()
