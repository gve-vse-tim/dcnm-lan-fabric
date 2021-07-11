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

import os
import json

from dcnm_lan_fabric.server import session


def connect(conn_fname, secure):
    """
    If the connection file is provided via CLI, it takes precedence
    over the environment variables.

    This is a bit counterintuitive from general industry practices but
    makes more sense since you have to manually input
    """

    keys = ['DCNM_HOST', 'DCNM_USER', 'DCNM_PASS']

    if os.path.exists(conn_fname):
        with open(conn_fname, 'r') as f:
            data = json.load(f)
    else:
        data = os.environ

    # Validation and arg building
    args = []
    for k in keys:
        if k not in data:
            raise Exception('Conn data {0} missing'.format(k))
        args.append(data[k])

    # Blame PEP8 and Flake for this args trick
    return session(args[0], args[1], args[2], secure=secure)
