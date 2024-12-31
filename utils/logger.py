import logging


class Logger:
    @classmethod
    def create_logger(cls, name):
        """Создает новый логгер с заданным именем."""
        logger = logging.getLogger(name)

        # Проверяем, установлен ли уровень логирования
        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)

            # Создание обработчика для записи в файл
            handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

            # Создание обработчика для вывода в консоль
            handler_stdout = logging.StreamHandler()
            handler_stdout.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

            # Добавление обработчиков к логгеру
            logger.addHandler(handler_stdout)
            logger.addHandler(handler)

        return logger
