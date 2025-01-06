import discord, os
from discord.ext import commands
from db.economy import EconomyDatabase
from locales import embeds
from utils.logger import Logger
from dotenv import load_dotenv

load_dotenv()
logger = Logger.create_logger("Экономика")
currency_names = [os.getenv("currency_name_1"), os.getenv("currency_name_2"), os.getenv("currency_name_3")]

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

        self.db.add_balance(user.id, ctx.guild.id, money, f"admin_add by {ctx.author.id}")
        balance = self.db.get_balance(user.id, ctx.guild.id)
        await ctx.edit(embed=embeds.green("Выдача валюты", f"Вы выдали {user.mention} {get_currency_name(money)}.\nТекущий баланс: {get_currency_name(balance)}"))


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

        self.db.minus_balance(user.id, ctx.guild.id, money, f"admin_minus by {ctx.author.id}")
        balance = self.db.get_balance(user.id, ctx.guild.id)
        await ctx.edit(embed=embeds.red("Вычитание валюты", f"Вы удалили {get_currency_name(money)} у {user.mention}.\nТекущий баланс: {get_currency_name(balance)}"))

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
        await ctx.edit(embed=embeds.green("Выдача валюты", f"Вы установили {get_currency_name(money)} у {user.mention}."))

    
    @commands.slash_command(description="Просмотреть историю баланса")
    async def balance_history(
            self,
            ctx: discord.ApplicationContext,
            user: discord.Option(discord.SlashCommandOptionType.user,
                                 description="Пользователь, история баланса которого нужно просмотреть")
    ):
        await ctx.response.defer(ephemeral=True)

        if ctx.guild is None:
            await ctx.edit(content="Команду нельзя использовать в ЛС!")
            return

        operations = self.db.get_operations(user.id, ctx.guild.id)

        if not operations:
            await ctx.edit(embed=embeds.error("История баланса", f"У {user.mention} нет операций с балансом."))
            return

        view = BalanceHistoryView(user, operations)
        await ctx.edit(embed=embeds.balance_history(user, operations, 1), view=view)

class BalanceHistoryView(discord.ui.View):
    def __init__(self, user, operations):
        super().__init__()
        self.user = user
        self.operations = operations
        self.current_page = 1
        self.items_per_page = 25
        self.total_pages = (len(operations) + self.items_per_page - 1) // self.items_per_page

    async def update_embed(self, interaction):
        embed = embeds.balance_history(self.user, self.operations, self.current_page)
        
        self.children[0].disabled = (self.current_page == 1)
        self.children[1].disabled = (self.current_page == self.total_pages)
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="<<", style=discord.ButtonStyle.primary, disabled=True)
    async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page > 1:
            self.current_page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.primary)
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page < self.total_pages:
            self.current_page += 1
            await self.update_embed(interaction)

def get_currency_name(amount):
    """
    Возвращает название валюты для определенного количества.

    :param amount: int, количество валюты.
    :return: str
    """
    # Округляем до целого числа
    rounded_amount = int(amount)

    if rounded_amount % 10 == 1 and rounded_amount % 100 != 11:
        return f"{amount} {currency_names[0]}"  # один октант
    elif 2 <= rounded_amount % 10 <= 4 and (rounded_amount % 100 < 10 or rounded_amount % 100 >= 20):
        return f"{amount} {currency_names[1]}"  # два или три октанта
    else:
        return f"{amount} {currency_names[2]}"  # много октантов
    

def setup(bot):
    bot.add_cog(EconomyCog(bot))