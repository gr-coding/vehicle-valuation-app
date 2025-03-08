import logging


class CustomLog:

    @staticmethod
    def log_gen():
        """ Returns a custom logger that can used for Info level logs across the framework
        Returns:
            logger: custom logger for info level logs
        """

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()

        c_format = logging.Formatter("")
        console_handler.setFormatter(c_format)

        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(console_handler)
        logger.propagate = False
        return logger
