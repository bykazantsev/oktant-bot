import discord
from discord.ext import commands
from db.economy import EconomyDatabase
from locales import embeds
from utils.logger import Logger

logger = Logger.create_logger("Экономика")

class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = EconomyDatabase()

    @commands.slash_command(description="Выдать определенное количество валюты у пользователя")
    async def add_balance(
            self,
            ctx: discord.ApplicationContext,
            user: discord.Option(discord.SlashCommandOptionType.user,
                                 description="Пользователь, которому нужно выдать валюту"),
            money: discord.Option(int, description="Сколько выдать")
    ):
        await ctx.response.defer(ephemeral=True)

        if ctx.guild is None:
            await ctx.edit(content="Команду нельзя использовать в ЛС!")
            return

        self.db.update_balance(user.id, ctx.guild.id, money, "admin_add")
        balance = self.db.get_balance(user.id)
        await ctx.edit(embed=embeds.green("Выдача валюты", f"Вы выдали {user.mention} {money} валюты.\nТекущий баланс: {balance}"))


    @commands.slash_command(description="Вычесть определенное количество валюты у пользователя")
    async def minus_balance(
            self,
            ctx: discord.ApplicationContext,
            user: discord.Option(discord.SlashCommandOptionType.user,
                                 description="Пользователь, которому нужно вычесть валюту"),
            money: discord.Option(int, description="Сколько выдать")
    ):
        await ctx.response.defer(ephemeral=True)

        if ctx.guild is None:
            await ctx.edit(content="Команду нельзя использовать в ЛС!")
            return

        if money == 0:
            money = self.db.get_balance(user.id, ctx.guild.id)

        self.db.minus_balance(user.id, ctx.guild.id, money, "admin_minus")
        balance = self.db.get_balance(user.id, ctx.guild.id)
        await ctx.edit(embed=embeds.red("Вычитание валюты", f"Вы удалили {money} валюты у {user.mention}.\nТекущий баланс: {balance}"))

    @commands.slash_command(description="Установить определенное количество валюты у пользователя")
    async def set_balance(
            self,
            ctx: discord.ApplicationContext,
            user: discord.Option(discord.SlashCommandOptionType.user,
                                 description="Пользователь, которому нужно установить валюту"),
            money: discord.Option(int, description="Количество валюты")
    ):
        await ctx.response.defer(ephemeral=True)

        if ctx.guild is None:
            await ctx.edit(content="Команду нельзя использовать в ЛС!")
            return

        self.db.set_balance(user.id, ctx.guild.id, money, "admin_set")
        await ctx.edit(embed=embeds.green("Выдача валюты", f"Вы установили {money} валюты у {user.mention}."))


def setup(bot):
    bot.add_cog(EconomyCog(bot))