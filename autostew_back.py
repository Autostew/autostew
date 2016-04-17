#!/usr/bin/python3

import argparse
import importlib
import logging
import sys
import traceback

import requests
from unittest import mock

from django.core.wsgi import get_wsgi_application

from autostew_back import settings

get_wsgi_application()

from autostew_back.ds_api.mocked_api import ApiReplay
from autostew_web_session.models.server import Server

description = """Autostew - A stuff doer for the Project Cars dedicated server"""
epilog = """Don't use --env-init on productive servers!"""


def main(server_id: int, env_init: bool, api_record, api_replay_dir, api_replay_manual: bool, event_offset: int):
    logging.info("Starting autostew")

    server = Server.objects.get(id=server_id)

    try:
        if api_replay_dir:
            logging.warning("Mocking gameserver API with {}".format(api_replay_dir))
            api = ApiReplay(api_replay_dir)
            settings.event_poll_period = 0
            settings.full_update_period = 0
            with mock.patch.object(requests, 'get', api.fake_request):
                server.back_start(settings, env_init=env_init, api_record=api_record)
                server.back_poll_loop()
        else:
            server.back_start(settings, env_init=env_init, api_record=api_record)
            server.back_poll_loop()
    except KeyboardInterrupt as e:
        traceback.print_tb(e.__traceback__)
    except ApiReplay.RecordFinished:
        logging.info("API record ended")

    if not env_init:
        server.back_destroy()

    logging.info("Autostew finished properly")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('--sid', '-i', required=True, help="Server ID")
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
        main(args.sid, args.env_init, args.api_record, args.api_replay, args.api_replay_manual, args.event_offset)
    )
