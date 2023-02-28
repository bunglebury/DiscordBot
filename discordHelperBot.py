import discord
from datetime import datetime
import requests
import youtube_dl
import asyncio



dt = datetime.now()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is reporting')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.lower().startswith('$day'):
        await message.channel.send(dt)
    
    if message.content.lower().startswith('$dog'):
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        img = r.json()["message"]
        await message.channel.send(img)
    
    if message.content.lower().startswith('$help'):
        await message.channel.send('These are commands to help you ---> $day, $dog, $hello')
    
    if message.content.startswith('$'):
        cmd = message.content.split(" ")[0]
        cmds = ['$dog','$help','$hello', '$joinvc']
        if cmd not in cmds:
            await message.channel.send('Sorry I do not that command, try ($help) for a list of commands')

    if message.content.startswith('$joinvc'):
        if message.author.voice:
            youtube_link = message.content.split(" ")[1]
            if youtube_link:
                ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(youtube_link, download=False)
                        title = info.get('title', None)
                        if title:
                            vc = await message.author.voice.channel.connect()
                            vc.play(discord.FFmpegPCMAudio(f"{title}.mp3"), after=lambda e: print('done', e))
                        await asyncio.sleep(info['duration'])
                except Exception as e:
                    print(e)
        if client.voice_clients:
            for vc in client.voice_clients:
                await vc.disconnect()
        

    
        

if __name__ == '__main__':
    client.run('')

