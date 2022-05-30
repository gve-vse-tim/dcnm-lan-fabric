#!/usr/bin/env python3
"""
Copyright (c) 2022 Cisco and/or its affiliates.

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
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
from urllib3.exceptions import InsecureRequestWarning

import dcnm_lan_fabric.api


class session(requests.Session):
    def __init__(self, host, user, password, secure=True, version='12.0'):
        """
        Initialize instance with the following information:
          - host: IP or FQDN of DCNM server
          - user, password: valid DCNM credentials with sufficient privileges
            to perform the desired tasks
          - secure: true if we need to validate the TLS/SSL certificates
          - version: DCNM/NDFC version - examples 11.5(1) or 12.0(2f)
        """

        requests.Session.__init__(self)

        self.__host = host
        self.__user = user
        self.__password = password
        self.__secure = secure

        self.__version = version
        self.__base_url = f"https://{host}"

        if self.__version[:2] == "11":
            self.__url = f"{self.__base_url}/rest"
        else:
            self.__url = f"{self.__base_url}/appcenter/cisco/ndfc/api/v1"  # noqa:E501

        # Validate SSL or not
        if not self.__secure:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # If HTTP, ensure we always pass verify=False in session
        self.verify = self.__secure

        # Update headers for JSON operations
        self.headers.update(
            {'Content-Type': 'application/json'}
        )

        # Are we authenticated to DCNM/NDFC
        self.__authenticated = False

        # Provide caching of the api object, if needed.
        self._api = None

    # Add dunder to print something meaningful about the session
    def __str__(self):
        """
        Print host, user, tls, and connections status
        """

        return f"ndfc.requests.Session: {self.__user}@{self.__host}, status {self.__authenticated}"  # noqa:E501

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

        # Not clear if NDFC actually has a version API any longer
        if self.__version[:2] == "12":
            return self.__version

        # Remainder of code is for DCNM 11.x
        url = self.__url + '/dcnm-version'

        # Call parent class method because version doesn't require login
        response = requests.Session.get(self, url)
        response.raise_for_status()

        result = response.json()
        if 'Dcnm-Version' not in result:
            raise Exception('Version key not in {0}'.format(result.keys()))

        # Update the local value
        self.__version = result['Dcnm-Version']
        return self.__version

    def logon(self):
        """
        If there is no valid token, connect to DCNM/NDFC server to authenticate
        using object parameters and process the returned token. This SDK
        stores lifetime in seconds but DCNM requires values in milliseconds.
        """

        if self.__authenticated:
            return

        version = self._check_version()

        if version[:4] == "11.5":
            url = self.__base_url + '/rest/logon'
            return dcnm_lan_fabric.api.dcnm_authenticate(
                self, url, self.__user, self.__password
            )

        if version[:4] == "12.0":
            url = self.__base_url + '/login'
            return dcnm_lan_fabric.api.ndfc_authenticate(
                self, url, self.__user, self.__password
            )

        # Probably should raise an exception here instead
        return False

    def logout(self):
        """
        If there is a valid token, invalidate it in the DCNM server.
        If token exists in this requests.sessions, remove the token
        from the headers.
        """

        # Currently no logout option for NDFC?
        if self.__version[:2] == "12":
            return

        if self.__authenticated:
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
            if self.__version[:4] == '11.5':
                self._api = dcnm_lan_fabric.api.v11_5(self)
            if self.__version[:4] == '12.0':
                self._api = dcnm_lan_fabric.api.v12_0(self)

        return self._api
