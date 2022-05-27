#!/usr/bin/env python3


import requests

from .lan_fabric import api as core


class api(core):
    def __init__(self, conn):
        core.__init__(self, conn)


def authenticate(conn, url, user, password, lifetime=30):
    """
    Authentication for DCNM 11.x is different from future versions so let's
    handle those functions here.

    Request: conn, user, password, and lifetime (in seconds)
    Response: dictionary with attributes to be added to requests.session header
    """

    body = {
        "expirationTime": int(lifetime * 1000),
    }

    auth = (user, password)
    response = requests.Session.post(conn, url, json=body, auth=auth)
    response.raise_for_status()

    result = response.json()

    if 'Dcnm-Token' not in result:
        raise Exception('Token not returned:' + result.text)

    conn.headers.update(
        {'Dcnm-Token': result['Dcnm-Token']}
    )

    return True
