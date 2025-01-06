import discord
from datetime import datetime
from cogs.economy import get_currency_name


def create_punishment(user_or_mod, action, duration, reason, guild_name: str, guild_icon: str, mod_id=None):
    """
    Создает embed сообщение о выдачи наказания.

    :param user_or_mod: "user" или "mod", указывает тип сообщения (выполучение наказания или выдача наказания).
    :param action: Тип наказания ("ban" или "mute").
    :param duration: Длительность наказания.
    :param reason: Причина наказания.
    :param guild_name: Название сервера.
    :param guild_icon: URL иконки сервера.
    :param mod_id: ID модератора (необязательно).
    
    :return: discord.Embed
    """

    titles = {
        "user": {
            "ban": "Вам была выдана блокировка!",
            "mute": "Вам была выдана блокировка чата!"
        },
        "mod": {
            "ban": "Вы выдали блокировку!",
            "mute": "Вы выдали блокировку чата!"
        }
    }

    title = titles[user_or_mod][action]
    embed = discord.Embed(title=title, color=discord.Color.red())
    embed.set_author(name=guild_name, icon_url=guild_icon)
    embed.add_field(name="Срок наказания:", value=duration, inline=True)
    embed.add_field(name="Причина:", value=reason, inline=True)

    if user_or_mod == "user":
        embed.add_field(name="ID модератора для жалобы:", value=mod_id, inline=True)

    embed.set_footer(text="Oktant Bot")
    embed.timestamp = datetime.now()

    return embed

def green(title, description):
    """
    Создает embed сообщение зеленым цветом.

    :param title: Заголовок сообщения.
    :param description: Описание сообщения.
    
    :return: discord.Embed
    """
    
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    embed.set_footer(text="Oktant Bot")
    embed.timestamp = datetime.now()

    return embed


def red(title, description):
    """
    Создает embed сообщение красным цветом.

    :param title: Заголовок сообщения.
    :param description: Описание сообщения.
    
    :return: discord.Embed
    """
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    embed.set_footer(text="Oktant Bot")
    embed.timestamp = datetime.now()

    return embed


def balance_history(user: discord.abc.User, operations: list, page: int = 1):
    """
    Создает embed сообщение с историей баланса пользователя с поддержкой пагинации.

    :param user: discord.User, пользователь чей баланс нужно вывести.
    :param operations: список кортежей (id, деньги, описание), история баланса.
    :param page: номер страницы для отображения (по умолчанию 1).
    
    :return: discord.Embed
    """
    
    # Определяем количество операций на странице
    items_per_page = 25
    
    # Вычисляем общее количество страниц
    total_pages = (len(operations) + items_per_page - 1) // items_per_page
    
    # Проверяем, что запрашиваемая страница корректна
    if page < 1 or page > total_pages:
        return error("Некорректная страница", "Номер страницы должен быть от 1 до " + str(total_pages))
    
    # Вычисляем индекс начала и конца для текущей страницы
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(operations))
    
    # Создаем embed сообщение
    embed = discord.Embed(title=f"История баланса {user.name} | Страница {page}/{total_pages}", color=discord.Color.blue())
    
    # Добавляем операции на текущей странице в embed
    for operation in operations[start_index:end_index]:
        embed.add_field(name=f"Операция №{operation[0]}", value=f"{get_currency_name(operation[3])} | {operation[4]}", inline=False)
    
    return embed

def punishment_end(punishment_type, guild_name, guild_icon):
    """
    Создает embed сообщение с уведомлением о снятии наказания.

    :param punishment_type: Тип снятого наказания (ban/mute/warn).
    :param guild_name: Название сервера.
    :param guild_icon: URL иконки сервера.
    
    :return: discord.Embed
    """

    titles = {
        "ban": "Ваша блокировка закончилось!",
        "mute": "Ваша блокировка чата закончилось!",
        "warn": "Ваше предупреждение закончилось!"
    }

    title = titles.get(punishment_type, "Ваше наказание закончилось!")
    embed = discord.Embed(title=title, description="Хорошего дня, не нарушайте больше!", color=discord.Color.green())
    embed.set_author(name=guild_name, icon_url=guild_icon)
    embed.set_footer(text="Oktant Bot")
    embed.timestamp = datetime.now()

    return embed


def error(error_text, where):
    """
    Создает embed сообщение об ошибке.

    :param error_text: Описание ошибки.
    :param where: Место, где произошла ошибка.
    
    :return: discord.Embed
    """

    embed = discord.Embed(title="Произошла ошибка в боте!", description="Если это проблема в боте, напишите <@539025449028681749>", color=discord.Color.red())
    embed.add_field(name="Что пошло не так?", value=where, inline=True)
    embed.add_field(name="Подробности:", value=error_text, inline=True)
    embed.set_footer(text="Oktant Bot")

    embed.timestamp = datetime.now()
    return embed