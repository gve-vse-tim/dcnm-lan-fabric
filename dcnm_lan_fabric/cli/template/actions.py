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


from typing import List

import typer

from dcnm_lan_fabric.server import session
from dcnm_lan_fabric.sdk.template import template

resource = typer.Typer()


@resource.command()
def show(ctx: typer.Context):
    print(ctx.obj['session'])
    return


@resource.command()
def list(
    ctx: typer.Context,
    filter: str = typer.Option(None, help="Template Name Search Filter"),
    detail: bool = typer.Option(False, help="Detailed Template View")
):
    """
    List some or all of the templates in NDFC. Without args, list of all
    template names generated. With a filter argument, only the subset of
    template names matching the filter will be returned.

    If detail option set, provide template details. (Option is local to CLI and
    not specific to the API)
    """

    # Grab session from context and login
    connection: session = ctx.obj['session']
    connection.logon()

    # Get the corresponding API for the server
    api = connection.api()

    # For "filter by name", we need to add attr to the filter string
    if filter:
        filter = f"name={filter}"

    # Fetch list of template objects
    list_of_templates: List[template.template] = template.get_all_templates(api, filter)  # noqa: E501

    for tmpl in list_of_templates:
        if detail:
            typer.echo(tmpl.summary())
        else:
            typer.echo(tmpl.name)


@resource.command(no_args_is_help=True)
def get(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Exact name of template to fetch"),
    nvpairs: bool = typer.Option(False, help="Simply print the nvpairs"),
    full: bool = typer.Option(False, help="Populate all template attributes"),
    verbose: bool = typer.Option(False, help="Dump entire attribute list")
):
    """
    Detailed information about a specific template. Options will adjust the
    output accordingly:
      - nvPairs option reduces output to just name, default, required
      - verbose outputs all the template attributes
      - full is an API option to populate the metadata attributes
    """

    # Grab session from context and login
    connection: session = ctx.obj['session']
    connection.logon()

    # Get the corresponding API for the server
    api = connection.api()

    tmpl_data = template.get_template(api, name, full)

    if nvpairs:
        pairs = tmpl_data.nvpairs(verbose)
        if len(pairs) == 0:
            typer.echo("No nvPairs found.")
            return

        for name, default, reqd, description in pairs:
            req_str = f"{'required' if reqd else 'optional'}"
            desc_str = f" : {description}" if verbose and description else ''

            # Crop or pad to 80 character string if there is a description
            if verbose:
                if len(desc_str) > 79:
                    desc_str = f"{desc_str[:76]}... "
                else:
                    desc_str = f"{desc_str:80}"

            typer.echo(
                f"({req_str}): {name:35}{desc_str} : {default}"
            )

        return

    if verbose:
        typer.echo(tmpl_data.verbose())
    else:
        typer.echo(tmpl_data.brief())
