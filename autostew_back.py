import logging
import sys
from autostew_back.gameserver.server import Server


def main():
    logging.info("Starting autostew")
    server = Server()
    server.event_loop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
