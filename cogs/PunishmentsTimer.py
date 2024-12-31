import discord, datetime
from discord.ext import commands, tasks
from db.punishments import PunishmentsDatabase
from locales import embeds
from utils.logger import Logger

logger = Logger.create_logger("Таймер снятия наказаний")

class PunishmentsTimerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = PunishmentsDatabase()
        self.check_punishments.start()

    @tasks.loop(minutes=1.0)
    async def check_punishments(self):
        punishments = self.db.get_punishments()

        for punishment in punishments:
            punishment_id, user_id, guild_id, punishment_type, reason, _, _, end_timestamp = punishment

            if self.is_punishment_expired(end_timestamp):
                logger.debug(f"Наказание № {punishment_id} ({punishment_type} {user_id}) закончилось")

                guild = self.bot.get_guild(guild_id)
                logger.debug(guild)
                user = await guild.fetch_member(user_id)
                logger.debug(user)
                await self.notify_user(user, punishment_type, reason, guild)
                if punishment_type == "ban":
                    await guild.unban(user)
                self.db.delete_punishment(punishment_id)

    def is_punishment_expired(self, end_timestamp_str):
        end_timestamp = datetime.datetime.fromisoformat(end_timestamp_str)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        return end_timestamp < current_time

    async def notify_user(self, user, punishment_type, reason, guild):
        try:
            await user.send(embed=embeds.user_punishment_end(punishment_type, guild.name, guild.icon))
        except Exception as e:
            logger.debug(f"Сообщение о снятии наказания не получилось отправить в ЛС: {e}")

    @check_punishments.before_loop
    async def before_check(self):
        logger.info('Ждем полной загрузки бота..')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(PunishmentsTimerCog(bot))