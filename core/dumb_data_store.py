"""
Contains a dummy db connection to use with our api.
"""


class Borg:
    """Allows shared state, similar to singleton."""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class dummmy_db_connection(Borg):
    """dummmy_db_connection A dummy db connection which implements
    some methods from the python redis library - but is actually
    a python dictionary in memory. To mirror a db connection all
    instances of this class point to the same state.
    """

    def __init__(self):
        super().__init__()
        self.store = {}

    def set(self, key, value):

        self.store[key] = value

        return "OK"

    def exists(self, key):

        return key in self.store.keys()

    def get(self, key):

        return self.store[key]
