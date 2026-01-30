![Disallowed Content](https://cdn.discordapp.com/attachments/1451076730792968364/1466599937725825239/NH6Jf6T.png?ex=697d5521&is=697c03a1&hm=f618be3e619586ce48a1a4d5003cf994e19b39a4b3861280423637f5c21169e6&animated=true)

A Discord bot that automatically monitors and filters messages containing disallowed words. The bot deletes messages with prohibited content and warns users, helping maintain a clean and appropriate chat environment.

## Features

- **Automatic Message Monitoring**: Continuously checks all messages for disallowed words
- **Auto-Deletion**: Automatically deletes messages containing prohibited words
- **User Warnings**: Sends warnings in the channel when messages are deleted
- **Word List Management**: Easy-to-use slash commands to manage the disallowed words list
- **Smart Matching**: Uses word boundary detection to avoid false positives (e.g., "bad" won't match "badminton")
- **Persistent Storage**: Word list is saved to a JSON file and persists across bot restarts
- **Case-Insensitive**: Detects words regardless of capitalization

## Prerequisites

- Python 3.8 or higher
- A Discord bot token ([How to create a Discord bot](https://discord.com/developers/applications))
- Discord server with appropriate bot permissions

## Installation

1. **Clone or download this repository**

2. **Install required dependencies:**
   ```bash
   pip install discord.py python-dotenv boto3
   ```


3. **Set up environment variables:**
   
   Create a `.env` file in the project root directory:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   S3_BUCKET=your_S3_bucket
   ```
   
   Replace `your_bot_token_here` with your actual Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
   Replace `your_S3_bucket` with your S3 bucket from [AWS](https://aws.amazon.com/s3/).

## Configuration

1. **Get your Discord Bot Token:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application or select an existing one
   - Navigate to the "Bot" section
   - Click "Reset Token" or copy your existing token
   - Paste it into your `.env` file

2. **Invite the bot to your server:**
   - In the Developer Portal, go to the "OAuth2" → "URL Generator" section
   - Select the `bot` scope
   - Select the following bot permissions:
     - `Send Messages`
     - `Manage Messages` (required to delete messages)
     - `Use Slash Commands`
   - Copy the generated URL and open it in your browser to invite the bot

3. **Configure the Guild ID (optional):**
   
   In `src/disallowed.py`, you can set a specific `GUILD_ID` for faster command syncing during development:
   ```python
   GUILD_ID = 1451076729929207810  # Replace with your server ID
   ```

## Usage

1. **Run the bot:**
   ```bash
   python src/disallowed.py
   ```

2. **Wait for the bot to come online:**
   - You should see a message indicating the bot has loaded and synced commands
   - The bot will print how many words were loaded from the file

3. **Start managing your word list:**
   - Use the slash commands (see Commands section below) to add words to the disallowed list
   - The bot will automatically start monitoring and filtering messages

## Commands

All commands are slash commands (use `/` in Discord to access them):

### `/addword <words>`
Add one or more words to the disallowed words list.

- **Parameters:**
  - `words`: Words separated by spaces or commas
- **Example:**
  - `/addword bad word`
  - `/addword spam, inappropriate, offensive`
- **Response:** Shows which words were added and which already existed

### `/removeword <words>`
Remove one or more words from the disallowed words list.

- **Parameters:**
  - `words`: Words separated by spaces or commas
- **Example:**
  - `/removeword bad`
  - `/removeword spam, inappropriate`
- **Response:** Shows which words were removed and which weren't found

### `/listwords`
Display all words currently in the disallowed words list.

- **Response:** Lists all disallowed words (ephemeral, only visible to you)

### `/clearwords`
Remove ALL words from the disallowed words list.

- **Response:** Confirms how many words were removed
- **Warning:** This action cannot be undone!

## How It Works

1. **Message Monitoring:**
   - The bot listens to all messages sent in channels where it has access
   - It ignores messages from bots to prevent infinite loops

2. **Word Detection:**
   - Messages are checked against the disallowed words list
   - Uses regex with word boundaries (`\b`) to match whole words only
   - Case-insensitive matching (e.g., "Bad", "BAD", "bad" all match)
   - Example: If "bad" is in the list, it will match "bad!", "bad.", "bad word" but NOT "badminton"

3. **Action Taken:**
   - When a disallowed word is detected:
     1. The message is immediately deleted
     2. A warning is sent in the channel mentioning the user
     - The warning lists which words triggered the deletion

## File Structure

```
Disallowed-Content/
├── src/
│   ├── disallowed.py      # Main bot code
│   ├── S3_helpers.py      # Helper functions for easier readability in S3.py
│   ├── S3.py              # Holds the S3 function called by disallowed.py
│   └── word_list.json     # Stores the disallowed words (auto-generated)
├── .env                   # Your bot token (create this file)
├── README.md              # This file
└── .gitignore            # Git ignore file
```

## Permissions Required

The bot needs the following permissions in your Discord server:

- ✅ **Send Messages** - To send warning messages
- ✅ **Manage Messages** - To delete messages containing disallowed words
- ✅ **Use Slash Commands** - To use the command system
- ✅ **Read Message History** - To monitor messages (usually granted by default)

## Troubleshooting

### Bot doesn't respond to commands
- Make sure the bot is online and running
- Check that you've invited the bot with the correct permissions
- Wait a few minutes after starting the bot for commands to sync

### Bot can't delete messages
- Ensure the bot has "Manage Messages" permission in the channel
- Check that the bot's role is positioned above the role of users whose messages it needs to delete

### Bot doesn't detect words
- Make sure words are added to the list using `/addword`
- Check that the word matches exactly (case-insensitive, but must be a whole word)
- Verify the bot has "Read Messages" permission in the channel

### Commands not showing up
- Commands sync on bot startup and may take a few minutes
- Try restarting the bot
- For faster syncing during development, set `GUILD_ID` in the code

## Notes

- The word list is stored in `src/word_list.json` and persists across bot restarts
- All commands are ephemeral (only visible to the user who ran them) for privacy
- The bot ignores empty messages and bot messages
- Word matching is case-insensitive and uses word boundaries to prevent false positives

## License

This project is open source and available for modification and distribution.

## Support

For issues or questions, please check the code comments or create an issue in the repository.

