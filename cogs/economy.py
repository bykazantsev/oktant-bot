import discord
from discord.ext import commands
from db.database import EconomyDatabase
from utils.logger import Logger

logger = Logger.get_logger()

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EconomyDatabase()

    @commands.slash_command(description="Выдать определенное количество валюты в боте")
    async def add_balance(
            self,
            ctx,
            user: discord.Option(discord.SlashCommandOptionType.user,
                                 description="Пользователь, которому нужно выдать валюты"),
            money: discord.Option(int, description="Сколько выдать")
    ):
        await ctx.response.defer(ephemeral=True)

        if ctx.guild is None:
            await ctx.edit(content="Команду нельзя использовать в ЛС!")
            return
        self.db.update_balance(user.id, money)
        await ctx.edit(content=f"Выдали {money} валюты {user.mention}")


def setup(bot):
    bot.add_cog(EconomyCog(bot))