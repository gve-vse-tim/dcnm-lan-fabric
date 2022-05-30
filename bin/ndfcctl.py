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


import os

import typer
from dcnm_lan_fabric.cli.template import template
from dcnm_lan_fabric.server import session

ndfc_ctl = typer.Typer(no_args_is_help=True)
ndfc_ctl.add_typer(template, name='template', no_args_is_help=True)


def ndfc_version_check(value: str):
    """
    TODO: Is there better way to DRY with supported versions?
    """
    valid_versions = ['11.4', '11.5', '12.0']

    if value[:4] not in valid_versions:
        raise typer.BadParameter(f"Unsupported version: {value}")
    return value


def ndfc_host_check(value: str):
    if value == "" and 'NDFC_HOST' in os.environ:
        return os.environ['NDFC_HOST']
    return value


def ndfc_user_check(value: str):
    if value == "" and 'NDFC_USER' in os.environ:
        return os.environ['NDFC_USER']
    return value


def ndfc_password_check(value: str):
    if value == "" and 'NDFC_PASS' in os.environ:
        return os.environ['NDFC_PASS']
    return value


@ndfc_ctl.callback(no_args_is_help=True)
def ndfc_callback(
    ctx: typer.Context,
    host: str = typer.Option(
        "", help="DCNM/NDFC Server FQDN/IP", callback=ndfc_host_check
    ),
    user: str = typer.Option(
        "", help="DCNM/NDFC account name", callback=ndfc_user_check
    ),
    password: str = typer.Option(
        "", help="DCNM/NDFC account password", callback=ndfc_password_check
    ),
    version: str = typer.Option(
        "12.0", help="DCNM/NDFC Server Version", callback=ndfc_version_check
    ),
    tls: bool = typer.Option(True, help="Verify/Validate TLS Connection"),
):
    """
    CLI Utility to manage DCNM/NDFC instances.
    """

    ctx.ensure_object(dict)

    ctx.obj['session'] = session(host, user, password, tls, version)


if __name__ == '__main__':
    ndfc_ctl(obj={})
