import os
import discord
import requests
from discord.ext import commands, tasks

import praw
redditclient = praw.Reddit(client_id=os.environ['reddit_id'], client_secret=os.environ['reddit_secret'], user_agent=os.environ['reddit_agent'])


# client = discord.Client()
client = commands.Bot(command_prefix = commands.when_mentioned_or("!"))
todos = [];

@client.event
async def on_ready():
	guild = discord.utils.get(client.guilds, name='My Test Server')
	print(f'We have logged in as {client.user}')
	print(f'{client.user} is connected to {guild.name}(id: {guild.id})')
	for member in guild.members:
		print(member)


# @client.event
# async def on_message(message):
# 	if message.author == client.user:
# 		return

# 	if message.content.startswith('$add'):
# 		todos.append(message.content[4:])
# 		await message.channel.send(f'> **{message.content[4:]}** has been added successfully.')
	
# 	if message.content == '$view':
# 		todolist = '';
# 		for i in range(len(todos)):
# 			todolist += f'{i}. {todos[i]}\n'
# 		await message.channel.send(f'> {todolist}')
	
# 	if message.content.startswith('$remove'):
# 		todos.remove(message.content[7:])
# 		await message.channel.send(f'> **{message.content[7:]}** has been removed successfully.')

# 	await client.process_commands(message)


@client.command()
async def random(ctx):
	url = ('https://api.quotable.io/random')
	response = requests.get(url)
	quote = response.json()
	quoteContent = quote['content']
	quoteAuthor = quote['author']
	await ctx.send(f'> {quoteContent} \n— {quoteAuthor}')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}.ms')


@client.event
async def on_member_join(member):
	await member.create_dm()
	await member.dm_channel.send(
			f'Hi {member.name}, welcome to my server'
		)

@client.command()
async def reddit(ctx, arg):
	hot_posts = redditclient.subreddit(arg[2:]).hot(limit=10)
	embed = discord.Embed(title=f'Top posts in {arg}', description=f"Shows the hottest posts in the [{arg}](https://reddit.com/{arg}) subreddit", color=0x00ff00)
	embed.set_thumbnail(url='https://cdn2.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Reddit-512.png')
	for post in hot_posts:
			print(post.title)
			embed.add_field(name=f'**{post.title}**', value=f':link:	{post.url} \n 	:arrow_up:	{post.score}	:speech_left:	{post.num_comments}', inline=False)
	await ctx.send(embed=embed)

@reddit.error
async def reddit_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please enter the name of the subreddit after the **!reddit** command')

@client.command()
async def redditposts(ctx):
	subreddit_list = ['r/coding', 'r/javascript', 'r/learnprogramming', 'r/programming', 'r/Python', 'r/webdev', 'r/web']
	embed = discord.Embed(title='List of available subreddits', description="Shows a list of subreddits where posts can be gotten from", color=0x6b57f7)
	embed.set_thumbnail(url='https://cdn2.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Reddit-512.png')
	for sub in subreddit_list:
		embed.add_field(name=f'**{sub}**', value=f'!reddit {sub} - Returns posts in the [{sub}](https:reddit.com/{sub}) subreddit', inline=False)
	await ctx.send(embed=embed)

client.run(os.environ['DISCORD_TOKEN'])