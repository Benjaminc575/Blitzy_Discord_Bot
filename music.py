import discord
import os
import asyncio
import yt_dlp
from dotenv import load_dotenv
from typing import Final
from responses import get_response


def run_bot():
    # Load the bot token
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # Properties for Music Portion
    queues = {}
    voice_clients = {}
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -filter:a "volume=0.25"'
    }

    # Define the command prefix
    COMMAND_PREFIX: Final[str] = '!'

    # Alerts when bot is ready
    @client.event
    async def on_ready():
        print(f'{client.user} is now jamming')

    # Sends a message in private
    async def send_message(message, user_message: str) -> None:
        if not user_message:
            print('(Message was empty because intents were not enabled probably)')
            return

        is_private = user_message.startswith('?')
        if is_private:
            user_message = user_message[1:]

        try:
            response: str = get_response(user_message)
            if is_private:
                await message.author.send(response)
            else:
                await message.channel.send(response)
        except Exception as e:
            print(e)

    # Methods for bot to respond with
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        user_message: str = message.content

        if user_message.startswith("!play"):
            await handle_play(message)

        elif user_message.startswith("!pause"):
            await handle_pause(message)

        elif user_message.startswith("!resume"):
            await handle_resume(message)

        elif user_message.startswith("!stop"):
            await handle_stop(message)

        else:
            # Only process non-command messages
            if user_message.startswith(COMMAND_PREFIX):
                user_message = user_message[len(COMMAND_PREFIX):]
                username: str = str(message.author)
                channel: str = str(message.channel)

                print(f'[{channel}] {username}: "{user_message}"')
                await send_message(message, user_message)

    async def handle_play(message):
        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        try:
            url = message.content.split()[1]
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            voice_clients[message.guild.id].play(player)
        except Exception as e:
            print(e)

    async def handle_pause(message):
        try:
            voice_clients[message.guild.id].pause()
        except Exception as e:
            print(e)

    async def handle_resume(message):
        try:
            voice_clients[message.guild.id].resume()
        except Exception as e:
            print(e)

    async def handle_stop(message):
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
        except Exception as e:
            print(e)

    client.run(TOKEN)
