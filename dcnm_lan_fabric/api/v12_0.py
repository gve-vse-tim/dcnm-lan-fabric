#!/usr/bin/env python3


import requests

from .lan_fabric import api as core


class api(core):
    def __init__(self, conn):
        core.__init__(self, conn)

    # ConfigTemplate - Templates
    def get_templates(self, filterStr: str = None):
        if filterStr:
            query = f"?filterStr={filterStr}"
        else:
            query = ""

        url = f"/configtemplate/rest/config/templates{query}"
        return self.get(url)

    def get_template_by_name(self, name: str, populate: bool = True):
        if populate:
            query = "?populate=true"
        else:
            query = "?populate=false"

        url = f"/configtemplate/rest/config/templates/{name}{query}"
        return self.get(url)


def authenticate(conn: requests.Session, url, user, password, domain="local"):
    """
    Authentication for DCNM 12.x is different from previous versions so let's
    handle those functions here.

    Request: conn, user, password, and domain ('local' for now)
    Response: dictionary with attributes to be added to requests.session header
    """

    body = {
        "userName": user,
        "userPasswd": password,
        "domain": domain
    }

    response = requests.Session.post(conn, url, json=body)
    response.raise_for_status()

    result = response.json()

    if 'jwttoken' not in result:
        raise Exception('Token not returned:' + result.text)

    # Unlike DCNM 11.5 that required a header to be set, NDFC relies on a
    # cookie that will already be stored within the session. So, simply
    # return to the calling routine

    return True
