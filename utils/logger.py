import logging

class Logger:
    _instance = None

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls._instance = cls._create_logger()
        return cls._instance

    @classmethod
    def _create_logger(cls):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)

        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

        handler_stdout = logging.StreamHandler()
        handler_stdout.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

        logger.addHandler(handler_stdout)
        logger.addHandler(handler)

        return logger