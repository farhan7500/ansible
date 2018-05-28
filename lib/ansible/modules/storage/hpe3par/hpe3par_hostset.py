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
short_description: "Manage HPE 3PAR Host Set"
author: "Farhan Nomani (nomani@hpe.com)"
description: "On HPE 3PAR - Create Host Set. - Add Hosts to Host Set. - Remove
 Hosts from Host Set."
module: hpe3par_hostset
options:
  domain:
    description:
      - The domain in which the VV set or host set will be created.
    required: false
  hostset_name:
    description:
      - Name of the host set to be created.
    required: true
  setmembers:
    description:
      - The host to be added to the set. Required with action
       add_hosts, remove_hosts
    required: false
  state:
    description:
      - Whether the specified Host Set should exist or not. State also
       provides actions to add or remove hosts from host set
    choices:
      ['present', 'absent', 'add_hosts', 'remove_hosts']
    required: true
extends_documentation_fragment: hpe3par
version_added: 2.6
'''

EXAMPLES = r'''
    - name: Create hostset sample_hostset
      hpe3par_hostset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: present
        hostset_name: sample_hostset
        setmembers: ["sample_host1", "sample_host2"]

    - name: Add hosts to Hostset sample_hostset
      hpe3par_hostset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: add_hosts
        hostset_name: sample_hostset
        setmembers: ["sample_host3"]

    - name: Remove hosts from Hostset sample_hostset
      hpe3par_hostset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: remove_hosts
        hostset_name: sample_hostset
        setmembers: ["sample_host3"]

    - name: Delete Hostset sample_hostset
      hpe3par_hostset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: absent
        hostset_name: sample_hostset
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


def create_hostset(
        client_obj,
        hostset_name,
        domain,
        setmembers):
    try:
        if not client_obj.hostSetExists(hostset_name):
            client_obj.createHostSet(hostset_name, domain, None, setmembers)
        else:
            return (True, False, "Hostset already present")
    except exceptions.ClientException as e:
        return (False, False, "Hostset creation failed | %s" % (e))
    return (True, True, "Created Hostset %s successfully." % hostset_name)


def delete_hostset(
        client_obj,
        hostset_name):
    try:
        if client_obj.hostSetExists(hostset_name):
            client_obj.deleteHostSet(hostset_name)
        else:
            return (True, False, "Hostset does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Hostset delete failed | %s" % (e))
    return (True, True, "Deleted Hostset %s successfully." % hostset_name)


def add_hosts(
        client_obj,
        hostset_name,
        setmembers):
    if setmembers is None:
        return (
            False,
            False,
            "setmembers delete failed. Setmembers is null")
    try:
        if client_obj.hostSetExists(hostset_name):
            existing_set_members = client_obj.getHostSet(
                hostset_name).setmembers
            if existing_set_members is not None:
                new_set_members = list(
                    set(setmembers) - set(existing_set_members))
            else:
                new_set_members = setmembers
            if new_set_members is not None and new_set_members:
                client_obj.addHostsToHostSet(hostset_name, new_set_members)
            else:
                return (
                    True,
                    False,
                    "No new members to add to the Host set %s. Nothing to \
do." % hostset_name)
        else:
            return (False, False, "Hostset does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Add hosts to hostset failed | %s" % e)
    return (True, True, "Added hosts successfully.")


def remove_hosts(
        client_obj,
        hostset_name,
        setmembers):
    if setmembers is None:
        return (
            False,
            False,
            "setmembers delete failed. Setmembers is null")
    try:
        if client_obj.hostSetExists(hostset_name):
            existing_set_members = client_obj.getHostSet(
                hostset_name).setmembers
            if existing_set_members is not None:
                set_members = list(set(setmembers) & set(existing_set_members))
            else:
                set_members = setmembers
            if set_members is not None and set_members:
                client_obj.removeHostsFromHostSet(hostset_name, set_members)
            else:
                return (
                    True,
                    False,
                    "No members to remove from the Host set %s. Nothing to do." %
                    hostset_name,
                )
        else:
            return (True, False, "Hostset does not exist")
    except Exception as e:
        return (False, False, "Remove hosts from hostset failed | %s" % e)
    return (True, True, "Removed hosts successfully.")


def main():

    module = AnsibleModule(argument_spec=hpe3par.hostset_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]
    hostset_name = module.params["hostset_name"]
    domain = module.params["domain"]
    setmembers = module.params["setmembers"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    if len(hostset_name) < 1 or len(hostset_name) > 27:
        rmodule.fail_json(msg="Hostset name must be atleast 1 character and not more than 27 characters")

    # States
    if module.params["state"] == "present":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = create_hostset(
                client_obj, hostset_name, domain, setmembers)
        except Exception as e:
            module.fail_json(msg="Host create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = delete_hostset(
                client_obj, hostset_name)
        except Exception as e:
            module.fail_json(msg="Host create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "add_hosts":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = add_hosts(
                client_obj, hostset_name, setmembers)
        except Exception as e:
            module.fail_json(msg="Host create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "remove_hosts":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = remove_hosts(
                client_obj, hostset_name, setmembers)
        except Exception as e:
            module.fail_json(msg="Host create failed | %s" % e)
        finally:
            client_obj.logout()

    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
