import discord 
from discord.ext import commands
import os
import requests
import json
from keep_alive import keep_alive
import random


client = commands.Bot(command_prefix = ',', help_command=None)

#Functions 
      
def get_joke(category):
  response = requests.get("https://v2.jokeapi.dev/joke/" + category + "?lang=en&blacklistFlags=nsfw,religious,racist")
  json_data = json.loads(response.text)
  if json_data['type'] == 'single':
    joke = json_data['joke']
    return(joke)
  else:
    joke = json_data['setup'] + "\n" + json_data['delivery']
    return(joke)

def get_riddle():
  response = requests.get("https://www.no-api-key.com/api/v1/riddle")
  json_data = json.loads(response.text)
  riddle = "Q: " + json_data['question'] + "\nA: " + json_data['answer']
  return(riddle)

#Commands

@client.group(name='joke', invoke_without_command=True)
async def joke(ctx):
  category= "Any"
  jokemessage = get_joke(category)
  await ctx.send(jokemessage)

@joke.command(name='programming')
async def programming_subcommand(ctx):
  category = "Programming"
  jokemessage = get_joke(category)
  await ctx.send(jokemessage)

@joke.command(name='misc')
async def misc_subcommand(ctx):
  category = "Misc"
  jokemessage = get_joke(category)
  await ctx.send(jokemessage)

@joke.command(name='pun')
async def pun_subcommand(ctx):
  category = "Pun"
  jokemessage = get_joke(category)
  await ctx.send(jokemessage)

@joke.command(name='spooky')
async def spooky_subcommand(ctx):
  category = "Spooky"
  jokemessage = get_joke(category)
  await ctx.send(jokemessage)

@joke.command(name='christmas')
async def christmas_subcommand(ctx):
  category = "Christmas"
  jokemessage = get_joke(category)
  await ctx.send(jokemessage)

@joke.command(name='dark')
async def dark_subcommand(ctx):
  category = "Dark"
  jokemessage = get_joke(category)
  await ctx.send(jokemessage)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.command()
async def riddle(ctx):
  riddlemessage = get_riddle()
  await ctx.send(riddlemessage)

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = 'Help', 
    description = 'A list of commands', 
    color = discord.Color.gold(),
  )
  embed.set_footer(text='Categories = programming, misc, pun, spooky, christmas, dark')
  embed.set_author(name='Joke Bot',icon_url='https://cdn.discordapp.com/attachments/884855108553281546/885500525804666930/185034.png')
  embed.add_field(name='Joke Commands', value=',joke - Just a joke!\n,joke (category) - A joke from that category', inline=False)
  embed.add_field(name='Game Commands', value=',numberguess - Play the number guessing game\n,highlow - Play the high low game', inline=False)
  embed.add_field(name='Misc Commands', value=',ping - Pong', inline=False)
  await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def numberguess(ctx):
  await ctx.send("A random number has been generated!\nType a number between 1 and 10 to guess the number!")
  num = random.randint(1,10)
  def check(reponse):
    return reponse.channel == ctx.channel and reponse.author == ctx.author and (int(reponse.content) >=1 or int(reponse.content) <=10)
  reponse = await client.wait_for("message", check=check)
  if int(reponse.content) == num:
    await ctx.send("You have guessed the number correctly!")
  else:
    await ctx.send("You have guessed the number incorrectly!\nThe number was " + str(num) + "!")

