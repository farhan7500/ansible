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
short_description: "Manage HPE 3PAR Offline Clone"
author: "Farhan Nomani (nomani@hpe.com)"
description: "On HPE 3PAR - Create Offline Clone. - Delete Clone. - Resync
 Clone. - Stop Cloning."
module: hpe3par_offline_clone
options:
  base_volume_name:
    description:
      - Specifies the source volume. Required with action present, absent,
       stop
  clone_name:
    description:
      - Specifies the destination volume.
    required: true
  dest_cpg:
    description:
      - Specifies the destination CPG for an online copy.
  priority:
    choices:
      - HIGH
      - MEDIUM
      - LOW
    default: MEDIUM
    description:
      - Priority of action.
  save_snapshot:
    description:
      - Enables (true) or disables (false) saving the the snapshot of the
       source volume after completing the copy of the volume.
    type: bool
  skip_zero:
    description:
      - Enables (true) or disables (false) copying only allocated portions of
       the source VV from a thin provisioned source.
    type: bool
  state:
    choices:
      - present
      - absent
      - resync
      - stop
    description:
      - Whether the specified Clone should exist or not. State also provides
       actions to resync and stop clone
    required: true
extends_documentation_fragment: hpe3par
version_added: 2.6
'''

EXAMPLES = r'''
    - name: Create Clone sample_clone
      hpe3par_offline_clone:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: present
        clone_name: sample_clone
        base_volume_name: sample_base_volume
        dest_cpg: sample_cpg
        priority: "MEDIUM"

    - name: Stop Clone {{ clone_name }}
      hpe3par_offline_clone:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: stop
        clone_name: sample_clone
        base_volume_name: sample_base_volume

    - name: Delete clone {{ clone_name }}
      hpe3par_offline_clone:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: absent
        clone_name: sample_clone
        base_volume_name: sample_base_volume
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


def create_offline_clone(
        client_obj,
        clone_name,
        base_volume_name,
        dest_cpg,
        skip_zero,
        save_snapshot,
        priority):
    print ('I am here')
    if base_volume_name is None:
        return (
            False,
            False,
            "Offline clone create failed. Base volume name is null",
        )
    print ('I am here now')
    if len(base_volume_name) < 1 or len(base_volume_name) > 31:
        return (False, False, "Clone create failed. Base volume name must be atleast 1 character and not more than 31 characters")
    print ('I am here now then')
    try:
        if not client_obj.onlinePhysicalCopyExists(
                base_volume_name,
                clone_name) and not client_obj.offlinePhysicalCopyExists(
                    base_volume_name,
                    clone_name):
            optional = {
                'online': False,
                'saveSnapshot': save_snapshot,
                'priority': getattr(
                    client.HPE3ParClient.TaskPriority,
                    priority)}
            if skip_zero:
                optional['skipZero'] = skip_zero
            client_obj.copyVolume(
                base_volume_name,
                clone_name,
                dest_cpg,
                optional)
        else:
            return (
                True,
                False,
                "Clone already exists / creation in progress. Nothing to do.",
                {})
    except Exception as e:
        return (False, False, "Offline Clone creation failed | %s" % (e))
    return (
        True,
        True,
        "Created Offline Clone %s successfully." %
        clone_name)


def resync_clone(
        client_obj,
        clone_name):
    try:
        client_obj.resyncPhysicalCopy(clone_name)
    except Exception as e:
        return (False, False, "Offline clone resync failed | %s" % e)
    return (
        True,
        True,
        "Resync-ed Offline Clone %s successfully." %
        clone_name)


def stop_clone(
        client_obj,
        clone_name,
        base_volume_name):
    if base_volume_name is None:
        return (
            False,
            False,
            "Offline clone stop failed. Base volume name is null",
        )
    if len(base_volume_name) < 1 or len(base_volume_name) > 31:
        return (False, False, "Clone create failed. Base volume name must be atleast 1 character and not more than 31 characters")
    try:
        if client_obj.volumeExists(
            clone_name) and client_obj.offlinePhysicalCopyExists(
                base_volume_name, clone_name):
            client_obj.stopOfflinePhysicalCopy(clone_name)
        else:
            return (True, False, "Offline Cloning not in progress")
    except Exception as e:
        return (False, False, "Offline Clone stop failed | %s" % (e))
    return (
        True,
        True,
        "Stopped Offline Clone %s successfully." %
        clone_name)


def delete_clone(
        client_obj,
        clone_name,
        base_volume_name):
    if base_volume_name is None:
        return (
            False,
            False,
            "Offline clone delete failed. Base volume name is null",
        )
    if len(base_volume_name) < 1 or len(base_volume_name) > 31:
        return (False, False, "Clone create failed. Base volume name must be atleast 1 character and not more than 31 characters")
    try:
        if client_obj.volumeExists(
                clone_name) and not client_obj.onlinePhysicalCopyExists(
                base_volume_name,
                clone_name) and not client_obj.offlinePhysicalCopyExists(
                base_volume_name, clone_name):
            client_obj.deleteVolume(clone_name)
        else:
            return (
                False,
                False,
                "Clone/Volume is busy. Cannot be deleted",
                {})
    except Exception as e:
        return (False, False, "Offline Clone delete failed | %s" % (e))
    return (
        True,
        True,
        "Deleted Offline Clone %s successfully." %
        clone_name)


def main():
    module = AnsibleModule(argument_spec=hpe3par.offline_clone_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]
    clone_name = module.params["clone_name"]
    base_volume_name = module.params["base_volume_name"]
    dest_cpg = module.params["dest_cpg"]
    save_snapshot = module.params["save_snapshot"]
    priority = module.params["priority"]
    skip_zero = module.params["skip_zero"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    if len(clone_name) < 1 or len(clone_name) > 31:
        rodule.fail_json(msg="Clone create failed. Clone name must be atleast 1 character and not more than 31 characters")

    # States
    if module.params["state"] == "present":
        try:
            print ('TATA')
            client_obj.login(storage_system_username, storage_system_password)
            print ('GAGA')
            client_obj.setSSHOptions(
                storage_system_ip,
                storage_system_username,
                storage_system_password)
            print ('LALA')
            return_status, changed, msg = create_offline_clone(
                client_obj, clone_name, base_volume_name, dest_cpg,
                skip_zero, save_snapshot, priority)
        except Exception as e:
            module.fail_json(msg="Clone create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            client_obj.setSSHOptions(
                storage_system_ip,
                storage_system_username,
                storage_system_password)
            return_status, changed, msg = delete_clone(
                client_obj, clone_name, base_volume_name)
        except Exception as e:
            module.fail_json(msg="Clone delete failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "resync":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = resync_clone(
                client_obj, clone_name)
        except Exception as e:
            module.fail_json(msg="Clone resync failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "stop":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            client_obj.setSSHOptions(
                storage_system_ip,
                storage_system_username,
                storage_system_password)
            return_status, changed, msg = stop_clone(
                client_obj, clone_name, base_volume_name)
        except Exception as e:
            module.fail_json(msg="Clone stop failed | %s" % e)
        finally:
            client_obj.logout()
    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
