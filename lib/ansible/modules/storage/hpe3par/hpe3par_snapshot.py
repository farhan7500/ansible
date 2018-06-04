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
short_description: Manage HPE 3PAR Snapshots
author:
  - Farhan Nomani (@farhan7500)
  - Gautham P Hegde (@gautamphegde)
description: On HPE 3PAR - Create Snapshot. - Delete Snapshot. - Modify
 Snapshot.
module: hpe3par_snapshot
options:
  allow_remote_copy_parent:
    description:
      - Allows the promote operation to proceed even if the RW parent volume
       is currently in a Remote Copy volume group, if that group has not been
       started. If the Remote Copy group has been started, this command
       fails.
    type: bool
  base_volume_name:
    description:
      - Specifies the source volume.\nRequired with action present.
  expiration_hours:
    default: 0
    description:
      - Specifies the relative time from the current time that the volume
       expires. Value is a positive integer and in the range of 1 to 43,800
       hours, or 1825 days.
  expiration_time:
    description:
      - Specifies the relative time from the current time that the volume
       expires. Value is a positive integer and in the range of 1 to 43,800
       hours, or 1825 days.
  expiration_unit:
    choices:
      - Hours
      - Days
    default: Hours
    description:
      - Unit of Expiration Time.
  new_name:
    description:
      - New name of the volume.
  priority:
    choices:
      - HIGH
      - MEDIUM
      - LOW
    description:
      - Does not apply to online promote operation or to stop promote
       operation.
  read_only:
    description:
      - Specifies that the copied volume is read-only. false(default) The
       volume is read/write.
    type: bool
  retention_hours:
    default: 0
    description:
      - Specifies the relative time from the current time that the volume
       expires. Value is a positive integer and in the range of 1 to 43,800
       hours, or 1825 days.
  retention_time:
    description:
      - Specifies the relative time from the current time that the volume will
       expire. Value is a positive integer and in the range of 1 to 43,800
       hours, or 1825 days.
  retention_unit:
    choices:
      - Hours
      - Days
    default: Hours
    description:
      - Unit of Retention Time.
  rm_exp_time:
    description:
      - Enables (false) or disables (true) resetting the expiration time. If false, and expiration time value is a positive number, then set.
    type: bool
  snapshot_name:
    description:
      - Specifies a snapshot volume name.
    required: true
  state:
    choices:
      - present
      - absent
      - modify
      - restore_offline
      - restore_online
    description:
      - Whether the specified Snapshot should exist or not. State also provides actions to modify and restore snapshots.
    required: true
extends_documentation_fragment: hpe3par
version_added: 2.7
'''

EXAMPLES = r'''
    - name: Create Volume snasphot my_ansible_snapshot
      hpe3par_snapshot:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: present
        snapshot_name: sample_snapshot
        base_volume_name: sample_base_volume
        read_only: false

    - name: Restore offline Volume snasphot my_ansible_snapshot
      hpe3par_snapshot:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: restore_offline
        snapshot_name: sample_snapshot
        priority: MEDIUM

    - name: Restore offline Volume snasphot my_ansible_snapshot
      hpe3par_snapshot:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: restore_online
        snapshot_name: sample_snapshot

    - name: Modify/rename snasphot my_ansible_snapshot to my_ansible_snapshot_renamed
      hpe3par_snapshot:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: modify
        snapshot_name: sample_snapshot
        new_name: new_snapshot

    - name: Delete snasphot my_ansible_snapshot_renamed
      hpe3par_snapshot:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: absent
        snapshot_name: sample_snapshot
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


def convert_to_hours(time, unit):
    hours = 0
    if unit == 'Days':
        hours = time * 24
    elif unit == 'Hours':
        hours = time
    return hours


def create_snapshot(
        client_obj,
        snapshot_name,
        base_volume_name,
        read_only,
        expiration_time,
        retention_time,
        expiration_unit,
        retention_unit):
    if len(snapshot_name) < 1 or len(snapshot_name) > 31:
        return (False, False, "Snapshot create failed. Snapshot name must be atleast 1 character and not more than 31 characters")
    if base_volume_name is None:
        return (
            False,
            False,
            "Snapshot create failed. Base volume name is null")
    if len(base_volume_name) < 1 or len(base_volume_name) > 31:
        return (False, False, "Snapshot create failed. Base volume name must be atleast 1 character and not more than 31 characters")
    try:
        if not client_obj.volumeExists(snapshot_name):
            optional = {
                'readOnly': read_only,
                'expirationHours': convert_to_hours(
                    expiration_time,
                    expiration_unit),
                'retentionHours': convert_to_hours(
                    retention_time,
                    retention_unit)}
            client_obj.createSnapshot(
                snapshot_name, base_volume_name, optional)
        else:
            return (True, False, "Volume/Snapshot already present")
    except exceptions.ClientException as e:
        return (False, False, "Snapshot creation failed | %s" % (e))
    return (
        True,
        True,
        "Created Snapshot %s successfully." %
        snapshot_name)


