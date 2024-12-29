import sqlite3

class Database:
    def __init__(self, db_name="db/bans.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                user_id INTEGER,
                reason TEXT,
                duration TEXT
            )
        """)
        self.connection.commit()

    def add_ban(self, user_id, reason, duration):
        self.cursor.execute("INSERT INTO bans (user_id, reason, duration) VALUES (?, ?, ?)", (user_id, reason, duration))
        self.connection.commit()

    def get_bans(self):
        self.cursor.execute("SELECT * FROM bans")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
