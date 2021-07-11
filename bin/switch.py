#!/usr/bin/env python3
"""
This command is used to manage switches in a given fabric.

The switch extended data (if required) and DCNM connection
information are provided by JSON files or, in the case of
DCNM, environment variables.

"""

import sys
import click

from dcnm_lan_fabric.server import connect
from dcnm_lan_fabric.actions.core import switch_data
from dcnm_lan_fabric.actions.core import NoPoapSwitches
from dcnm_lan_fabric.actions.core import poap_register_switch
from dcnm_lan_fabric.actions.core import assign_switch_role


# Commands for the switch module
@click.group()
def switch():
    pass


# Add switches from POAP
@click.command()
@click.option('--conn', 'conn_fname', default='server.json',
              help='filename of DCNM connection info'
              )
@click.option('--swdata', 'sw_fname', default='switches.json',
              help='filename of switches to add'
              )
@click.option('--fabric', 'fabric_name', required=True,
              help='fabric on which to add switch'
              )
@click.option('--switch', 'switch_name', default=False,
              help='Optionally specify a single switch to process'
              )
@click.option('--secure', 'secure', default=False, is_flag=True,
              help='Validate SSL certificate - defaults to False'
              )
def poap(conn_fname, sw_fname, fabric_name, switch_name, secure):
    """
    Register switches in POAP phase to specified fabric with desired identity
    """
    # From CLI inputs, generate switch data to process
    switches = switch_data(sw_fname, fabric_name, switch_name)

    # Connect to DCNM
    conn = connect(conn_fname, secure)

    # Register the switches that are at POAP stage
    try:
        results = poap_register_switch(conn, fabric_name, switches)
    except NoPoapSwitches:
        print("No switches found")
        sys.exit(1)

    for x in results:
        print("{0}: {1}".format(x, results[x]))


# Set switch role
@click.command()
@click.option('--conn', 'conn_fname', default='server.json',
              help='filename of DCNM connection info'
              )
@click.option('--swdata', 'sw_fname', default='switches.json',
              help='filename of switches to consider'
              )
@click.option('--fabric', 'fabric_name', required=True,
              help='fabric on which to add switch'
              )
@click.option('--switch', 'switch_name', default=False, type=str,
              help='Optionally specify a single switch to process'
              )
@click.option('--role', 'switch_role', default=False, type=str,
              help='Switch role to assign to selected switches'
              )
@click.option('--secure', 'secure', default=False, is_flag=True,
              help='Validate SSL certificate - defaults to False'
              )
def role(conn_fname, sw_fname, fabric_name, switch_name, switch_role, secure):
    """
    Assign the desired role to the specified switches.
    """
    if switch_name == "False":
        switch_name = False
    if switch_role == "False":
        switch_role = False

    # From CLI inputs, generate switch data to process
    switches = switch_data(sw_fname, fabric_name, switch_name)

    # Connect to DCNM
    conn = connect(conn_fname, secure)

    # Set the role of the switches
    results = assign_switch_role(conn, fabric_name, switch_role, switches)

    output = {
        sw.name: switch_role if switch_role else sw.role
        for sw in switches if sw.serialNumber in results
    }

    for name, role in output.items():
        print(f'{name}: {role} assignment success')


# Build the click group heirarchy
switch.add_command(poap)
switch.add_command(role)

if __name__ == '__main__':
    switch()
