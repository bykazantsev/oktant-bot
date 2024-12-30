import discord
from datetime import datetime

def _user_punishment(duration, reason, mod_id, title="Вам было выдано наказание!"):
    embed = discord.Embed(title=title, color=discord.Color.red())
    embed.add_field(name="Срок наказания:", value=duration, inline=True)
    embed.add_field(name="Причина:", value=reason, inline=True)
    embed.add_field(name="ID модератора для жалобы:", value=mod_id, inline=True)
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed

def _mod_punishment(duration, reason, title="Вы выдали наказание!"):
    embed = discord.Embed(title=title, color=discord.Color.red())
    embed.add_field(name="Срок:", value=duration, inline=True)
    embed.add_field(name="Причина:", value=reason, inline=True)
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed

def green(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed


def red(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.red())
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed


def error(error_text, where):
    embed = discord.Embed(title="Произошла ошибка в боте!", description="Сообщите об этом <@539025449028681749>!", color=discord.Color.red())
    embed.add_field(name="Что пошло не так?", value=where, inline=True)
    embed.add_field(name="Подробности:", value=error_text, inline=True)
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed


def user_ban(duration, reason, mod_id):
    return _user_punishment(duration, reason, mod_id, title="Вам была выдана блокировка!")

def user_mute(duration, reason, mod_id):
    return _user_punishment(duration, reason, mod_id, title="Вам была выдана блокировка чата!")

def mod_ban(duration, reason):
    return _mod_punishment(duration, reason, title="Вы выдали блокировку!")

def mod_mute(duration, reason):
    return _mod_punishment(duration, reason, title="Вы выдали блокировку чата!")