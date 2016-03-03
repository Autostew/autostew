#!/usr/bin/python3

import argparse
import logging
import sys
from autostew_back.gameserver.server import Server


description = """Autostew - A stuff doer for the Project Cars dedicated server"""
epilog = """Don't use --env-init on productive servers!"""


def main(args):
    logging.info("Starting autostew")
    server = Server(args.env_init)
    server.event_loop()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('--env-init', default=False, action='store_true',
                        help="Initialize environment")
    args = parser.parse_args()
    if args.env_init:
        input("You are about to run env-init. Are you sure? (Enter to continue, ctrl+c to cancel)")
    sys.exit(main(args))
