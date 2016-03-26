import logging


class AbstractAttribute:
    type_name_in_list = 'OVERRIDE_ME'
    type_name_in_method = 'OVERRIDE_ME'

    def __init__(self, descriptor, api, subsection=None):
        self.name = descriptor.name
        self._api = api
        self._subsection = subsection
        self._value = None
        self._writable = descriptor.access == "ReadWrite"
        self._writable_next_session = self._writable

    def get(self):
        return self._value

    def update_from_game(self, status):
        if self._subsection is not None:
            self._value = status[self._subsection][self.name]
        else:
            self._value = status[self.name]

    def set_to_game(self, value, copy_to_next=True, for_next_session=False):
        if for_next_session and copy_to_next:
            copy_to_next = False

        method = "set_next_attributes" if for_next_session else "set_attributes"
        params = {
            '{attr.type_name_in_method}_{attr.name}'.format(attr=self): value,
            'copy_to_next': int(copy_to_next)
        }
        self._api._call("session/{method}".format(method=method), params=params)
        self._value = value


class AbstractAttributeLinkedToList(AbstractAttribute):
    def __init__(self, descriptor, api, api_list, list_key_ugly_value, list_key_nice_value='name', subsection=None):
        AbstractAttribute.__init__(self, descriptor, api, subsection)
        self._nice_value = None
        self._list = api_list
        self._list_key_ugly_value = list_key_ugly_value
        self._list_key_nice_value = list_key_nice_value

    def get_nice(self):
        return self._nice_value

    def set_to_game_nice(self, nice_value):
        self.set_to_game(
            self._list.get_list_items(self._list_key_nice_value, nice_value)[0].raw[self._list_key_ugly_value]
        )

    def set_to_game(self, value, copy_to_next=True, for_next_session=True):
        AbstractAttribute.set_to_game(self, value, copy_to_next, for_next_session)
        self._update_nice_value_from_ugly_value()

    def update_from_game(self, status):
        AbstractAttribute.update_from_game(self, status)
        self._update_nice_value_from_ugly_value()

    def _update_nice_value_from_ugly_value(self):
        candidates = self._list.get_list_items(self._list_key_ugly_value, self._value)
        if len(candidates) == 0 and self._value == 0:
            self._nice_value = None
        elif len(candidates) == 1:
            self._nice_value = candidates[0].raw[self._list_key_nice_value]
        elif len(candidates) == 0:
            raise Exception("No matching values for {name}, value {value}".format(self.name, self._value))
        elif len(candidates) > 1:
            raise Exception("Too many matching values for {name}, value {value}".format(self.name, self._value))


class AbstractAttributeLinkedToEnum(AbstractAttribute):
    def __init__(self, descriptor, api, enum, subsection=None):
        AbstractAttribute.__init__(self, descriptor, api, subsection)
        self._nice_value = None
        self._enum = enum

    def get_nice(self):
        return self._nice_value

    def set_to_game_nice(self, nice_value):
        self.set_to_game(nice_value.value)

    def set_to_game(self, value, copy_to_next=True, for_next_session=True):
        AbstractAttribute.set_to_game(self, value, copy_to_next, for_next_session)
        self._update_nice_value_from_ugly_value()

    def update_from_game(self, status):
        AbstractAttribute.update_from_game(self, status)
        self._update_nice_value_from_ugly_value()

    def _update_nice_value_from_ugly_value(self):
        try:
            self._nice_value = self._enum(self._value)
        except ValueError:
            self._nice_value = None


class AbstractFlagAttribute(AbstractAttribute):
    def __init__(self, descriptor, api, flags_enum, subsection=None):
        AbstractAttribute.__init__(self, descriptor, api, subsection)
        self.flags_enum = flags_enum

    def get_flags(self):
        current_flags = self.get()
        result = []
        for flag in self.flags_enum:
            if current_flags & flag.value != 0:
                result.append(flag)
        return result

    def set_flags(self, flags, value):
        def _set_single_flag(flag):
            current_flags = self.get_flags()

            if value:
                if flag not in current_flags:
                    current_flags.append(flag)
            else:
                if flag in current_flags:
                    current_flags.remove(flag)
            self.set_to_game(sum([i.value for i in current_flags]))

        try:
            for flag in flags:
                _set_single_flag(flag)
        except TypeError:
            _set_single_flag(flags)


class AbstractStatusTable:
    def _from_list(self, name):
        return self.attr_list.get_list_items('name', name).pop()

    def update_from_game(self, status):
        for attr in dir(self):
            if isinstance(getattr(self, attr), AbstractAttribute):
                logging.debug("Updating from game: {}".format(attr))
                getattr(self, attr).update_from_game(status)


class StatusList:
    def __init__(self, attr_list, lists, api, element_type, id_attribute):
        self._attr_list = attr_list
        self._lists = lists
        self._api = api
        self._element_type = element_type
        self.elements = []
        self._id_attribute = id_attribute

    def get_by_id(self, id):
        return self.get_by_property(self._id_attribute, id)

    def get_by_property(self, property, value, unique=True):
        result = []
        for element in self.elements:
            if getattr(element, property).get() == value:
                result.append(element)
        if not unique:
            return result
        else:
            if len(result) == 0:
                return None
            elif len(result) > 1:
                raise Exception("More than one matching element found")
            else:
                return result[0]

    def update_from_game(self, status):  # TODO fix this shitty method
        elements_known = [getattr(el, self._id_attribute).get() for el in self.elements]
        elements_update = [el[self._id_attribute] for el in status]

        def diff(a, b):
            b = set(b)
            return [aa for aa in a if aa not in b]

        elements_gone = diff(elements_known, elements_update)
        elements_new = diff(elements_update, elements_known)
        for existing_element in self.elements:
            if getattr(existing_element, self._id_attribute).get() in elements_gone:
                logging.debug("Removing element {} from table {}".format(existing_element, self))
                self.elements.remove(existing_element)
        for new_element in elements_new:
            new_one = self._element_type(self._attr_list, self._lists, self._api)
            for st in status:
                if st[self._id_attribute] == new_element:
                    new_one.update_from_game(st)
            logging.debug("Adding element {} from table {}".format(new_one, self))
            self.elements.append(new_one)

        for existing_element in self.elements:
            for st in status:
                if st[self._id_attribute] == getattr(existing_element, self._id_attribute).get():
                    existing_element.update_from_game(st)