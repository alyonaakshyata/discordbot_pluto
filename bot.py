import discord
import youtube_dl
import random
import os
from discord.ext import commands
from discord.utils import get
import asyncio

bot = commands.Bot(command_prefix = '.')

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command()
@commands.is_owner()
async def reload(ctx, cog):
    try:
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'{cog} got reloaded:')
    except Exception as e:
        print(f'{cog} cannot be loaded:')
        raise e 

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(aliases = ['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Don’t count on it.',
                 'It is certain.',
                 'It is decidedly so.',
                 'Most likely.',
                 'My reply is no.',
                 'My sources say no.',
                 'Looks not so good.',
                 'Looks good.',
                 'Reply hazy, try again.',
                 'Signs point to yes.',
                 'Very doubtful.',
                 'Without a doubt.',
                 'Yes.',
                 'Yes – definitely.',
                 'Not at all.',
                 'You may rely on it.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@bot.command(aliases=['ui','Userinfo','UserInfo','UI'])
async def userinfo(ctx, member : discord.Member = None):

    member = ctx.author if not member else member

    roles = [role for role in member.roles]

    '''roles = []
    for role in member.roles:
        roles.append(role)'''

    embed = discord.Embed(
        colour = member.colour,
        timestamp = ctx.message.created_at
    )

    embed.set_author(name = f'User Info - {member}')
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
    
    embed.add_field(name = 'ID:', value = member.id)
    embed.add_field(name = 'Name:', value = member.display_name)
    
    embed.add_field(name = 'Created at:', value = member.created_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
    embed.add_field(name = 'Joined at:', value = member.joined_at.strftime('%a, %d %B %Y, %I:%M %p UTC'))
    
    embed.add_field(name = f'Roles ({len(roles)})', value = ' '.join([role.mention for role in roles]))
    embed.add_field(name = 'Top role:', value = member.top_role.mention)

    embed.add_field(name = 'Bot?', value = member.bot)

    await ctx.send(embed = embed)

@bot.command()
async def avatar(ctx, member : discord.Member = None):
    
    member = ctx.author if not member else member

    embed = discord.Embed(
        title = 'Avatar',
        colour = member.colour
    )
    
    embed.set_author(name = f'{member}', icon_url = member.avatar_url)
    embed.set_image(url = member.avatar_url)
    
    await ctx.send(embed = embed)    


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title = 'List of all Commands',
        colour = discord.Colour.purple()
    )   
    
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/750060115578716212/752431094934142996/Drib8314_rectangle.jpg')
    embed.set_author(name = 'Pluto', icon_url = 'https://cdn.discordapp.com/attachments/750060115578716212/752431094934142996/Drib8314_rectangle.jpg')
    embed.add_field(name = '.ping', value = 'Returns Pong!', inline = False)
    embed.add_field(name = '.8ball', value = 'Lets you ask any question', inline = False)
    embed.add_field(name = '.clear', value = 'Clears the number of specified messages', inline = False)
    embed.add_field(name = '.userinfo', value = 'Shows information about the user or about the user mentioned', inline = False)

    await ctx.send(embed=embed)

async def chng_pr():
    await bot.wait_until_ready()

    statuses = ['.help', 'Being a good bot', 
                'Having fun', 'Playing with Softie',
                'Playing with Corvus', 'Playing with 19Stars', 
                'Playing with Jelly', 'Playing with Lexii', 
                'Playing with Gangu', 'Playing with ASM',
                'Playing with Triggered', 'Playing with Toxic',
                'Playing with Notty Bot']

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity = discord.Game(status))

        await asyncio.sleep(15)

bot.loop.create_task(chng_pr())

@bot.command(pass_content = True, aliases = ['j'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot is connected to {channel}\n")
    
    await ctx.send(f"Pluto has joined {channel}")

@bot.command(pass_content = True, aliases = ['l'])
async def leave(ctx):
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Pluto has left {channel}")
    else:
        print("Asked to leave channel where the bot was not in")
        await ctx.send(f"Pluto is not in that channel")
    

@bot.command(pass_content = True, aliases = ['p'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("Oh no! The song is being played")
        return

    await ctx.send("Getting things ready now")

    voice = get(bot.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format': 'beastaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Dowloading audio now\n")
        ydl.download([url])
        
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = fileprint(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
        
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("Playing\n")




'''
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 753867663373238344:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emo ji.name == 'a':
            print('role1')
        elif payload.emoji.name == 'b':
            role = discord.utils.get(guild.roles, name = 'role 2')
        else:
            role = discord.utils.get(guild.roles, name = payload.emoji.name)

        if role is not None:
            print(role.name)

@bot.event
async def on_raw_reaction_remove(payload):
    pass

for cog in os.listdir('.\\cogs'):
    if cog.endswith('.py'):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f'{cog} cannot be loaded:')
            raise e 
'''

bot.run('NzQ1NzA3ODAwNTcwNjI2MTQ5.Xz1sgg.FG_CZ9nY_vv_B2GsL-bvF7jm2_g')
