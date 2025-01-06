import sqlite3


class EconomyDatabase:
    def __init__(self, db_name="db/economy.db"):
        """Инициализация базы данных и создание необходимых таблиц."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """Создание таблиц для хранения балансов и операций."""
        # Таблица для хранения балансов пользователей
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS balances (
                user_id INTEGER,
                guild_id INTEGER,
                balance REAL DEFAULT 0,
                PRIMARY KEY (user_id, guild_id)
            )
        """)

        # Таблица для хранения истории транзакций
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS operations (
                operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                guild_id INTEGER,
                amount REAL,
                reason TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def add_balance(self, user_id, guild_id, amount, reason):
        """
        Добавляет указанное количество валюты на баланс пользователя.
        
        :param user_id: ID пользователя.
        :param guild_id: ID сервера.
        :param amount: Количество валюты.
        :param reason: Причина операции.
        """
        
        # Получаем текущий баланс пользователя
        current_balance = self.get_balance(user_id, guild_id)

        # Если пользователь еще не имеет записи в базе данных
        if current_balance is None:
            # Вставляем новую запись с начальным балансом
            self.cursor.execute("""
                INSERT INTO balances (user_id, guild_id, balance) 
                VALUES (?, ?, ?)
            """, (user_id, guild_id, amount))
        else:
            # Обновляем существующий баланс
            new_balance = current_balance + amount
            self.cursor.execute("""
                UPDATE balances SET balance = ? WHERE user_id = ? AND guild_id = ?
            """, (new_balance, user_id, guild_id))

        self.add_operation(user_id, guild_id, amount, reason)
        self.connection.commit()

    def set_balance(self, user_id, guild_id, amount, reason):
        """
        Устанавливает баланс пользователя.
        
        :param user_id: ID пользователя.
        :param guild_id: ID сервера.
        :param amount: Новое количество валюты.
        :param reason: Причина операции для лога.
        """
        
        # Устанавливаем новый баланс
        self.cursor.execute("""
            INSERT INTO balances (user_id, guild_id, balance) 
            VALUES (?, ?, ?) 
            ON CONFLICT(user_id, guild_id) 
            DO UPDATE SET balance = ?
        """, (user_id, guild_id, amount, amount))

        self.add_operation(user_id, guild_id, amount, reason)
        self.connection.commit()

    def minus_balance(self, user_id, guild_id, amount, reason):
        """
        Вычитает указанное количество валюты с баланса пользователя.

        :param user_id: ID пользователя.
        :param guild_id: ID сервера.
        :param amount: Количество валюты для вычитания.
        :param reason: Причина операции.
        
        :raises ValueError: Если недостаточно средств на счёте.
        """
        
        current_balance = self.get_balance(user_id, guild_id)

        if current_balance is None or current_balance < amount:
            raise ValueError("Недостаточно средств на счете.")

        new_balance = current_balance - amount
        self.cursor.execute("""
            UPDATE balances SET balance = ? WHERE user_id = ? AND guild_id = ?
        """, (new_balance, user_id, guild_id))

        self.add_operation(user_id, guild_id, amount, reason)
        self.connection.commit()

    def get_balance(self, user_id, guild_id):
        """
        Получает текущий баланс пользователя.

        :param user_id: ID пользователя.
        :param guild_id: ID сервера.
        
        :return: Текущий баланс пользователя или None если не найден.
        """
        
        self.cursor.execute("SELECT balance FROM balances WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
        
        result = self.cursor.fetchone()
        
        return result[0] if result else None

    def add_operation(self, user_id, guild_id, amount, reason):
        """Добавляет запись о транзакции в историю операций."""
        
        self.cursor.execute(
            "INSERT INTO operations (user_id, guild_id, amount, reason) VALUES (?, ?, ?, ?)",
            (user_id, guild_id, amount, reason)
        )
        
    def get_operations(self, user_id, guild_id):
        """
        Получает всю историю транзакций пользователя.
        
        :param user_id: ID пользователя.
        :param guild_id: ID сервера.
        
        :return: Список транзакций.
        """
        
        self.cursor.execute("SELECT * FROM operations WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
        
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        
        self.connection.close()
