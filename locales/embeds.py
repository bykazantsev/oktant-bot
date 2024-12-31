import discord
from datetime import datetime

def _user_punishment(duration, reason, mod_id, guild_name, guild_icon, title="Вам было выдано наказание!"):
    embed = discord.Embed(title=title, color=discord.Color.red())
    embed.set_author(name=guild_name, icon_url=guild_icon)
    embed.add_field(name="Срок наказания:", value=duration, inline=True)
    embed.add_field(name="Причина:", value=reason, inline=True)
    embed.add_field(name="ID модератора для жалобы:", value=mod_id, inline=True)
    embed.set_footer(text=f"Oktant Bot, {datetime.now().year}")
    return embed

def _mod_punishment(duration, reason, guild_name, guild_icon, title="Вы выдали наказание!"):
    embed = discord.Embed(title=title, color=discord.Color.red())
    embed.set_author(name=guild_name, icon_url=guild_icon)
    embed.add_field(name="Срок:", value=duration, inline=True)
    embed.add_field(name="Причина:", value=reason, inline=True)
    embed.set_footer(text=f"Oktant Bot, {datetime.now().year}")
    return embed

def green(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    embed.set_footer(text=f"Oktant Bot, {datetime.now().year}")
    return embed


def red(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    embed.set_footer(text=f"Oktant Bot, {datetime.now().year}")
    return embed

def user_punishment_end(punishment_type, guild_name, guild_icon):
    punishment_titles = {
        "ban": "Ваша блокировка закончилось!",
        "mute": "Ваша блокировка чата закончилось!",
        "warn": "Ваше предупреждение закончилось!"
    }

    title = punishment_titles.get(punishment_type, "Ваше наказание закончилось!")
    embed = discord.Embed(title=title, description="Хорошего дня, не нарушайте больше!", color=discord.Color.green())
    embed.set_author(name=guild_name, icon_url=guild_icon)
    embed.set_footer(text=f"Oktant Bot, {datetime.now().year}")

    return embed


def error(error_text, where):
    embed = discord.Embed(title="Произошла ошибка в боте!", description="Сообщите об этом <@539025449028681749>!", color=discord.Color.red())
    embed.add_field(name="Что пошло не так?", value=where, inline=True)
    embed.add_field(name="Подробности:", value=error_text, inline=True)
    embed.set_footer(text=f"Oktant Bot, {datetime.now().year}")
    return embed


def user_ban(duration, reason, mod_id, guild_name, guild_icon):
    return _user_punishment(duration, reason, mod_id, guild_name, guild_icon, title="Вам была выдана блокировка!")

def user_mute(duration, reason, mod_id, guild_name, guild_icon,):
    return _user_punishment(duration, reason, mod_id, guild_name, guild_icon, title="Вам была выдана блокировка чата!")

def mod_ban(duration, reason, guild_name, guild_icon):
    return _mod_punishment(duration, reason, guild_name, guild_icon, title="Вы выдали блокировку!")

def mod_mute(duration, reason, guild_name, guild_icon,):
    return _mod_punishment(duration, reason, guild_name, guild_icon, title="Вы выдали блокировку чата!")