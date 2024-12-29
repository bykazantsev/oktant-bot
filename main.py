import discord
import os
from dotenv import load_dotenv
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
async def on_application_command_error(context, exception):
    if str(exception) == "Application Command raised an exception: NotFound: 404 Not Found (error code: 10062): Unknown interaction":
        logger.error(
            "Не успели ответить на сообщение за 3 секунды, дискорд ответил на команду \"Приложение не отвечает\"")
    else:
        logger.error(f"Возникла какая-то проблема при выполнении команды: {exception}")


if __name__ == "__main__":
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(BOT_TOKEN)
