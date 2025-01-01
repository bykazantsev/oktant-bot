import datetime, discord
from discord.ext import commands, tasks
from db.punishments import PunishmentsDatabase
from locales import embeds
from utils.logger import Logger

logger = Logger.create_logger("PunishmentsManager")

class PunishmentsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = PunishmentsDatabase()
        self.check_punishments.start()

    @tasks.loop(minutes=1.0)
    async def check_punishments(self):
        punishments = self.db.get_punishments()

        for punishment in punishments:
            punishment_id, user_id, guild_id, punishment_type, reason, _, _, end_timestamp = punishment
            if end_timestamp == "forever":
                return
            if is_punishment_expired(end_timestamp):
                logger.debug(f"Наказание № {punishment_id} ({punishment_type} {user_id}) закончилось")
                await self.unpunish_user(punishment_id, punishment_type, user_id, guild_id)

    @check_punishments.before_loop
    async def before_check(self):
        logger.info('Ждем полной загрузки бота..')
        await self.bot.wait_until_ready()
    
    async def unpunish_user(self, punishment_id, punishment_type, user_id, guild_id):
        guild = self.bot.get_guild(guild_id)
        user = await guild.fetch_member(user_id)
        await notify_user(user, punishment_type, guild)
        if punishment_type == "ban":
            try:
                await guild.unban(user)
            except discord.errors.NotFound:
                logger.error(f"Пользователь {user.name} ({user.id}) не был забанен (discord.errors.NotFound)")
            except discord.errors.Forbidden:
                logger.error(f"У бота не получилось разбанить {user.name} ({user.id}) (discord.errors.Forbidden)")
        self.db.delete_punishment(punishment_id)

def is_punishment_expired(end_timestamp_str):
    end_timestamp = datetime.datetime.fromisoformat(end_timestamp_str)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    return end_timestamp < current_time

async def notify_user(user, punishment_type, guild):
    try:
        await user.send(embed=embeds.punishment_end(punishment_type, guild.name, guild.icon))
    except Exception as e:
        logger.debug(f"Сообщение о снятии наказания не получилось отправить в ЛС: {e}")

def setup(bot):
    bot.add_cog(PunishmentsManager(bot))