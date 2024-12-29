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

class EconomyDatabase:
    def __init__(self, db_name="db/economy.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицу для хранения балансов
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS balances (
                user_id INTEGER PRIMARY KEY,
                balance REAL DEFAULT 0
            )
        """)

        # Создаем таблицу для хранения истории транзакций
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                transaction_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def update_balance(self, user_id, amount):
        # Обновляем баланс пользователя
        self.cursor.execute("""
            INSERT INTO balances (user_id, balance) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?
        """, (user_id, amount, amount))
        self.connection.commit()

    def decrease_balance(self, user_id, amount):
        # Проверяем, достаточно ли средств на балансе
        self.cursor.execute("""
            SELECT balance FROM balances WHERE user_id = ?
        """, (user_id,))

        result = self.cursor.fetchone()

        if result is None:
            raise ValueError("Пользователь не найден.")

        current_balance = result[0]

        if current_balance < amount:
            raise ValueError("Недостаточно средств на счете.")

        # Обновляем баланс пользователя
        self.cursor.execute("""
            UPDATE balances SET balance = balance - ? WHERE user_id = ?
        """, (amount, user_id))

        self.connection.commit()

    def get_balance(self, user_id):
        # Получаем текущий баланс пользователя
        self.cursor.execute("SELECT balance FROM balances WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()[0] or 0

    def add_transaction(self, user_id, amount, transaction_type):
        # Добавляем запись о транзакции
        self.cursor.execute("INSERT INTO transactions (user_id, amount, transaction_type) VALUES (?, ?, ?)",
                            (user_id, amount, transaction_type))
        self.connection.commit()

    def get_transactions(self):
        # Получаем всю историю транзакций
        self.cursor.execute("SELECT * FROM transactions")
        return self.cursor.fetchall()

    def close(self):
        # Закрываем соединение с базой данных
        self.connection.close()