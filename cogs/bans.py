import discord
from discord.ext import commands
from db.database import Database
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

        if duration is None:
            duration = "forever"

        self.db.add_ban(user.id, reason, duration)
        logger.info(f"{ctx.author.name} забанил {user.name} на {duration} по причине: {reason}")

        embed = discord.Embed(title="Вы были заблокированы", description=f"На сервере {ctx.guild.name}", color=0x9e0000)
        embed.add_field(name="Срок блокировки", value=duration, inline=True)
        embed.add_field(name="Причина", value=reason, inline=True)
        embed.set_footer(text="© Все права не то что зафырканы, они держатся на синей изоленте")
        try:
            await user.send("sosal?", embed=embed)
        except discord.errors.Forbidden:
            logger.info(f"Сообщение о блокировке {user.name} ({user.id}) не получилось отправить в ЛС (discord.errors.Forbidden)")
            pass

        embed.title = "Выдача блокировки"
        await ctx.edit(content=f"{user.mention} был забанен на {duration} по причине: {reason}")


def setup(bot):
    bot.add_cog(BanCog(bot))
