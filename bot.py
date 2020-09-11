import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases = ['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Of course.',
                 'Absolutely.',
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

@client.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(aliases=['ui','Userinfo','UserInfo','UI'])
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
    
@client.command()
async def avatar(ctx, member : discord.Member = None):
    
    member = ctx.author if not member else member

    embed = discord.Embed(
        title = 'Avatar',
        colour = member.colour
    )
    
    embed.set_author(name = f'{member}', icon_url = member.avatar_url)
    embed.set_image(url = member.avatar_url)
    
    await ctx.send(embed = embed)        
    

@client.command()
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

client.run('NzQ1NzA3ODAwNTcwNjI2MTQ5.Xz1sgg.7drNBQmVg1eyrKD2F_WESEv3Q3k')
