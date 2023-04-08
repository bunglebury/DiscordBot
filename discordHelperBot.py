import discord          # Import the discord library
import requests         # Import the requests library to make HTTP requests
import asyncio          # Import the asyncio library for asynchronous programming
import datetime         # Import the datetime library to work with dates and times
import youtube_dl       # Import the youtube_dl library to download and extract YouTube videos
import openai

# Set up the client object with the necessary intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = 'OPENAI API KEY HERE'
async def generate_message(message):
    prompt = message.content
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    output_text = response.choices[0].text.strip()
    await message.channel.send(output_text)

# Define a coroutine to display the current time in the chat
async def display_time(message):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await message.channel.send(f"Current time: {current_time}")

# Define a coroutine to display a random picture of a dog in the chat
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
    voice_client = None  # Define voice_client with a default value of None
    try:
        with youtube_dl.YoutubeDL({'verbose': True}) as ydl:
            info = ydl.extract_info(youtube_link, download=False)
            video_url = info['formats'][0]['url']
        voice_channel = message.author.voice.channel
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(video_url), after=lambda e: print('done', e))
        await asyncio.sleep(info['duration'])
    except Exception as e:
        await message.channel.send(f"An error occurred: {e}")
    finally:
        if voice_client:  # Check if voice_client has been assigned a value
            await voice_client.disconnect()

# Define a coroutine to display a help message with a list of available commands
async def display_help(message):
    help_text = "These are the available commands:\n"
    help_text += "- `$hello`: Say hello to the bot.\n"
    help_text += "- `$day`: Display the current date and time.\n"
    help_text += "- `$dog`: Display a random picture of a dog.\n"
    help_text += "- `$joinvc <YouTube link>`: Join your voice channel and play the audio from the specified YouTube video.\n"
    await message.channel.send(help_text)

# Define a coroutine to handle incoming messages and execute the appropriate command
async def handle_command(message):
    command = message.content.lower().split(" ")[0]
    if command == "$hello":
        response = await generate_message(message)
        await message.channel.send(response)
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

# Event handler that runs when the bot is ready to start receiving events
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
    client.run('DISCORD BOT KEY HERE')