def modify_snapshot(
        client_obj,
        snapshot_name,
        new_name,
        expiration_hours,
        retention_hours,
        rm_exp_time):
    if len(snapshot_name) < 1 or len(snapshot_name) > 31:
        return (False, False, "Snapshot create failed. Snapshot name must be atleast 1 character and not more than 31 characters")
    try:
        volume_mods = {
            'expirationHours': expiration_hours,
            'newName': new_name,
            'retentionHours': retention_hours,
            'rmExpTime': rm_exp_time}
        client_obj.modifyVolume(snapshot_name, volume_mods)
    except exceptions.ClientException as e:
        return (False, False, "Modify Snapshot failed | %s" % e)
    return (True, True, "Modified Snapshot %s successfully." % snapshot_name)


def delete_snapshot(
        client_obj,
        snapshot_name):
    if len(snapshot_name) < 1 or len(snapshot_name) > 31:
        return (False, False, "Snapshot create failed. Snapshot name must be atleast 1 character and not more than 31 characters")
    try:
        if client_obj.volumeExists(snapshot_name):
            client_obj.deleteVolume(snapshot_name)
        else:
            return (True, False, "Volume/Snapshot does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Snapshot delete failed | %s" % (e))
    return (
        True,
        True,
        "Deleted Snapshot %s successfully." %
        snapshot_name)


def restore_snapshot_offline(
        client_obj,
        snapshot_name,
        priority,
        allow_remote_copy_parent):
    if len(snapshot_name) < 1 or len(snapshot_name) > 31:
        return (False, False, "Snapshot create failed. Snapshot name must be atleast 1 character and not more than 31 characters")
    try:
        optional = {
            'online': False,
            'allowRemoteCopyParent': allow_remote_copy_parent,
            'priority': getattr(
                client.HPE3ParClient.TaskPriority,
                priority)}
        client_obj.promoteVirtualCopy(snapshot_name, optional)
    except exceptions.ClientException as e:
        return (False, False, "Offline snapshot restore failed | %s" % (e))
    return (
        True,
        True,
        "Restored offline snapshot %s successfully." %
        snapshot_name)


def restore_snapshot_online(
        client_obj,
        snapshot_name,
        allow_remote_copy_parent):
    if len(snapshot_name) < 1 or len(snapshot_name) > 31:
        return (False, False, "Snapshot create failed. Snapshot name must be atleast 1 character and not more than 31 characters")
    try:
        optional = {'online': True,
                    'allowRemoteCopyParent': allow_remote_copy_parent
                    }
        client_obj.promoteVirtualCopy(snapshot_name, optional)
    except exceptions.ClientException as e:
        return (False, False, "Online snapshot restore failed | %s" % (e))
    return (
        True,
        True,
        "Restored online Snapshot %s successfully." %
        snapshot_name)


def main():
    module = AnsibleModule(argument_spec=hpe3par.snapshot_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(
            msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]
    snapshot_name = module.params["snapshot_name"]
    base_volume_name = module.params["base_volume_name"]
    read_only = module.params["read_only"]
    expiration_time = module.params["expiration_time"]
    retention_time = module.params["retention_time"]
    expiration_unit = module.params["expiration_unit"]
    retention_unit = module.params["retention_unit"]
    expiration_hours = module.params["expiration_hours"]
    retention_hours = module.params["retention_hours"]
    priority = module.params["priority"]
    allow_remote_copy_parent = module.params["allow_remote_copy_parent"]
    new_name = module.params["new_name"]
    rm_exp_time = module.params["rm_exp_time"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    # States
    if module.params["state"] == "present":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = create_snapshot(
                client_obj,
                snapshot_name, base_volume_name, read_only, expiration_time,
                retention_time, expiration_unit, retention_unit)
        except Exception as e:
            module.fail_json(msg="Snapshot create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "modify":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = modify_snapshot(
                client_obj,
                snapshot_name, new_name, expiration_hours, retention_hours,
                rm_exp_time)
        except Exception as e:
            module.fail_json(msg="Snapshot modify failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = delete_snapshot(
                client_obj,
                snapshot_name)
        except Exception as e:
            module.fail_json(msg="Snapshot delete failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "restore_offline":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                restore_snapshot_offline(client_obj,
                                         snapshot_name, priority,
                                         allow_remote_copy_parent))
        except Exception as e:
            module.fail_json(msg="Snapshot offline restore failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "restore_online":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = restore_snapshot_online(
                client_obj,
                snapshot_name, allow_remote_copy_parent)
        except Exception as e:
            module.fail_json(msg="Snapshot online restore failed | %s" % e)
        finally:
            client_obj.logout()

    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
