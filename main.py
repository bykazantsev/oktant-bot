import discord, os, asyncio

from discord.ext import commands
from dotenv import load_dotenv

from db.economy import EconomyDatabase
from locales import embeds
from utils.logger import Logger


logger = Logger.create_logger("main.py")

logger.debug("Загружаем .env")
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = discord.Bot()

db = EconomyDatabase()

@bot.event
async def on_ready():
    logger.info(f"Авторизовались как {bot.user.name} (ID: {bot.user.id})")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="⛷️Зимнее волшебство!"))


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        logger.error(
            f"Команда '{ctx.command.qualified_name}' не ответила вовремя: {error}")
    try:
        await ctx.respond(embed=embeds.error(error, ctx.command.qualified_name), ephemeral=True)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения об ошибке: {e}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    db.add_balance(message.author.id, message.guild.id, 0.5, "Сообщение в чате")

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel is None and after.channel is not None:        
        while after.channel is not None:
            await asyncio.sleep(600)
            
            voice_state = member.guild.get_member(member.id).voice
            if voice_state and voice_state.channel:
                db.add_balance(member.id, member.guild.id, 10, "Активность в голосовом канале")
            else:
                break


def load_cogs(bot):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                logger.error(f"Не удалось загрузить {filename}: {e}")


if __name__ == "__main__":
    logger.debug("Загружаем коги")
    load_cogs(bot)
    bot.run(BOT_TOKEN)