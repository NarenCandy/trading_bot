import logging
import os

os.makedirs("logs", exist_ok=True)

def setup_logging():
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("logs/trading_bot.log")
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.INFO)

    # only attach to our bot's loggers, not root (avoids Flasknoise)
    for name in ["bot.client", "bot.orders", "bot.validators", "cli"]:
        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        if not log.handlers:
            log.addHandler(file_handler)

def get_logger(name):
    return logging.getLogger(name)