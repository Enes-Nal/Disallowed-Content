import discord
import os
from dotenv import load_dotenv
from discord import app_commands
import json

DATA_FILE = "word_list.json"
# Load word list from file
def load_words():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Save word list to file
def save_words(words):
    with open(DATA_FILE, 'w') as f:
        json.dump(words, f, indent=2)

# Global word list
word_list = load_words()


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# intents for the bot
intents = discord.Intents.default()
intents.message_content = True

GUILD_ID = 1451076729929207810  #server ID

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Sync commands to a specific guild for faster updates for testing purposes
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"Commands synced to guild {GUILD_ID}")

    async def on_ready(self):
        print(f"Loaded {len(word_list)} words from file")

client = MyClient(intents=intents)
tree = client.tree

@tree.command(name="addword", description="Add one or more words to the list")
@app_commands.describe(words="Enter words separated by spaces or commas")
async def addword(interaction: discord.Interaction, words: str):
    # turns input into raw input by removing uncesary stuff and splitting it into json
    raw_words = words.replace(",", " ").split()
    added = []
    skipped = []

    for word in raw_words:
        #checks for each word in the list, strips of whitespace, lowers
        word = word.strip().lower()
        if not word:
            continue

        if word in word_list:
            skipped.append(word)
        else:
            word_list.append(word)
            added.append(word)

    if added:
        save_words(word_list)

    response = []
    if added:
        response.append(f"✅ Added: {', '.join(added)}")
    if skipped:
        response.append(f"⚠️ Already existed: {', '.join(skipped)}")

    if not response:
        response.append("No valid words were provided.")

    await interaction.response.send_message(
        "\n".join(response), #adds added and skipped list messages as the response on diff lines
        ephemeral=True #makes the message visible only to the user who ran the command
    )

@tree.command(name="clearwords", description="Delete ALL words from the list")
async def clearwords(interaction: discord.Interaction):
    if not word_list:
        await interaction.response.send_message(
            "The word list is already empty.",
            ephemeral=True 
        )
        return

    count = len(word_list)  # Get count before clearing
    word_list.clear()   # removes everything from the list
    save_words(word_list) #saves the new empty list
    await interaction.response.send_message(
        f"Cleared all words ({count} words removed)",
        ephemeral=True
    )
@tree.command(name="removeword", description="Remove one or more words from the list")
@app_commands.describe(words="Enter words separated by spaces or commas")
async def removeword(interaction: discord.Interaction, words: str):
    raw_words = words.replace(",", " ").split()
    removed = []
    not_found = []

    for word in raw_words:
        word = word.strip().lower()
        if not word:
            continue

        if word in word_list:
            word_list.remove(word)
            removed.append(word)
        else:
            not_found.append(word)

    if removed:
        save_words(word_list)

    response = []
    if removed:
        response.append(f"🗑️ Removed: {', '.join(removed)}")
    if not_found:
        response.append(f"❌ Not found: {', '.join(not_found)}")

    if not response:
        response.append("No valid words were provided.")

    await interaction.response.send_message(
        "\n".join(response),
        ephemeral=True
    )

@tree.command(name="listwords", description="List ALL words from the list")
async def listwords(interaction: discord.Interaction):
    if not word_list:
        await interaction.response.send_message(
            "The word list is already empty.",
            ephemeral=True 
        )
        return
    words_text = ", ".join(word_list)
    for word in word_list:
        await interaction.response.send_message(
        f"{words_text}",
        ephemeral=True
    )

client.run(DISCORD_TOKEN)