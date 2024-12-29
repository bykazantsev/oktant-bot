import discord
from datetime import datetime

def _user(duration, reason, mod_id, title="Вам было выдано наказание!"):
    embed = discord.Embed(title=title, color=0x9e0000)
    embed.add_field(name="Срок наказания:", value=duration, inline=True)
    embed.add_field(name="Причина:", value=reason, inline=True)
    embed.add_field(name="ID модератора для жалобы:", value=mod_id, inline=True)
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed

def _mod(duration, reason, title="Вы выдали наказание!"):
    embed = discord.Embed(title=title, color=0x9e0000)
    embed.add_field(name="Срок:", value=duration, inline=True)
    embed.add_field(name="Причина:", value=reason, inline=True)
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed


def error(error_text, where):
    embed = discord.Embed(title="Произошла ошибка в боте!", description="Сообщите об этом <@539025449028681749>!", color=0x9e0000)
    embed.add_field(name="Что пошло не так?", value=where, inline=True)
    embed.add_field(name="Подробности:", value=error_text, inline=True)
    embed.set_footer(text=f"Harmony Bot, {datetime.now().year}")
    return embed

def user_ban(duration, reason, mod_id):
    return _user(duration, reason, mod_id, title="Вам была выдана блокировка!")

def user_mute(duration, reason, mod_id):
    return _user(duration, reason, mod_id, title="Вам была выдана блокировка чата!")

def mod_ban(duration, reason):
    return _mod(duration, reason, title="Вы выдали блокировку!")

def mod_mute(duration, reason):
    return _mod(duration, reason, title="Вы выдали блокировку чата!")