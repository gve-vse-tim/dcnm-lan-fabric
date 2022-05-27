# DCNM Lan Fabric Python Utilities

A Python SDK and set of utilities to manage/automate DCNM LAN Fabric operations.

---

The purposes of this project are to:
- Provide an SDK that leverages the DCNM REST API to implement common tasks
- Provide CLI interfaces into that SDK

## Features

The SDK currently provides:
- Connection management
- Version aware API SDK
- POAP and Device role configuration

The CLI currently supports:
- CLI for assigning devices in POAP stage to a fabric and role

## Solution Components

### Cisco Products / Services

- Cisco Data Center Network Manager, v11.5(1)
  - Earlier versions (11.3(1) and 11.4(1)) while untested should work

## Usage

Documentation to be written.

## Installation

Pre-requisite Python environment - like all good Python users, you'll need a
dedicated virtual environment (venv). Within that venv, you'll install this
SDK Python module via:

```bash
pip install dcnm-lan-fabric
```

That should install the required pre-requisities as well.  In case it does not,
you'll also need the followin Python modules (see requirements.txt):

```bash
pip install -r requirements.txt
```

Alternatively, you could simply leverage the GitHub repository and install the
module directly using setuptools:

```bash
git clone https://github.com/gve-vse-tim/dcnm-lan-fabric
cd dcnm-lan-fabric
# Activate your python environment, e.g.  source install.sh
python -m build
pip install dist/dcnm_lan_fabric-0.?.?-py3-none-any.whl
```

## Documentation

- NDFC 12.x REST API Guide (yet to be published)

- [DCNM 11.5 REST API Guide](https://www.cisco.com/c/en/us/td/docs/dcn/dcnm/1151/restapi/cisco-dcnm-rest-api-guide-1151.html)
- [DevNet DCNM 11.5 REST API Reference Guide](https://developer.cisco.com/docs/data-center-network-manager/11-5-1/)
- [DCNM 11.5 REST API Tool](https://www.cisco.com/c/en/us/td/docs/dcn/dcnm/1151/restapi/cisco-dcnm-rest-api-guide-1151.html#task_etx_dhn_xjb)

