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
short_description: Manage HPE 3PAR Volume Set
author:
  - Farhan Nomani (@farhan7500)
  - Gautham P Hegde (@gautamphegde)
description: On HPE 3PAR - Create Volume Set. - Add Volumes to Volume Set. -
 Remove Volumes from Volume Set.
module: hpe3par_volumeset
options:
  domain:
    description:
      - The domain in which the VV set or host set will be created.
  setmembers:
    description:
      - The virtual volume to be added to the set.\nRequired with action
       add_volumes, remove_volumes.
  state:
    choices:
      - present
      - absent
      - add_volumes
      - remove_volumes
    description:
      - Whether the specified Volume Set should exist or not. State also
       provides actions to add or remove volumes from volume set.
    required: true
  volumeset_name:
    description:
      - Name of the volume set to be created.
    required: true
extends_documentation_fragment: hpe3par
version_added: 2.6
'''

EXAMPLES = r'''
    - name: Create volume set sample_volumeset
      hpe3par_volumeset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: present
        volumeset_name: sample_volumeset
        setmembers: [sample_volume]

    - name: Add volumes to sample_volumeset 
      hpe3par_volumeset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: add_volumes
        volumeset_name: sample_volumeset
        setmembers: [sample_volume2]

    - name: Remove volumes from Volumeset sample_volumeset
      hpe3par_volumeset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: remove_volumes
        volumeset_name: sample_volumeset
        setmembers: [sample_volume2]

    - name: Delete Volumeset sample_volumeset
      hpe3par_volumeset:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: absent
        volumeset_name: sample_volumeset
'''

RETURN = r'''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import hpe3par, basic
try:
    from hpe3par_sdk import client
    from hpe3parclient import exceptions
    HAS_3PARCLIENT = True
except ImportError:
    HAS_3PARCLIENT = False


def create_volumeset(
        client_obj,
        volumeset_name,
        domain,
        setmembers):
    if len(volumeset_name) < 1 or len(volumeset_name) > 27:
        return (False, False, "Volume Set create failed. Volume Set name must be atleast 1 character and not more than 27 characters")
    try:
        if not client_obj.volumeSetExists(volumeset_name):
            client_obj.createVolumeSet(
                volumeset_name, domain, None, setmembers)
        else:
            return (True, False, "volumeset already present")
    except Exception as e:
        return (False, False, "volumeset creation failed | %s" % (e))
    return (
        True,
        True,
        "Created volumeset %s successfully." %
        volumeset_name)


def delete_volumeset(
        client_obj,
        volumeset_name):
    if len(volumeset_name) < 1 or len(volumeset_name) > 27:
        return (False, False, "Volume Set create failed. Volume Set name must be atleast 1 character and not more than 27 characters")
    try:
        if client_obj.volumeSetExists(volumeset_name):
            client_obj.deleteVolumeSet(volumeset_name)
        else:
            return (True, False, "volumeset does not exist")
    except Exception as e:
        return (False, False, "volumeset delete failed | %s" % (e))
    return (
        True,
        True,
        "Deleted volumeset %s successfully." %
        volumeset_name)


def add_volumes(
        client_obj,
        volumeset_name,
        setmembers):
    if len(volumeset_name) < 1 or len(volumeset_name) > 27:
        return (False, False, "Volume Set create failed. Volume Set name must be atleast 1 character and not more than 27 characters")
    if setmembers is None:
        return (
            False,
            False,
            "Add volume to volumeset failed. Setmembers is null")
    try:
        if client_obj.volumeSetExists(volumeset_name):
            existing_set_members = client_obj.getVolumeSet(
                volumeset_name).setmembers
            if existing_set_members is not None:
                new_set_members = list(
                    set(setmembers) - set(existing_set_members))
            else:
                new_set_members = setmembers
            if new_set_members is not None and new_set_members:
                client_obj.addVolumesToVolumeSet(
                    volumeset_name, new_set_members)
            else:
                return (
                    True,
                    False,
                    "No new members to add to the Volume set %s#. Nothing to \
do." %
                    volumeset_name)
        else:
            return (False, False, "Volumeset does not exist")
    except Exception as e:
        return (False, False, "Add volumes to volumeset failed | %s" % (e))
    return (True, True, "Added volumes successfully.")


def remove_volumes(
        client_obj,
        volumeset_name,
        setmembers):
    if len(volumeset_name) < 1 or len(volumeset_name) > 27:
        return (False, False, "Volume Set create failed. Volume Set name must be atleast 1 character and not more than 27 characters")
    if setmembers is None:
        return (
            False,
            False,
            "Remove volume(s) from Volumeset failed. Setmembers is null")
    try:
        if client_obj.volumeSetExists(volumeset_name):
            existing_set_members = client_obj.getVolumeSet(
                volumeset_name).setmembers
            if existing_set_members is not None:
                set_members = list(set(existing_set_members) & set(setmembers))
            else:
                set_members = setmembers
            if set_members is not None and set_members:
                client_obj.removeVolumesFromVolumeSet(
                    volumeset_name, set_members)
            else:
                return (
                    True,
                    False,
                    "No members to remove to the Volume set %s. Nothing to \
do." %
                    volumeset_name)
        else:
            return (True, False, "Volumeset does not exist")
    except Exception as e:
        return (
            False,
            False,
            "Remove volumes from volumeset failed | %s" %
            e)
    finally:
        client_obj.logout()
    return (True, True, "Removed volumes successfully.")


def main():

    module = AnsibleModule(argument_spec=hpe3par.volumeset_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(
            msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]
    volumeset_name = module.params["volumeset_name"]
    domain = module.params["domain"]
    setmembers = module.params["setmembers"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    # States
    if module.params["state"] == "present":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = create_volumeset(
                client_obj,
                volumeset_name, domain, setmembers)
        except Exception as e:
            module.fail_json(msg="Snapshot create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = delete_volumeset(
                client_obj,
                volumeset_name)
        except Exception as e:
            module.fail_json(msg="Snapshot create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "add_volumes":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = add_volumes(
                client_obj,
                volumeset_name, setmembers)
        except Exception as e:
            module.fail_json(msg="Snapshot create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "remove_volumes":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = remove_volumes(
                client_obj,
                volumeset_name, setmembers)
        except Exception as e:
            module.fail_json(msg="Snapshot create failed | %s" % e)
        finally:
            client_obj.logout()

    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
