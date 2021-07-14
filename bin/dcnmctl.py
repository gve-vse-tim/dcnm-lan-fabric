#!/usr/bin/env python3

import sys
import click

from dcnm_lan_fabric.cli.switch import switch


@click.group(invoke_without_command=True)
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
    """ A CLI interface to the DCNM API """

    ctx.ensure_object(dict)

    ctx.obj['dcnm_host'] = dcnm_host
    ctx.obj['dcnm_user'] = dcnm_user
    ctx.obj['dcnm_pass'] = dcnm_pass
    ctx.obj['dcnm_verify'] = dcnm_verify

# Bolt on all the sub-commands
dcnmctl.add_command(switch, name='switch')

if __name__ == '__main__':
    dcnmctl(obj={})
