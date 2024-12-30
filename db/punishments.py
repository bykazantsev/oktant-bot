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
                punishment_type TEXT,
                reason TEXT,
                duration TEXT
            )
        """)
        self.connection.commit()

    def add_punishment(self, user_id, punishment_type, reason, duration):
        """Add a new punishment record."""
        self.cursor.execute(
            "INSERT INTO punishments (user_id, punishment_type, reason, duration) VALUES (?, ?, ?, ?)",
            (user_id, punishment_type, reason, duration)
        )
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

