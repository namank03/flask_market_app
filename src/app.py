import logging
import sys
from logging.handlers import RotatingFileHandler

from market import app, db

if __name__ == '__main__':
    db.create_all()
    formatter = logging.Formatter(
        "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
    handler = RotatingFileHandler(
        'logs/SlackBotApp.log', maxBytes=10000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    app.logger.setLevel(logging.DEBUG)
    app.run()
