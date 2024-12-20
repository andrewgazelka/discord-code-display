import os
import re
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# STRONG OPINION: Use environment variables for your token, never hardcode.
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')  # Make sure you set this before running.

# This regex aims to capture:
# Full URL, owner, repo, commit, file path, start line, and end line.
# Example tested: https://github.com/hyperion-mc/hyperion/blob/ef00b81042a6699573013941374099134817502d/crates/hyperion/src/simulation/handlers.rs#L257-L276
GITHUB_URL_REGEX = re.compile(
    r'(https://github\.com/([^/]+)/([^/]+)/blob/([0-9a-f]+)/(.+?)#L(\d+)(?:-L(\d+))?)'
)

# Strong opinion: a small map from file extension to language code for markdown.
EXTENSION_LANG_MAP = {
    '.rs': 'rust',
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.go': 'go',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.cs': 'csharp',
    '.html': 'html',
    '.css': 'css',
    '.sh': 'bash'
    # Add more as needed
}


def guess_language(filepath: str) -> str:
    # STRONG OPINION: just pick the extension, map it. If unknown, default to text.
    for ext, lang in EXTENSION_LANG_MAP.items():
        if filepath.endswith(ext):
            return lang
    return 'text'


intents = discord.Intents.default()
intents.message_content = True  # Important for reading messages with links
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.event
async def on_message(message: discord.Message):
    # Don’t respond to ourselves or if there's no content
    if message.author.bot or not message.content:
        return

    match = GITHUB_URL_REGEX.search(message.content)
    if match:
        url, owner, repo, commit, filepath, start_line, end_line = match.groups()
        start_line = int(start_line)
        end_line = int(end_line) if end_line else start_line

        # STRONG OPINION: Just fetch via raw.githubusercontent.com
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{filepath}"

        async with aiohttp.ClientSession() as session:
            async with session.get(raw_url) as resp:
                if resp.status != 200:
                    # If it fails, respond with an error
                    await message.channel.send("Failed to fetch the file from GitHub.")
                    return

                text = await resp.text()
                lines = text.split('\n')

                # Adjust indexing since lines are 1-based in GitHub links
                if start_line < 1 or end_line > len(lines):
                    await message.channel.send("Line numbers out of range.")
                    return

                snippet = lines[start_line - 1:end_line]
                language = guess_language(filepath)

                # Format the code block
                code_block = f"```{language}\n" + "\n".join(snippet) + "\n```"
                await message.channel.send(code_block)

    # Allow commands to still work
    await bot.process_commands(message)


if __name__ == '__main__':
    bot.run(TOKEN)
