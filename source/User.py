from enum import Enum
from . import creds


class UserState(Enum):
    PASSWORD_REQUESTED = 1
    AUTHORIZED = 2


class User:
    def __init__(self):
        self._password = None
        self._state = UserState.PASSWORD_REQUESTED
        self._chat_id = None

    # pickle serializing fields
    def __getstate__(self):
        return self._chat_id, self._state, self._password

    def __setstate__(self, dump):
        self._chat_id, self._state, self._password = dump

    def is_pass_requested(self):
        return self._state == UserState.PASSWORD_REQUESTED

    def is_authorized(self):
        return self._state == UserState.AUTHORIZED and self._password == creds.GLOBAL_AUTH_PASSWORD

    def authorize(self, password):
        self._state = UserState.AUTHORIZED
        self._password = password

    def unauthorize(self):
        self._state = UserState.PASSWORD_REQUESTED
        self._password = None
        self._chat_id = None

    def get_password(self):
        return self._password

    def get_chat_id(self):
        return self._chat_id
