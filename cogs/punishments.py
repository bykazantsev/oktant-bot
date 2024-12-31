import discord, re
from discord.ext import commands
from db.punishments import PunishmentsDatabase
from locales import embeds
from utils.logger import Logger

logger = Logger.create_logger("Наказания")


class PunishmentsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = PunishmentsDatabase()

    @commands.slash_command(description="Забанить пользователя")
    async def ban(
            self,
            ctx: discord.ApplicationContext,
            user: discord.Option(discord.SlashCommandOptionType.user,
                                 description="Пользователь, которого нужно забанить"),
            reason: discord.Option(str, description="Причина бана"),
            duration: discord.Option(str, description="Продолжительность бана (необязательно)", default=None)
    ):
        await ctx.response.defer(ephemeral=True)

        if ctx.guild is None:
            await ctx.edit(content="Команду нельзя использовать в ЛС!")
            return

        if duration is None:
            duration = "forever"
        else:
            duration = parse_duration(duration)

        self.db.add_punishment(user.id, ctx.guild.id, "ban", reason, duration)
        logger.info(f"{ctx.author.name} забанил {user.name} на {duration} по причине: {reason}")
        await ctx.edit(embed=embeds.mod_ban(duration, reason, ctx.author.guild.name, ctx.author.guild.icon))
        try:
            await user.send(embed=embeds.user_ban(duration, reason, ctx.author.id, ctx.author.guild.name, ctx.author.guild.icon))
        except discord.errors.Forbidden:
            error_message = "Не удалось отправить сообщение в ЛС"
            logger.info(
                f"Сообщение о блокировке {user.name} ({user.id}) не получилось отправить в ЛС (discord.errors.Forbidden)")
            await ctx.edit(
                embeds=[embeds.mod_ban(duration, reason, ctx.author.guild.name, ctx.author.guild.icon), embeds.error("discord.errors.Forbidden", error_message)])
        except Exception as e:
            logger.error(f"Сообщение о блокировке {user.name} ({user.id}) не получилось отправить в ЛС ({e})")
            await ctx.edit(
                embeds=[embeds.mod_ban(duration, reason, ctx.author.guild.name, ctx.author.guild.icon), embeds.error(str(e), "Не удалось отправить сообщение в ЛС")])
        finally:
            await user.ban()


def parse_duration(duration: str) -> int:
    """
    Преобразует строку продолжительности в секунды.

    :param duration: Строка с продолжительностью (например, '1s', '2m', '3d', '4y').
    :return: Общее количество секунд.
    """
    # Определяем множители для различных единиц времени
    time_multipliers = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800,
        'y': 31536000
    }

    total_seconds = 0

    # Регулярное выражение для поиска чисел с единицами
    pattern = re.compile(r'(\d+)([smhdwy])')

    # Ищем все совпадения в строке
    matches = pattern.findall(duration)

    for amount, unit in matches:
        amount = int(amount)
        if unit in time_multipliers:
            total_seconds += amount * time_multipliers[unit]

    return total_seconds

def setup(bot):
    bot.add_cog(PunishmentsCog(bot))
