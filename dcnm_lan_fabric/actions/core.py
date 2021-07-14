#!/usr/bin/env python3

import os
import json


class switch_info:
    def __init__(self, serial, name, ip, user, password, role):
        """
        username and password are the discovery username and passwords.
        Assumption is that the 'bare' password will also use the
        discovery password
        """
        self.serialNumber = serial
        self.name = name
        self.mgmt_ip = ip
        self.user = user
        self.password = password
        self.role = role

    def asdict(self):
        return {
            "serialNumber": self.serialNumber,
            "hostname": self.name,
            "ipAddress": self.mgmt_ip,
            "password": self.password,
            "discoveryUsername": self.user,
            "discoveryPassword": self.password,
            "switchRole": self.role
        }

    def json(self):
        return json.dumps(self.asdict())

    def __str__(self):
        return '{0}: {1}, {2}, {3}, {4}'.format(
          self.name, self.serialNumber, self.mgmt_ip, self.user, self.password
        )


class NoPoapSwitches(Exception):
    pass


def switch_data(sw_fname, fabric_name=False, switch_name=False):
    """
    Read all the switch data via JSON and return the data for
    the specified fabric and, optionally, the given switch
    """

    # Load switch data from JSON file
    if not os.path.exists(sw_fname):
        raise Exception('Switch file {0} missing'.format(sw_fname))

    with open(sw_fname, 'r') as f:
        data = json.load(f)

    # Do I need to limit switch data to a given fabric
    if fabric_name is not False:
        if fabric_name not in data:
            raise Exception('Fabric {0} missing'.format(fabric_name))

        fabrics = [fabric_name]
    else:
        fabrics = data.keys()

    switches = []
    for fab_name in fabrics:
        fabric_switches = data[fab_name]

        # Pretty intense list comprehension
        switches += [
            switch_info(
                x['serialNumber'],
                x['hostname'],
                x['ipAddress'],
                x['discoveryUsername'],
                x['discoveryPassword'],
                x['switchRole']
            )
            for x in fabric_switches
            if (
                switch_name is False or x['hostname'] == switch_name
            )
        ]

    return switches


def poap_register_switch(conn, fabric_name, switch):
    """
    poap_register_switch(conn, switch):
        conn - dcnm_lan.server.session.session

    """

    # Current connections API model/version
    api = conn.api()

    # Get list of switches in POAP status
    devices = api.get_bootstrap_devices(fabric_name)

    # Merge data from POAP devices and configuration from user
    configs = []
    for sw in switch:
        if sw.serialNumber not in devices:
            continue
        d = sw.asdict()
        d.update(devices[sw.serialNumber])
        configs.append(d)

    # Verify we have switches to register
    if len(configs) == 0:
        raise NoPoapSwitches()

    # Okay, loop over each device and post it
    output = {}
    for sw in configs:
        json_data = json.dumps([sw])

        # Send updated switches to config
        results = api.create_bootstrap_devices(fabric_name, json_data)

        if 'status' in results:
            output[sw['hostname']] = results['status']
        else:
            output[sw['hostname']] = 'No output returned on success'

    return output


def assign_switch_role(conn, fabric_name, switch_role, switch):
    # Current connections API model/version
    api = conn.api()

    body = []
    for sw in switch:
        role = {
            'serialNumber': sw.serialNumber
        }

        if switch_role:
            role['role'] = switch_role
        else:
            role['role'] = sw.role

        body.append(role)

    results = api.set_switch_roles(json.dumps(body))

    if 'successList' in results:
        return results['successList'].split(',')

    return []


def get_switch_list(conn, fabric_name):
    api = conn.api()

    devices = api.get_switch_inventory()

    switches = [
        {
            'name': sw['logicalName'],
            'ip': sw['ipAddress'],
            'fabric': sw['fabricName']
        }
        for sw in devices
        if (
            fabric_name is None or sw['fabricName'] == fabric_name
        )
    ]

    return switches
