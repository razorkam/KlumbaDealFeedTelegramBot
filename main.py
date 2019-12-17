import logging
import threading
from http.server import HTTPServer
from logging.handlers import RotatingFileHandler
from source.TelegramWorker import TgWorker
from source.BitrixWorker import BitrixWorker
from source.HTTPRequestHandler import DealUpdatesHandler
from source.MiscConstants import *

LOG_MAX_SIZE = 2 * 1024 * 1024  # 2 mbytes
LOG_LEVEL = logging.INFO


def http_serve():
    try:
        deals_update_server = HTTPServer((HTTP_SERVER_ADDRESS, HTTP_SERVER_PORT), DealUpdatesHandler)

        while True:
            try:
                deals_update_server.serve_forever()
            except Exception as e:
                logging.error("HTTP server processing exception: ", e)

    except Exception as e:
        logging.error("HTTP server init exception: ", e)


def main():
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    log_handler = RotatingFileHandler('app.log', mode='a', maxBytes=LOG_MAX_SIZE,
                                      backupCount=5)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(LOG_LEVEL)
    logging.getLogger().setLevel(LOG_LEVEL)
    logging.basicConfig(handlers=[log_handler])

    http_daemon = threading.Thread(name='deals_update_server', daemon=True,
                                   target=http_serve)
    http_daemon.start()

    BitrixWorker.load_tokens_store()

    # no message listening needed now
    TgWorker.run()


main()
