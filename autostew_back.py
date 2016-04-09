#!/usr/bin/python3

import argparse
import importlib
import logging
import sys
import traceback

import requests
from unittest import mock

from autostew_back.gameserver.mocked_api import ApiReplay
from autostew_web_session.models.server import Server

description = """Autostew - A stuff doer for the Project Cars dedicated server"""
epilog = """Don't use --env-init on productive servers!"""


def main(server_name: str, env_init: bool, api_record, api_replay_dir, api_replay_manual: bool, event_offset: int, settings_source: str):
    logging.info("Starting autostew")

    server = Server.objects.get(name=server_name)

    settings_module = importlib.import_module('autostew_back.settings.{}'.format(settings_source))
    settings = settings_module.Settings()

    try:
        if api_replay_dir:
            logging.warning("Mocking gameserver API with {}".format(api_replay_dir))
            api = ApiReplay(api_replay_dir)
            settings.event_poll_period = 0
            settings.full_update_period = 0
            with mock.patch.object(requests, 'get', api.fake_request):
                server.back_start()
        else:
            server.back_start()
    except KeyboardInterrupt as e:
        traceback.print_tb(e.__traceback__)
    except ApiReplay.RecordFinished:
        logging.info("API record ended")

    if not env_init:
        server.destroy()

    logging.info("Autostew finished properly")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('--name', '-n', default='TestServer', help="Server name")
    parser.add_argument('--settings', '-s', default='base', help="Settings module")
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
    sys.exit(
        main(args.name, args.env_init, args.api_record, args.api_replay, args.api_replay_manual, args.event_offset)
    )
