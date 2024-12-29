import discord
from discord.ext import commands
from db.database import Database
from embeds import punishments as embeds
from utils.logger import Logger

logger = Logger.get_logger()


class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.slash_command(description="Забанить пользователя")
    async def ban(
            self,
            ctx,
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

        self.db.add_ban(user.id, reason, duration)
        logger.info(f"{ctx.author.name} забанил {user.name} на {duration} по причине: {reason}")

        try:
            await user.send(embed=embeds.user_ban(duration, reason, ctx.author.id))
            await ctx.edit(embed=embeds.mod_ban(duration, reason))
        except discord.errors.Forbidden:
            error_message = "Не удалось отправить сообщение в ЛС"
            logger.info(
                f"Сообщение о блокировке {user.name} ({user.id}) не получилось отправить в ЛС (discord.errors.Forbidden)")
            await ctx.edit(
                embeds=[embeds.mod_ban(duration, reason), embeds.error("discord.errors.Forbidden", error_message)])
        except Exception as e:
            logger.error(f"Сообщение о блокировке {user.name} ({user.id}) не получилось отправить в ЛС ({e})")
            await ctx.edit(
                embeds=[embeds.mod_ban(duration, reason), embeds.error(str(e), "Не удалось отправить сообщение в ЛС")])
        finally:
            await user.ban()

def setup(bot):
    bot.add_cog(BanCog(bot))
