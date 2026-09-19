import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(

        command_prefix = "F!",
        intents = intents
        )

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def archive(ctx):
    progress_message = await ctx.send("Обработано: 0 сообщений")
    num = 0 
    channel = ctx.channel
    async for message in channel.history(limit=None, oldest_first = True):
        num += 1
        print(message.author, message.content)
        if num % 1000 == 0:
            await progress_message.edit(content=f"Обработано: {num} сообщений")
    await progress_message.edit(content=f"Всё записала!")

bot.run(os.getenv("DISCORD_TOKEN"))
