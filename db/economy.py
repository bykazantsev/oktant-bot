import sqlite3


class EconomyDatabase:
    def __init__(self, db_name="db/economy.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Создаем таблицу для хранения балансов
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS balances (
                user_id INTEGER,
                guild_id INTEGER,
                balance REAL DEFAULT 0
            )
        """)

        # Создаем таблицу для хранения истории транзакций
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                amount REAL,
                operation_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def update_balance(self, user_id, guild_id, amount, operation_type):
        self.cursor.execute("""
            SELECT balance FROM balances WHERE user_id = ? AND guild_id = ?
        """, (user_id, guild_id))

        result = self.cursor.fetchone()

        if result is None:
            self.cursor.execute("""
        INSERT INTO balances (user_id, guild_id, balance) VALUES (?, ?, ?)""", (user_id, guild_id, 0))

        self.cursor.execute("""
           UPDATE balances SET balance = ? WHERE user_id = ? AND guild_id = ?
        """, (amount, user_id, guild_id))
        self.add_operation(user_id, guild_id, amount, operation_type)
        self.connection.commit()

    def set_balance(self, user_id, guild_id, amount, operation_type):
            self.cursor.execute("""
                SELECT balance FROM balances WHERE user_id = ? AND guild_id = ?
            """, (user_id, guild_id))

            result = self.cursor.fetchone()

            if result is None:
                self.cursor.execute("""
            INSERT INTO balances (user_id, guild_id, balance) VALUES (?, ?, ?)""", (user_id, guild_id, 0))

            self.cursor.execute("""
                UPDATE balances SET balance = ? WHERE user_id = ? AND guild_id = ?
            """, (amount, user_id, guild_id))
            self.add_operation(user_id, guild_id, amount, operation_type)
            self.connection.commit()

    def minus_balance(self, user_id, guild_id, amount, operation_type):
        # Проверяем, достаточно ли средств на балансе
        self.cursor.execute("""
            SELECT balance FROM balances WHERE user_id = ? AND guild_id = ?
        """, (user_id, guild_id))

        result = self.cursor.fetchone()

        if result is None:
            self.cursor.execute("""
            INSERT INTO balances (user_id, guild_id, balance) VALUES (?, ?, ?)""", (user_id, guild_id, 0))

        current_balance = result[0]

        if current_balance < amount:
            raise ValueError("Недостаточно средств на счете.")

        # Обновляем баланс пользователя
        self.cursor.execute("""
            UPDATE balances SET balance = balance - ? WHERE user_id = ?
        """, (amount, user_id))
        self.add_operation(user_id, guild_id, amount, operation_type)
        self.connection.commit()

    def get_balance(self, user_id, guild_id):
        # Получаем текущий баланс пользователя
        self.cursor.execute("SELECT balance FROM balances WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
        return self.cursor.fetchone()[0] or 0

    def add_operation(self, user_id, guild_id, amount, operation_type):
        # Добавляем запись о транзакции
        self.cursor.execute("INSERT INTO operations (user_id, guild_id, amount, operation_type) VALUES (?, ?, ?, ?)",
                            (user_id, guild_id, amount, operation_type))
        self.connection.commit()

    def get_operations(self, user_id, guild_id):
        # Получаем всю историю транзакций
        self.cursor.execute("SELECT * FROM operations WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
        return self.cursor.fetchall()

    def close(self):
        # Закрываем соединение с базой данных
        self.connection.close()