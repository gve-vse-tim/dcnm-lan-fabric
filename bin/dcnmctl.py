#!/usr/bin/env python3

import sys
import click

from dcnm_lan_fabric.server import session
from dcnm_lab_fabric.cli.switch import switch


@click.group()
@click.option('--dcnm_host', 'dcnm_host', envvar='DCNM_HOST',
              help='IP or FQDN of DCNM server'
              )
@click.option('--dcnm_user', 'dcnm_user', envvar='DCNM_USER',
              help='username for DCNM server credentials'
              )
@click.option('--dcnm_pass', 'dcnm_pass', envvar='DCNM_PASS',
              help='password for DCNM server credentials'
              )
@click.option('--dcnm_verify', 'dcnm_verify', envvar='DCNM_VERIFY',
              is_flag=True, default=True,
              help='flag used to request TLS validation, defaults to True'
              )
@click.pass_context
def dcnmctl(ctx, dcnm_host, dcnm_user, dcnm_pass, dcnm_verify):
    # Need to validate DCNM credentials here
    conn = session(dcnm_host, dcnm_user, dcnm_pass, secure=dcnm_verify)

    ctx.ensure_object(dict)
    ctx.obj['dcnm_connection'] = conn


# Bolt on all the sub-commands
dcnmctl.add_command(switch, name='switch')

if __name__ == '__main__':
    dcnmctl(obj={})
