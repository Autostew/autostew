import json
import logging
import os
from collections import defaultdict

import requests


class ApiConnector:
    def __init__(self, api, target_model, translations):
        self.api = api
        self.object = target_model
        self.translations = translations

    def push_to_game(self, api_type_name, for_next_session = False, copy_to_next = False):
        for i in self.translations:
            if 'enum_model' in i.keys():
                value = getattr(self.object, i['model_field']).ingame_id
            else:
                value = getattr(self.object, i['model_field'])
            method = "set_next_attributes" if for_next_session else "set_attributes"
            params = {
                '{api_type_name}_{api_field}'.format(api_type_name=api_type_name, api_field=i['api_field']): value,
                'copy_to_next': int(copy_to_next)
            }
            self.api._call("session/{method}".format(method=method), params=params)

    def pull_from_game(self, api_result):
        for i in self.translations:
            if 'enum_model' in i.keys():
                setattr(
                    self.object,
                    i['model_field'],
                    i['enum_model'].objects.get_or_create(ingame_id=api_result[i['api_field']])[0]
                )
            else:
                setattr(self.object, i['model_field'], api_result[i['api_field']])


class ApiCaller:
    class ApiResultNotOk(Exception):
        pass

    def __init__(self, server, test_connection=True, show_api_definition=False, record_destination=None):
        self.server = server
        self.event_offset = 0
        self.record_destination = record_destination
        self.record_indexes = defaultdict(int)
        if test_connection:
            self._print_api_version()
        if show_api_definition:
            logging.debug("API definition:")
            logging.debug(self.api_help_parser())

    def _print_api_version(self):
        r = self._call('version')
        logging.info("API version: {}".format(r))
        for k, v in r.items():
            if v not in self.server.settings.api_compatibility[k]:
                logging.warning("{} is {}, not compatible with known versions {}".format(
                    k,
                    v,
                    self.server.settings.api_compatibility[k])
                )

    def _cleanup_parameters(self, value: str):
        return str(value).translate({ord(i): None for i in '?&#'})

    def _call(self, path: str, params={}):  # TODO handle errors
        url = "{url}/api/{path}?{params}".format(
            url=self.server.api_url,
            path=path,
            params='&'.join(
                [
                    "{k}={v}".format(k=self._cleanup_parameters(k), v=self._cleanup_parameters(v))
                    for k, v in params.items()
                ])
        )
        r = requests.get(url)
        if not r.ok:
            message = 'Request to {url} returned {code}'.format(url=url, code=r.status_code)
            logging.warning(message)
            raise self.ApiResultNotOk(message)
        parsed = json.loads(r.text)
        if parsed['result'] != 'ok':
            message = 'Request to {url} result was {result}'.format(url=url, result=parsed['result'])
            logging.warning(message)
            raise self.ApiResultNotOk(message)
        return parsed.get('response', None)

    def record_result(self, type, content):
        with open(os.path.join(
                os.getcwd(),
                self.record_destination,
                "{}-{}-{}.json".format(self.record_indexes['total'], type, self.record_indexes[type])
        ), 'w') as f:
            json.dump(content, f, indent=4)
        self.record_indexes[type] += 1
        self.record_indexes['total'] += 1

    def get_lists(self):
        return self._call('list/all')

    def get_status(self, attributes=True, members=True, participants=True):
        params = {
            'attributes': int(attributes),
            'members': int(members),
            'participants': int(participants)
        }
        result = self._call("session/status", params)
        if self.record_destination:
            self.record_result("status", result)
        return result

    def reset_event_offset(self):
        result = self._call("log/range", {'count': 1, 'offset': -1})
        if result['events']:
            self.event_offset = result['events'][0]['index'] + 1
        else:
            self.event_offset = 0

    def get_new_events(self):
        result = self._call("log/range", {'count': 100, 'offset': self.event_offset})
        if self.record_destination:
            self.record_result("events", result)
        if result['events']:
            self.event_offset = result['events'][-1]['index'] + 1
        return result['events']

    def send_chat(self, message, player_refid=None, prefix='--- '):
        params = {'message': "{}{}".format(prefix, message)}
        if player_refid is not None:
            params['refid'] = player_refid
        try:
            return self._call("session/send_chat", params)
        except self.ApiResultNotOk:
            logging.error("Send chat to {} failed, message was: {}". format(player_refid, message))
            return None

    def kick(self, player_refid, ban_seconds=0):
        params = {'refid': player_refid}
        if ban_seconds:
            params['ban'] = ban_seconds
        try:
            return self._call("session/kick", params)
        except self.ApiResultNotOk:
            logging.error("Kicking player {} failed". format(player_refid))
            return None

    def api_help_parser(self):
        api_desc = self._call('help')
        methods = api_desc['methods']
        output = ''
        for method in methods:
            output += "{name}?{parameters} ({response_type}) {description}\n".format(
                name=method['name'],
                parameters='&'.join([parameter['name'] for parameter in method['parameters']]),
                response_type=method['responsetype'],
                description=method['description'],
            )
        return output
