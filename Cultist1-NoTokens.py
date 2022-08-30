import discord
import asyncio
import praw
import random
import youtube_dl
from discord.ext import commands
TOKEN = 'TOKEN'

client = commands.Bot(command_prefix = 'g')

reddit = praw.Reddit(client_id='ID',
                     client_secret='SECRET',
                     user_agent='discord:discordBotGondolaCultist:v1.0 (by /u/nagrago)')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

@client.command()
async def ping(ctx):
    await ctx.send(f'pong {round(client.latency*1000)}ms')

@client.command()
async def set(ctx, member: discord.Member, *, newName="null"):
                await ctx.send(member.display_name + "has become" + newName + "!")
                await member.edit(nick=newName)
                
@client.command(aliases=['M'])
async def meter(ctx, member: discord.Member):
                        responses = ['100%', '50%', '10%', '25%', 'Literally 0%', 'no']
                        await ctx.send(member.display_name + " has been declared: " + random.choice(responses))

@client.command(aliases=['S'])
async def chance(ctx, member: discord.Member):
    num = round(random.uniform(0, 10), 1)
    await ctx.send(f'{member.display_name} is: {num}')

@client.command(aliases=['pog', 'pogchamp'])
async def poggers(ctx, *, num=1):
    count = 0
    responses = ['Pog', 'Pogchamp', 'Poggers', 'Pepehands', 'Yeet', 'Pepega', 'LEROY JENKINS', 'YE', 'ye', 'Damn']
    while count<num:
        await ctx.send(random.choice(responses))
        count+=1

@client.command()
async def echo(ctx, *, echoS="echo"):
    await ctx.send(echoS)

@client.command()
async def g(ctx):
    response = ['lol I was lagging', 'you should legit just uninstall', 'no']
    await ctx.send(random.choice(response))

@client.command()
async def o(ctx):
    response = 'no'
    await ctx.send(response)

#random images
@client.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)

@client.command()
async def memeN(ctx):
    memes_submissions = reddit.subreddit('memes').new()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)

@client.command()
async def memeT(ctx):
    memes_submissions = reddit.subreddit('memes').top()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await ctx.send(submission.url)

@client.command()
async def dankmeme(ctx):
    memes_submissions = reddit.subreddit('dankmemes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)

@client.command()
async def dankmemeN(ctx):
    memes_submissions = reddit.subreddit('dankmemes').new()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)

@client.command()
async def dankmemeT(ctx):
    memes_submissions = reddit.subreddit('dankmemes').top()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    await ctx.send(submission.url)


#voice
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def p(ctx, *, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
        print(url)
        channel = ctx.author.voice.channel
        vc = await channel.connect()

        async with ctx.typing():
            player = await YTDLSource.from_url(url)
            vc.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))

#YT COPIES
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(executable = "C:/ProgramData/chocolatey/bin/ffmpeg.exe",source = filename, **ffmpeg_options), data=data)
    

client.run(TOKEN)
