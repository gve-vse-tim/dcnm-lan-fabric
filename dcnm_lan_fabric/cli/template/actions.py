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


from typing import Optional
import typer

from dcnm_lan_fabric.sdk.template import template

resource = typer.Typer()


@resource.command()
def show(ctx: typer.Context):
    print(ctx.obj['session'])
    return


@resource.command()
def list(
    filter: Optional[str] = typer.Argument(
        None, help="Template Name Search Filter"
    ),
    detail: bool = typer.Option(
        False, help="Detailed Template View"
    )
):
    """
    List some or all of the templates in NDFC. Without args, list of all
    template names generated. With a filter argument, only the subset of
    template names matching the filter will be returned.

    If detail option set, provide template details.
    """

    if filter is None:
        list_of_templates = template.get_all_templates()
        sorted_list = sorted(list_of_templates, key=lambda tmpl: tmpl['name'])

        for tmpl in sorted_list:
            if detail:
                print(f"{tmpl['name']:25}: {tmpl['description']}")
            else:
                print(f"{tmpl['name']}")

        return

    list_of_templates = template.get_template(filter)
    sorted_list = sorted(list_of_templates, key=lambda tmpl: tmpl['name'])

    for tmpl in sorted_list:
        if detail:
            pass
        else:
            pass

    return
