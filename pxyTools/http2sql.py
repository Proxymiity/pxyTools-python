import json
import requests


class H2SException(Exception):
    def __init__(self, r):
        self.status = r.status_code
        self.data = None
        try:
            self.data = r.json()
        except json.decoder.JSONDecodeError:
            self.data = r.content


class H2SNotFound(H2SException):
    pass


class H2SUnauthorized(H2SException):
    pass


class H2SAlreadyExists(H2SException):
    pass


class H2SClientError(H2SException):
    pass


class H2SServerError(H2SException):
    pass


class H2SInterface:
    __slots__ = ("server", "profile", "token", "base", "session")

    def __init__(self, server: str, profile: str, token: str):
        self.server = server
        self.profile = profile
        self.token = token
        self.base = server + "/" + profile
        self.session = requests.Session()
        self.session.headers["APIKey"] = token

    def reload_profiles(self):
        r = self.session.get(f"{self.server}/reload")
        if r.status_code == 200:
            return True
        else:
            self._handle_error_tree(r)

    def create_table(self, table: str):
        r = self.session.post(f"{self.base}/{table}")
        if r.status_code == 200:
            return True
        else:
            self._handle_error_tree(r)

    def delete_table(self, table: str):
        r = self.session.delete(f"{self.base}/{table}")
        if r.status_code == 200:
            return True
        else:
            self._handle_error_tree(r)

    def put(self, table: str, key: str, value: str, pool=None):
        h = {"Pool": pool} if pool else None
        r = self.session.put(f"{self.base}/{table}/{key}", headers=h, data=str(value).encode('utf-8'))
        if r.status_code == 200:
            return True
        else:
            self._handle_error_tree(r)

    def get(self, table: str, key: str, pool=None):
        h = {"Pool": pool} if pool else None
        r = self.session.get(f"{self.base}/{table}/{key}", headers=h)
        if r.status_code == 200:
            return r.content.decode('utf-8')
        elif r.status_code == 204:
            return None
        else:
            self._handle_error_tree(r)

    def delete(self, table: str, key: str, pool=None):
        h = {"Pool": pool} if pool else None
        r = self.session.delete(f"{self.base}/{table}/{key}", headers=h)
        if r.status_code == 200:
            return True
        else:
            self._handle_error_tree(r)

    @staticmethod
    def _handle_error_tree(r):
        if r.status_code == 400:
            raise H2SClientError(r)
        elif r.status_code == 403:
            raise H2SUnauthorized(r)
        elif r.status_code == 404:
            raise H2SNotFound(r)
        elif r.status_code == 409:
            raise H2SAlreadyExists(r)
        elif r.status_code == 500:
            raise H2SServerError(r)
        else:
            raise H2SException(r)
