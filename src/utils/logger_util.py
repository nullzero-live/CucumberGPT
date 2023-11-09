import logging
import traceback
from prettytable import PrettyTable
from termcolor import colored

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    handlers = [
        {"cls": logging.StreamHandler, "level": logging.DEBUG, "fmt": '%(name)s - %(levelname)s - %(message)s'},
        {"cls": logging.FileHandler, "level": logging.WARNING, "fmt": '%(asctime)s - %(name)s - %(levelname)s - %(message)s', "filename": './logs/app.log'}
    ]
    
    for h in handlers:
        handler = h["cls"](**{k: v for k, v in h.items() if k != "cls" and k != "level" and k != "fmt"})
        handler.setLevel(h["level"])
        handler.setFormatter(logging.Formatter(h["fmt"]))
        logger.addHandler(handler)
    
    return logger

def pretty_print(data, title):
    table = PrettyTable()
    table.field_names = ["Field", "Value"]
    for key, value in data.items():
        table.add_row([key, value])

    print(colored(title, 'green'))
    print(table)

def log_all_levels(logger):
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

'''if __name__ == "__main__":
    logger = setup_logger('MyApp')
    pretty_print({"Agent": "Research Agent", "Status": "Success"}, "Summary")
    log_all_levels(logger)'''
