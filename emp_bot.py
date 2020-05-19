
import os
import random
import sys
import praw
import discord
import datetime
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, BadArgument, Context
from discord import Guild, Member, Embed
from discord.utils import get
from textwrap import wrap


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
# redditSecret = os.getenv('REDDIT_CLIENT_SECRET')
# redditID = os.getenv('REDDIT_CLIENT_ID')
# redditAgent = os.getenv('REDDIT_USER_AGENT')
# redditPW = os.getenv('REDDIT_PW')
# redditUName = os.getenv('REDDIT_USERNAME')
# reddit = praw.Reddit(client_id=redditID,
#                    client_secret=redditSecret,
#                    user_agent=redditAgent,
#                    username=redditUName,
#                    password=redditPW)

# Discord client
client = commands.Bot(command_prefix='!')  # !COMMAND_NAME args


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command(pass_context=True, name="kick")
@has_permissions(kick_members=True)
async def kick(ctx: Context, user: Member, *, reason: str = None):
    """
        <prefix> kick <user name>
        Mentioning is a faster way to get the user.
         Is able to kick a user from guild.
        """
    await Guild.kick(ctx.guild, user)
    await ctx.channel.send("I have kicked {}".format(user.name))


@client.command(pass_context=True, name="ban")
@has_permissions(ban_members=True)
async def ban(ctx: Context, member: Member, reason=None):
    """Bans a user"""
    if reason == None:
        await ctx.send(f"Woah {ctx.author.mention}, Make sure you provide a reason!")
    else:
        messageok = f"You have been banned from {ctx.guild.name} for {reason}"
        await member.send(messageok)
        await member.ban(reason=reason)


@client.command(pass_context=True)
async def create_mute_role(guild: Guild):
    '''
    `guild` : must be :class:`discord.Guild`
    '''
    role_name = "muted"
    # allows us to check if the role exists or not
    mute_role = get(guild.roles, name=role_name)

    # if the role doesn't exist, we create it
    if mute_role is None:
        await guild.create_role(name=role_name)
        # retrieves the created role
        mute_role = get(guild.roles, name=role_name)

    # set channels permissions
    for channel in guild.text_channels:
        await asyncio.sleep(0)

        mute_permissions = discord.PermissionOverwrite()
        mute_permissions.send_messages = False

        await channel.set_permissions(mute_role, overwrite=mute_permissions)

    return(mute_role)


@client.command(pass_context=True)
async def mute(ctx, member: discord.Member):
    guild = ctx.message.guild
    mute_role = await create_mute_role(guild)
    await member.add_roles(mute_role)

    await ctx.send(f"{member.name} has been muted !")
    return


@client.command(pass_context=True)
async def ping(ctx):
    ping_in_millis = round((client.latency * 1000), 4)
    await ctx.channel.send(f'My ping is {str(ping_in_millis) } ms!')


@client.command(pass_context=True)
async def server_info(ctx):
    await ctx.channel.send(f'Server name: {ctx.guild.name}\nServer emojis: {ctx.guild.emojis})\nServer owner: {ctx.guild.owner}\nServer roles: {ctx.guild.roles}')


async def help(ctx):
    await ctx.channel.send("You can use commands !user-info, !ping, !ban, !kick, and !server-info")


@client.command(pass_context=True)
async def user_info(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    await ctx.channel.send(f"This user joined this server at: {user.joined_at.strftime('%A, %B %d %Y')}) \nThis user created their account at: {user.created_at.strftime('%A, %B %d %Y')})\nThis user has been premium since: {str(user.premium_since)})")

client.run(token)
