import discord
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Ready to detect some naughty words!')

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    print(f"Received message: {message.content} from {message.author}")
    

    content = message.content.strip()    
    if content.lower().startswith('!config'):
        try:
            await message.channel.send('Lists config commands')
            print(f"Sent response to {message.author}")
        except discord.errors.Forbidden:
            print(f"Error: Bot doesn't have permission to send messages in {message.channel}")
        except Exception as e:
            print(f"Error sending message: {e}")

client.run(DISCORD_TOKEN)