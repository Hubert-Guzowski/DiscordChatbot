from tone_analyzer import analyze_tone, results_to_list
import random
import os

from discord.ext import commands
from response_loader import *

BOT_TOKEN = "TOKEN"

bot = commands.Bot(command_prefix='!')


@bot.command(name='hello')
async def hello(ctx):
    response = Hello.hello
    await ctx.send(response)


@bot.command(name='info')
async def info(ctx):
    response = ""
    for command in Help:
        response += command[1] + "\n"
    await ctx.send(response)


@bot.command(name='emotion')
async def emotion(ctx, text):
    result = analyze_tone(text)
    if result:
        if len(results_to_list(result)) == 0:
            await ctx.send(Emotion.indecisive)
        for result in results_to_list(result):
            if result[1] >= 0.8:
                answer = Emotion.intense.format(result[0])
                await ctx.send(answer)
            if 0.8 > result[1] >= 0.3:
                answer = Emotion.normal.format(result[0])
                await ctx.send(answer)
            if result[1] < 0.3:
                answer = Emotion.mild.format(result[0])
                await ctx.send(answer)
    else:
        await ctx.send(Emotion.error)


@bot.command(name='games')
async def games(ctx):
    result = ""
    games_dir = os.path.join(os.path.dirname(__file__), "resources", "games")
    for filename in os.listdir(games_dir):
        with open(os.path.join(games_dir, filename)) as f:
            content = f.read().strip(",").strip()
        result += Games.game.format(filename, content)
    await ctx.send(result)


@bot.command(name='game')
async def game(ctx, title):
    print(title)
    games_dir = os.path.join(os.path.dirname(__file__), "resources", "games")
    cur_user = ctx.author
    with open(os.path.join(games_dir, str(cur_user)), 'a+') as f:
        f.write(", " + title.strip('"'))
    await ctx.send(Games.noted)


@bot.command(name='descriptions')
async def descriptions(ctx):
    result = ""
    descriptions_dir = os.path.join(os.path.dirname(__file__), "resources", "descriptions")
    for filename in os.listdir(descriptions_dir):
        with open(os.path.join(descriptions_dir, filename)) as f:
            content = f.read().strip()
        result += Description.description.format(filename, content)
    await ctx.send(result)


@bot.command(name='description')
async def description(ctx, text):
    print(text)
    descriptions_dir = os.path.join(os.path.dirname(__file__), "resources", "descriptions")
    cur_user = ctx.author
    with open(os.path.join(descriptions_dir, str(cur_user)), 'w') as f:
        f.write(text.strip('"'))
    await ctx.send(Description.noted)


@bot.command(name='joke')
async def joke(ctx):
    jokes_path = os.path.join(os.path.dirname(__file__), "resources", "jokes", "jokes")
    with open(jokes_path) as f:
        content = f.read().split(", ")
    random_joke = random.choice(content)
    await ctx.send(random_joke)


@bot.command(name='addJoke')
async def add_joke(ctx, text):
    jokes_path = os.path.join(os.path.dirname(__file__), "resources", "jokes", "jokes")
    with open(jokes_path, 'a+') as f:
        f.write(", " + text)
    await ctx.send(Jokes.noted)


@bot.command(name='clear')
async def clear(ctx):
    cur_user = ctx.author
    games_dir = os.path.join(os.path.dirname(__file__), "resources", "games")
    descriptions_dir = os.path.join(os.path.dirname(__file__), "resources", "descriptions")

    try:
        os.remove(os.path.join(games_dir, str(cur_user)))
    except OSError:
        pass

    try:
        os.remove(os.path.join(descriptions_dir, str(cur_user)))
    except OSError:
        pass

    await ctx.send(Clear.clear)


# TODO implement
# @bot.command(name='talk')
# async def talk(ctx):
#     if datetime.now() - timedelta(seconds=5) < globals()["ASKED_ON"]:
#         await ctx.send(Talk.wait.format(globals()["CURRENTLY_TALKING"]))
#     else:
#         globals()["ASKED_ON"] = datetime.now()
#         globals()["CURRENT_TOPIC"] = random.choice(Topics.topics)
#         globals()["CURRENTLY_TALKING"] = ctx.author
#         question = Talk.question.format(globals()["CURRENT_TOPIC"])
#         await ctx.send(question)


bot.run(os.getenv(BOT_TOKEN))
