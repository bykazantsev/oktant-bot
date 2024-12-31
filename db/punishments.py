import datetime
import sqlite3

class PunishmentsDatabase:
    def __init__(self, db_name="db/punishments.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS punishments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                punishment_type TEXT,
                reason TEXT,
                duration INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_timestamp DATETIME
            )
        """)
        self.connection.commit()

    def add_punishment(self, user_id, guild_id, punishment_type, reason, duration):
        end_timestamp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=duration)

        self.cursor.execute(
            "INSERT INTO punishments (user_id, guild_id, punishment_type, reason, duration, end_timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, guild_id, punishment_type, reason, duration, end_timestamp)
        )
        self.connection.commit()

    def delete_punishment(self, punishment_id):
        self.cursor.execute("DELETE FROM punishments WHERE id = ?", (punishment_id,))
        self.connection.commit()
    def get_punishments(self):
        """Retrieve all punishments from the database."""
        self.cursor.execute("SELECT * FROM punishments")
        return self.cursor.fetchall()

    def get_user_punishments(self, user_id):
        """Retrieve all punishments for a specific user."""
        self.cursor.execute("SELECT * FROM punishments WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.connection.close()

