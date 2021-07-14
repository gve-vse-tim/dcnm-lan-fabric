#!/usr/bin/env python3

class api:
    def __init__(self, conn):
        self._conn = conn

    # General REST functions
    def get(self, url):
        """
        api.get(self, url):
            assumption is that all responses are JSON
        """

        result = self._conn.get(url)
        result.raise_for_status()

        return result.json()

    def post(self, url, **kwargs):
        """
        api.post(self, url):
            assumption is that all responses are JSON
        """

        result = self._conn.post(url, **kwargs)
        result.raise_for_status()

        return result.json()

    def put(self, url, **kwargs):
        """
        api.put(self, url):
            assumption is that all responses are JSON
        """

        result = self._conn.put(url, **kwargs)
        result.raise_for_status()

        return result.json()

    # Control - Fabrics
    def get_fabrics(self, name=None):
        """
        get_fabrics(name) - if name provide, get named fabric details.
        Otherwise, provide details for all fabrics.
        """
        if name is None:
            url = '/control/fabrics'
        else:
            url = '/control/fabrics/' + name

        return self.get(url)

    # Control - Inventory
    def get_bootstrap_devices(self, fabric_name):
        """
        get_bootstrap_devices(fabric_name): return a dict of devices that are
        actively in the POAP process (PXE booting against DCNM awaiting POAP
        config)
          - fabric_name required
          - Status code 404 returned if fabric does not exist.
          - Status code 200 returned with JSON list of devices in body
                "serialNumber": "SAL1927JKHQ",
                "model": "N9K-C9372PX",
                "version": "9.3(1)",
                "data": "{\"gateway\": \"10.60.66.1/24\", \"modulesModel\": \"N9K-C9372PX\"]}"  # noqa: E501

        Return dictionary whose key is the serialNumber and the remaining JSON
        data are the dict value assigned.

        """
        url = f'/control/fabrics/{fabric_name}/inventory/poap'
        results = self.get(url)

        return {
            device.pop('serialNumber'): device for device in results
        }

    def create_bootstrap_devices(self, fabric_name, json_data):
        url = f'/control/fabrics/{fabric_name}/inventory/poap'
        results = self.post(url, data=json_data)

        return results

    # Control - Switches
    def set_switch_roles(self, json_data):
        url = '/control/switches/roles'
        results = self.post(url, data=json_data)

        return results

    # DCNM - Inventory
    def get_switch_inventory(self):
        url = '/inventory/switches'
        results = self.get(url)

        return results