@client.command()
async def highlow(ctx):
  num1 = random.randint(1,100)
  await ctx.send("A random number has been generated, is this number higher or lower than " + str(num1) + "?\nThe number is between 1 and 100!\nType h, l or same!")
  num2 = random.randint(1,100)
  def check(reponse):
    return reponse.channel == ctx.channel and reponse.author == ctx.author
  response = await client.wait_for("message", check=check)

  if num2 > num1:
    condition = "Higher"
  elif num2 < num1:
    condition = "Lower"
  elif num1 == num2:
    condition = "Same"

  if response.content != "h" and response.content != "l" and response.content != "same":
    await ctx.send("Invalid reponse! Please respond with l, h or same!")
  elif condition == "Higher" and response.content == "h":
    await ctx.send("You have won!\nThe hidden number was " + str(num2)+ "!")
  elif condition == "Higher" and response.content == "l":
    await ctx.send("You have lost, it was higher!\nThe hidden number was " + str(num2)+ "!")
  elif condition == "Higher" and response.content == "same":
    await ctx.send("You have lost, it was higher!\nThe hidden number was " + str(num2)+ "!")

  elif condition == "Lower" and response.content == "l":
    await ctx.send("You have won!\nThe hidden number was " + str(num2)+ "!")
  elif condition == "Lower" and response.content == "h":
    await ctx.send("You have lost, it was lower!\nThe hidden number was " + str(num2)+ "!")
  elif condition == "Lower" and response.content == "same":
    await ctx.send("You have lost, it was lower!\nThe hidden number was " + str(num2)+ "!")

  elif condition == "Same" and response.content == "same":
    await ctx.send("You have won!\nThe hidden number was " + str(num2)+ "!")
  elif condition == "Same" and response.content =="h":
    await ctx.send("You have lost, the two numbers were the same!\nThe hidden number was " + str(num2)+ "!")
  elif condition == "Same" and response.content =="l":
    await ctx.send("You have lost, the two numbers were the same!\nThe hidden number was " + str(num2)+ "!")
    
@client.command()
async def highlowloop(ctx):
  loop = True
  score = 0
  while loop == True:
    num1 = random.randint(1,100)
    await ctx.send("A random number has been generated, is this number higher or lower than " + str(num1) + "?\nThe number is between 1 and 100!\nType h, l or same!")
    num2 = random.randint(1,100)
    def check(reponse):
      return reponse.channel == ctx.channel and reponse.author == ctx.author
    response = await client.wait_for("message", check=check)
    if response.content != "h" and response.content != "l" and response.content != "same":
      await ctx.send("Invalid reponse! Please respond with l, h or same!\nYour score was " + str(score) + "!")
      break
    if num2 > num1:
      condition = "Higher"
    elif num2 < num1:
      condition = "Lower"
    elif num1 == num2:
      condition = "Same"

    if condition == "Higher" and response.content == "h":
      await ctx.send("You have won!\nThe hidden number was " + str(num2)+ "!")
      score += 1
      loop = True
    elif condition == "Higher" and response.content == "l":
      await ctx.send("You have lost, it was higher!\nThe hidden number was " + str(num2)+ "!\nYour score was " + str(score))
      loop = False
      score = 0
    elif condition == "Higher" and response.content == "same":
      await ctx.send("You have lost, it was higher!\nThe hidden number was " + str(num2)+ "!\nYour score was " + str(score))
      loop = False
      score = 0

    elif condition == "Lower" and response.content == "l":
      await ctx.send("You have won!\nThe hidden number was " + str(num2)+ "!")
      score += 1
      loop = True
    elif condition == "Lower" and response.content == "h":
      await ctx.send("You have lost, it was lower!\nThe hidden number was " + str(num2)+ "!\nYour score was " + str(score))
      loop = False
      score = 0
    elif condition == "Lower" and response.content == "same":
      await ctx.send("You have lost, it was lower!\nThe hidden number was " + str(num2)+ "!\nYour score was " + str(score))
      loop = False
      score = 0

    elif condition == "Same" and response.content == "same":
      await ctx.send("You have won!\nThe hidden number was " + str(num2)+ "!")
      score += 1
      loop = True
    elif condition == "Same" and response.content =="h":
      await ctx.send("You have lost, the two numbers were the same!\nThe hidden number was " + str(num2)+ "!\nYour score was " + str(score))
      loop = False
      score = 0
    elif condition == "Same" and response.content =="l":
      await ctx.send("You have lost, the two numbers were the same!\nThe hidden number was " + str(num2)+ "!\nYour score was " + str(score))
      loop = False
      score = 0