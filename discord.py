import discord
from discord.ext import commands
import yt_dlp
import asyncio

intents=discord.Intents.default()
intents.message_content=True
intents.voice_states=True
FFMPEG_OPTIONS={'options':'-vn'}
YDL_OPTIONS={'format':'bestaudio','noplay':True}

class MusicBot(commands.Cog):
    def __init__(self,client):
        self.client=client
        self.queue=[]

    @commands.command()
    async def    play(self,ctx,*,search):
        voice_channel=ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("Join vc mf")
        if not ctx.voice_client:
            await voice_channel.connect()


        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info=ydl.extract_info(url=f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info=info['entries'][0]
                url=info['url']
                title=info['title']
                self.queue.append((url,title))
                await ctx.send(f'Added to queue:**(title)**')
        if not ctx.voice_client.is_playing():
            await.self.play_next()
        
async def play_next(self,ctx):
        if self.queue:
            url,title=self.queue.pop(0)
            source=await discord.FFmpegOpusAudio.from_probe(url,**FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lamda _:self.client.loop.create_tast(self.play_next(ctx)))
            await ctx.send(f'Now playing **{title}**')
        elif not ctx.voice_client.is_playing():
            wait ctx.send("Queue is empty")

        @commands.command()
        async def skip(self, ctx):
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Skipped")
                
                
                
client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    await client.add_cog(MusicBot(client))
    await client.start('MTA1NjY2OTExODg2ODI0MjYwMg.Go2Kj7.7fbCxF1rQieWd-KIDOsyuiYywTQ9J0beVn3VMk')
 
asyncio.run(main())
