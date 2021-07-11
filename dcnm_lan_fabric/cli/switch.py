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
from dcnm_lan_fabric.actions.core import switch_info
from dcnm_lan_fabric.actions.core import NoPoapSwitches
from dcnm_lan_fabric.actions.core import poap_register_switch
from dcnm_lan_fabric.actions.core import assign_switch_role


# Commands for the switch module
@click.group()
@click.pass_context
def switch(ctx):
    pass

@click.group()
@click.pass_context
def add(ctx):
    """
    Somehow convert this to help docs...

    dcnmctl [global opts] switch add poap FABRIC SW_SER_NUM SW_NAME SW_MGMT0_IP --sw_user SW_USER --sw_pass SW_PASS 
        Note: this will look for a switch with the specified serial number in POAP phase and set the
        switch hostname, mgmt0 IP address, username, and password to the provided values. 

    dcnmctl [global opts] switch add discover FABRIC SW_MGMT0_IP --sw_user SW_USER --sw_pass SW_PASS
        Note: unlike the GUI, it's not practical to walk the network via CLI.  So this CLI is essentially a
        direct add of a single switch given that switch's mgmt0 IP address.
    """
    pass


# Add switches from POAP
@click.command()
@click.option('--sw_user', 'sw_user', envvars='SW_USER',
              help='switch credentials username'
              )
@click.option('--sw_pass', 'sw_pass', envvars='SW_PASS',
              help='switch credentials password'
              )
@click.argument('fabric_name', 
              help='Fabric on which to add switch'
              )
@click.argument('sw_serial',
              help='Switch serial number to identify switch'
              )
@click.argument('sw_name',
              help='Switch name to assign the switch'
              )
@click.argument('sw_ip',
              help='IP Address to assign the switch mgmt0 interface'
              )
def poap(ctx, fabric_name, sw_serial, sw_name, sw_ip, sw_user, sw_pass):
    """
    Register switches in POAP phase to specified fabric with desired identity
    """

    # Retrieve connection from the context
    conn = ctx.obj['dcnm_connection']

    # Create switch data object
    switch_data = switch_info(sw_serial, sw_name, sw_ip, sw_user, sw_pass, "")

    # Register the switches that are at POAP stage
    try:
        results = poap_register_switch(conn, fabric_name, switch_data)
    except NoPoapSwitches:
        print("No switches found")
        sys.exit(1)

    for x in results:
        print("{0}: {1}".format(x, results[x]))


@click.command()
@click.option('--sw_user', 'sw_user', envvars='SW_USER',
              help='switch credentials username'
              )
@click.option('--sw_pass', 'sw_pass', envvars='SW_PASS',
              help='switch credentials password'
              )
@click.argument('fabric_name', 
              help='Fabric on which to add switch'
              )
@click.argument('sw_ip',
              help='IP Address to assign the switch mgmt0 interface'
              )
@click.option('--cfg_erase', 'cfg_erase', envvars='CFG_ERASE',
              is_flag=True, default=False,
              help='If used, switches will have configs erased.'
              )
def discover(ctx, fabric_name, sw_ip, sw_user, sw_pass, cfg_erase):
    """
    Add switches to the fabric that have already
    """

    # Retrieve connection from the context
    conn = ctx.obj['dcnm_connection']

    # If flag enabled, confirm configuration replacement
    if cfg_erase:
        print(f'You will erase configs on {sw_ip} in fabric {fabric_name}')
        print('Confirm [y/N]')
        # Do input check here

    # This functionality not implemented yet
    pass

# Set switch role
@click.command()
@click.option('--sw_user', 'sw_user', envvars='SW_USER',
              help='switch credentials username'
              )
@click.option('--sw_pass', 'sw_pass', envvars='SW_PASS',
              help='switch credentials password'
              )
@click.argument('fabric_name', 
              help='Fabric on which to add switch'
              )
@click.argument('sw_name',
              help='Switch name to assign the new role'
              )
@click.argument('sw_role',
              help='Switch role to assign to switches'
              )
def role(ctx, fabric_name, sw_name, sw_role, sw_user, sw_pass):
    """
    Assign the desired role to the specified switches.
    """

    # Retrieve connection from the context
    conn = ctx.obj['dcnm_connection']

    # Set the role of the switches
    results = assign_switch_role(conn, fabric_name, sw_role, sw_name)

    # output = {
    #     sw.name: switch_role if switch_role else sw.role
    #     for sw in switches if sw.serialNumber in results
    # }

    # for name, role in output.items():
    #     print(f'{name}: {role} assignment success')


# Build the click group heirarchy
add.add_command(poap)
add.add_command(discover)

switch.add_command(add)
switch.add_command(role)
# switch.add_command(delete)

if __name__ == '__main__':
    switch()
