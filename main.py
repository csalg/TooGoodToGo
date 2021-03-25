import logging
from time import sleep

from config import *
from lib import TooGoodToGo, Emailer
from queries import ACTIVE_QUERIES


def main():
    logging.basicConfig(level=logging.WARNING)

    too_good_to_go = TooGoodToGo(URL, DATA, HEADERS)
    emailer = Emailer(SERVER, PORT, SENDER_EMAIL, RECEIVER_EMAILS, PASSWORD)

    while True:
        try:
            items = too_good_to_go.get_items_matching(ACTIVE_QUERIES)
            if items:
                for item in items:
                    print(item)
                    emailer.send_items_found_message(item)
            sleep(SERVER_QUERY_INTERVAL)
        except Exception as e:
            logging.error(f'Exception occurred: {e}')
            logging.error(f'Waiting for {WAIT_AFTER_ERROR_INTERVAL} seconds to retry')
            sleep(WAIT_AFTER_ERROR_INTERVAL)

if __name__ == "__main__":
    main()

