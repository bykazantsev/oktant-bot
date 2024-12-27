import discord, os, sqlite3, logging
from dotenv import load_dotenv

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


load_dotenv()
bot = discord.Bot()
BOT_TOKEN = os.getenv("BOT_TOKEN")


@bot.event
async def on_ready():
    con = sqlite3.connect("bans.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bans (user_id INTEGER, reason TEXT, duration TEXT)")
    con.commit()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="⛷️Зимнее волшебство!"))
    print(f"Авторизовались как {bot.user.name} (ID: {bot.user.id})")


@bot.slash_command(description="Забанить пользователя")
async def ban(ctx, user: discord.User, reason: str, duration: str = None):
    await ctx.response.defer(ephemeral=True)
    if duration is None:
        duration = "forever"
    con = sqlite3.connect("bans.db")
    cur = con.cursor()
    cur.execute("INSERT INTO bans (user_id, reason, duration) VALUES (?, ?, ?)", (user.id, reason, duration))
    con.commit()

    embed = discord.Embed(title="Вы были заблокированы", description=f"На сервере {ctx.guild.name}",
                          color=0x9e0000)
    embed.add_field(name="Срок блокировки", value=duration, inline=True)
    embed.add_field(name="Причина", value=reason, inline=True)
    embed.set_footer(text="© Все права не то что зафырканы, они держатся на синей изоленте")
    await user.send("sosal?", embed=embed)
    embed.title = "Выдача блокировки"
    await ctx.edit(content=f"{user.mention} был забанен на {duration} по причине: {reason}")
    # await ctx.guild.ban(user)



bot.run(BOT_TOKEN)