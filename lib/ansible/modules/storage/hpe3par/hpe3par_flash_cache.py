#!/usr/bin/python

# (C) Copyright 2018 Hewlett Packard Enterprise Development LP
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.  Alternatively, at your
# choice, you may also redistribute it and/or modify it under the terms
# of the Apache License, version 2.0, available at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <https://www.gnu.org/licenses/>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = r'''
---
short_description: "Manage HPE 3PAR Flash Cache"
author:
  - Farhan Nomani (@farhan7500)
  - Gautham P Hegde (@gautamphegde)
description: Create and delete Flash Cache on HPE 3PAR.
module: hpe3par_flash_cache
options:
  size_in_gib:
    description:
      - Specifies the node pair size of the Flash Cache on
the system.
    required: true
  mode:
    description:
      - Simulator 1 Real 2 (default)
  state:
    choices:
      - present
      - absent
    description:
      - Whether the specified Flash Cache should exist or not.
    required: true
extends_documentation_fragment: hpe3par
version_added: "2.6"
'''

EXAMPLES = r'''
    - name: Create Flash Cache
      hpe3par_flash_cache:
        storage_system_ip= 10.10.10.1
        storage_system_username= username
        storage_system_password= password
        state=present
        size_in_gib= 64

    - name: Delete Flash Cache
      hpe3par_flash_cache:
        storage_system_ip= 10.10.10.1
        storage_system_username= username
        storage_system_password= password
        state=absent
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import hpe3par
try:
    from hpe3par_sdk import client
    from hpe3parclient import exceptions
    HAS_3PARCLIENT = True
except ImportError:
    HAS_3PARCLIENT = False


def create_flash_cache(
        client_obj,
        size_in_gib,
        mode):
    try:
        if size_in_gib is None:
            return (False, False, "Flash Cache creation failed. Size is null")
        if not client_obj.flashCacheExists():
            client_obj.createFlashCache(size_in_gib, mode)
        else:
            return (True, False, "Flash Cache already present")
    except exceptions.ClientException as e:
        return (False, False, "Flash Cache creation failed | %s" % e)
    finally:
        client_obj.logout()
    return (True, True, "Created Flash Cache successfully.")


def delete_flash_cache(client_obj):
    try:
        if client_obj.flashCacheExists():
            client_obj.deleteFlashCache()
        else:
            return (True, False, "Flash Cache does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Flash Cache delete failed | %s" % e)
    finally:
        client_obj.logout()
    return (True, True, "Deleted Flash Cache successfully.")


def main():

    module = AnsibleModule(argument_spec=hpe3par.flash_cache_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(
            msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["secure"]
    secure = module.params["storage_system_password"]
    size_in_gib = module.params["size_in_gib"]
    mode = module.params["mode"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    # States
    if module.params["state"] == "present":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = create_flash_cache(
                client_obj, size_in_gib, mode)
        except Exception as e:
            module.fail_json(msg="Flash Cache create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = delete_flash_cache(
                client_obj)
        except Exception as e:
            module.fail_json(msg="Flash Cache create failed | %s" % e)
        finally:
            client_obj.logout()

    if return_status:
        module.exit_json(changed=changed, msg=msg)

    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
