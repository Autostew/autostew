import logging


class ApiConnector:
    def __init__(self, api, target_model, translations):
        self.api = api
        self.object = target_model
        self.translations = translations

    def push_to_game(self, api_type_name, for_next_session=False, copy_to_next=False, retry=True):
        flag_fields = []
        method = "set_next_attributes" if for_next_session else "set_attributes"
        for translation in self.translations:
            if 'push_if' in translation.keys() and not translation['push_if'](self.object):
                continue
            if 'flag' in translation.keys():
                if not translation['api_field'] in flag_fields:
                    flag_fields.append(translation['api_field'])
                continue
            elif 'enum_model' in translation.keys():
                try:
                    db_object = getattr(self.object, translation['model_field'])
                    if db_object is not None:
                        value = db_object.ingame_id
                except Exception as e:
                    logging.critical("Failed trying to push {}".format(translation['model_field']))
                    raise e
            else:
                value = getattr(self.object, translation['model_field'])
                if type(value) == type(True):
                    value = int(value)
            params = {
                '{api_type_name}_{api_field}'.format(
                    api_type_name=api_type_name,
                    api_field=translation['api_field']
                ): value,
                # 'copy_to_next': int(copy_to_next)
            }
            self.api._call("session/{method}".format(method=method), params=params, retry=retry)

        for flag_field in flag_fields:
            value = 0
            for translation in [translation for translation in self.translations if translation['api_field'] == flag_field]:
                if getattr(self.object, translation['model_field']):
                    value |= translation['flag']
            params = {
                '{api_type_name}_{api_field}'.format(
                    api_type_name=api_type_name,
                    api_field=translation['api_field']
                ): value,
                # 'copy_to_next': int(copy_to_next)
            }
            self.api._call("session/{method}".format(method=method), params=params, retry=retry)

    def pull_from_game(self, api_result):
        for translation in self.translations:
            value = (
                api_result.get(translation['api_field']) if 'subsection' not in translation.keys() else
                api_result.get(translation.get('subsection')).get(translation.get('api_field'))
            )
            if value is None:
                setattr(self.object, translation['model_field'], None)
            elif 'flag' in translation.keys():
                setattr(
                    self.object,
                    translation['model_field'],
                    int(value) & translation['flag'] != 0
                )
            elif 'enum_model' in translation.keys():
                result_model = (
                    translation['enum_model'].get_or_create_default(value) if 'depends_on' not in translation.keys() else
                    translation['enum_model'].get_or_create_default(value, getattr(self.object, translation['depends_on']))
                )
                setattr(
                    self.object,
                    translation['model_field'],
                    result_model
                )
            else:
                setattr(self.object, translation['model_field'], value)