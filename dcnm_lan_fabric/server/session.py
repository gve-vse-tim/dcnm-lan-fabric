#!/usr/bin/env python3
"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Dr Timothy E Miller <timmil@cisco.com>"
__contributors__ = [
]
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import time

import requests
from urllib3.exceptions import InsecureRequestWarning

import dcnm_lan_fabric.api


class session(requests.Session):
    def __init__(self, host, user, password, secure=True, lifetime=30):
        """
        Initialize instance with the following information:
          - host: IP or FQDN of DCNM server
          - user, password: valid DCNM credentials with sufficient privileges
            to perform the desired tasks
          - secure: true if we need to validate the TLS/SSL certificates
          - lifetime: session lifetime (in seconds) to request for DCNM token
        """

        requests.Session.__init__(self)

        self.__host = host
        self.__user = user
        self.__password = password
        self.__secure = secure
        self.__lifetime = lifetime

        self.__url = 'https://{0}/rest'.format(host)

        # When was last authentication and the token returned
        self.__last = None

        # Validate SSL or not
        if not self.__secure:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # If HTTP, ensure we always pass verify=False in session
        self.verify = self.__secure

        # Update headers for JSON operations
        self.headers.update(
            {'Content-Type': 'application/json'}
        )

        # Server DCNM version (exception error if can't connect)
        self.version = self._check_version()

        # Provide caching of the api object, if needed.
        self._api = None

    # Some light overloading to make the api calls here reflect
    # the API documentation (/logon)
    def get(self, url, **kwargs):
        """
        HTTP GET method call
         - Ensures login credentials are fresh
         - URL should be DCNM API endpoint
        """

        self.logon()

        url = self.__url + url
        return requests.Session.get(self, url, **kwargs)

    def post(self, url, **kwargs):
        """
        HTTP POST method call
         - Ensures login credentials are fresh
         - URL should be DCNM API endpoint
        """

        self.logon()

        url = self.__url + url
        return requests.Session.post(self, url, **kwargs)

    def _check_version(self):
        """
        Internal method for this class to fetch DCNM service version
        """
        url = self.__url + '/dcnm-version'

        # Call parent class method because version doesn't require login
        response = requests.Session.get(self, url)
        response.raise_for_status()

        result = response.json()
        if 'Dcnm-Version' not in result:
            raise Exception('Version key not in {0}'.format(result.keys()))

        return result['Dcnm-Version']

    def _token_is_current(self):
        """
        Internal method for this class to check if authentication token
        is still valid.
        """
        if self.__last is None:
            return False

        # If we are within 10 seconds of expiration, re-auth
        since = time.time() - self.__last - 10
        if since > (self.__lifetime):
            return False

        # Token is fresh
        return True

    def logon(self):
        """
        If there is no valid token, connect to DCNM server to authenticate
        using object parameters and process the returned token. This SDK
        stores lifetime in seconds but DCNM requires values in milliseconds.
        """
        if self._token_is_current():
            return

        url = self.__url + '/logon'
        auth = (self.__user, self.__password)
        body = {
            "expirationTime": int(self.__lifetime * 1000),
        }

        # Call parent class method to prevent recursive logon() loop
        response = requests.Session.post(self, url, json=body, auth=auth)
        response.raise_for_status()

        result = response.json()
        if 'Dcnm-Token' not in result:
            raise Exception('Token not returned:' + result.text)

        # requests.Session behavior is to update the existing entry
        # so no need to delete the old one.
        self.headers.update(
            {'Dcnm-Token': result['Dcnm-Token']}
        )

    def logout(self):
        """
        If there is a valid token, invalidate it in the DCNM server.
        If token exists in this requests.sessions, remove the token
        from the headers.
        """
        if self._token_is_current():
            url = '/logout'

            response = self.post(url)
            response.raise_for_status()

        # Token is either invalidated or expired now
        if 'Dcnm-Token' in self.headers:
            self.headers.pop('Dcnm-Token')

    def api(self):
        """
        Based on DCNM server version, generate the API object in order
        to reference the correct methods/endpoints for this SDK.
        """
        self.logon()

        if self._api is None:
            if self.version == '11.5(1)':
                self._api = dcnm_lan_fabric.api.v11_5(self)

        return self._api
