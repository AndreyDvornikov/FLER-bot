import discord
from discord.ext import commands
import os
import json
import requests
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="F!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def archive(ctx):
    date = datetime.now().strftime("%Y-%m-%d")
    progress_message = await ctx.send("Обработано: 0 сообщений")
    num = 0
    channel = ctx.channel
    filename = f"{channel.name}_{date}.json"

    try:
        msgs = []

        async for message in channel.history(
            limit=None,
            oldest_first=True
        ):
            num += 1

            msgs.append({
                "id": message.id,
                "author": str(message.author),
                "content": message.content,
                "date": message.created_at.isoformat()
            })

            if num % 1000 == 0:
                await progress_message.edit(
                    content=f"Обработано: {num} сообщений"
                )

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(msgs, file, ensure_ascii=False, indent=2)

        with open(filename, "rb") as file:
            files = {
                "file": file
            }

            response = requests.post(
                "https://file.io",
                files=files,
                data={
                    "maxDownloads": 1,
                    "autoDelete": "true"
                }
            )

        response.raise_for_status()

        data = response.json()
        link = data["link"]

        await progress_message.edit(
            content=f"Всё записала!\n{link}"
        )

    except Exception as error:
        print(error)
        await progress_message.edit(
            content="Просчиталась! Но где..."
        )


bot.run(os.getenv("DISCORD_TOKEN"))
