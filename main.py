import discord
import os

from discord.ext import commands
from dotenv import load_dotenv

from locales import embeds
from utils.logger import Logger

logger = Logger.get_logger()
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = discord.Bot()

@bot.event
async def on_ready():
    logger.info(f"Авторизовались как {bot.user.name} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="⛷️Зимнее волшебство!"))


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        logger.error(
            "Не успели ответить на сообщение за 3 секунды, дискорд ответил на команду \"Приложение не отвечает\"")
    else:
        await ctx.respond(embed=embeds.error(error, ctx.command.qualified_name))
        logger.error(f"Возникла какая-то проблема при выполнении команды: {error}")


if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(BOT_TOKEN)
