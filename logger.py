import logging
import sys


class Logger:
    @staticmethod
    def setup_logger():
        # Configure the logger
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().handlers.clear()
        logger = logging.getLogger('webcam-ha-sensor')
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(console_handler)
        return logger