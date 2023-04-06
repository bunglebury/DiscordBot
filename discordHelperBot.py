import discord
import requests
import asyncio
import datetime
import youtube_dl


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


async def display_time(message):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await message.channel.send(f"Current time: {current_time}")


async def display_dog(message):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    img_url = response.json()["message"]
    await message.channel.send(img_url)


async def join_voice_channel(message):
    if not message.author.voice:
        await message.channel.send("You are not connected to a voice channel.")
        return
    youtube_link = message.content.split(" ")[1]
    if not youtube_link:
        await message.channel.send("Please provide a valid YouTube link.")
        return
    try:
        with youtube_dl.YoutubeDL() as ydl:
            info = ydl.extract_info(youtube_link, download=False)
            video_url = info['formats'][0]['url']
        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(video_url), after=lambda e: print('done', e))
        await asyncio.sleep(info['duration'])
    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")
    finally:
        await voice_client.disconnect()


async def display_help(message):
    help_text = "These are the available commands:\n"
    help_text += "- `$hello`: Say hello to the bot.\n"
    help_text += "- `$day`: Display the current date and time.\n"
    help_text += "- `$dog`: Display a random picture of a dog.\n"
    help_text += "- `$joinvc <YouTube link>`: Join your voice channel and play the audio from the specified YouTube video.\n"
    await message.channel.send(help_text)


async def handle_command(message):
    command = message.content.lower().split(" ")[0]
    if command == "$hello":
        await message.channel.send("Hello!")
    elif command == "$day":
        await display_time(message)
    elif command == "$dog":
        await display_dog(message)
    elif command == "$joinvc":
        await join_voice_channel(message)
    elif command == "$help":
        await display_help(message)
    else:
        await message.channel.send(f"Unknown command: {command}")


@client.event
async def on_ready():
    print(f'{client.user} is reporting')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$"):
        await handle_command(message)


if __name__ == '__main__':
    client.run('')
