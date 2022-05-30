#!/usr/bin/env python3

class api:
    def __init__(self, conn):
        self._conn = conn

    # General REST functions
    def get(self, url):
        """
        api.get(self, url):
            assumption is that all responses are JSON
        """

        result = self._conn.get(url)
        result.raise_for_status()

        return result.json()

    def post(self, url, **kwargs):
        """
        api.post(self, url):
            assumption is that all responses are JSON
        """

        result = self._conn.post(url, **kwargs)
        result.raise_for_status()

        return result.json()

    def put(self, url, **kwargs):
        """
        api.put(self, url):
            assumption is that all responses are JSON
        """

        result = self._conn.put(url, **kwargs)
        result.raise_for_status()

        return result.json()
