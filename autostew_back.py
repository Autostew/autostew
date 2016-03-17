#!/usr/bin/python3

import argparse
import logging
import sys

import requests
from unittest import mock

from autostew_back.gameserver.mocked_api import ApiReplay
from autostew_back.gameserver.server import Server
from autostew_back.settings import Settings

description = """Autostew - A stuff doer for the Project Cars dedicated server"""
epilog = """Don't use --env-init on productive servers!"""


def main(args):
    def start():
        server = Server(settings, args.env_init, args.api_record)
        server.poll_loop(event_offset=args.event_offset, one_by_one=args.api_replay_manual)

    logging.info("Starting autostew")

    settings = Settings()
    try:
        if args.api_replay:
            logging.warning("Mocking gameserver API with {}".format(args.api_replay))
            api = ApiReplay(args.api_replay)
            settings.event_poll_period = 0
            settings.full_update_period = 0
            with mock.patch.object(requests, 'get', api.fake_request):
                start()
        else:
            start()
    except KeyboardInterrupt:
        pass
    except ApiReplay.RecordFinished:
        logging.info("API record ended")

    logging.info("Autostew finished properly")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('--env-init', default=False, action='store_true',
                        help="Initialize environment")
    parser.add_argument('--api-record', nargs='?', const=True, default=False,
                        help="Record API calls")
    parser.add_argument('--api-replay', default=False,
                        help="Replay API calls from this directory")
    parser.add_argument('--api-replay-manual', default=False, action='store_true',
                        help="On API replay, require keypress for each loop")
    parser.add_argument('--event-offset',
                        help="Set initial event offset")
    args = parser.parse_args()
    if args.env_init:
        input("You are about to run env-init. Are you sure? (Enter to continue, ctrl+c to cancel)")
        print("Okay let's do it.")
    sys.exit(main(args))
