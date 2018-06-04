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
short_description: "Manage HPE 3PAR Volume"
author:
  - Farhan Nomani (@farhan7500)
  - Gautham P Hegde (@gautamphegde)
description: On HPE 3PAR - Create Volume. - Delete Volume. - Modify Volume.
 - Grow Volume - Grow Volume to certain size - Change Snap CPG - Change User
 CPG - Convert Provisioning TypeError - Set Snap CPG
module: hpe3par_volume
options:
  compression:
    default: false
    description:
      - Specifes whether the compression is on or off.
    type: bool
  cpg:
    description:
      - Specifies the name of the CPG from which the volume user space will be
       allocated. Required with action present, change_user_cpg.
  expiration_hours:
    default: 0
    description:
      - Remaining time, in hours, before the volume expires.
  keep_vv:
    description:
      - Name of the new volume where the original logical disks are saved.
  new_name:
    description:
      - Specifies the new name for the volume.
  retention_hours:
    default: 0
    description:
      - Sets the number of hours to retain the volume.
  rm_exp_time:
    default: false
    description:
      - Enables false or disables true resetting the expiration time. If
       false, and expiration time value is a positive. number, then set.
    type: bool
  rm_ss_spc_alloc_limit:
    default: false
    description:
      - Enables false or disables true removing the snapshot space allocation
       limit. If false, and limit value is 0, setting  ignored.If false, and
       limit value is a positive number, then set.
    type: bool
  rm_ss_spc_alloc_warning:
    default: false
    description:
      - Enables false or disables true removing the snapshot space allocation
       warning. If false, and warning value is a positive number, then set.
    type: bool
  rm_usr_spc_alloc_limit:
    default: false
    description:
      - Enables false or disables true the allocation limit. If false, and
       limit value is a positive number, then set.
    type: bool
  rm_usr_spc_alloc_warning:
    default: false
    description:
      - Enables false or disables true removing the user space allocation
       warning. If false, and warning value is a positive number, then set.
    type: bool
  size:
    description:
      - Specifies the size of the volume. Required with action present, grow,
       grow_to_size
  size_unit:
    choices:
      - MiB
      - GiB
      - TiB
    default: MiB
    description:
      - Specifies the unit of the volume size. Required with action present,
       grow, grow_to_size.
  snap_cpg:
    description:
      - Specifies the name of the CPG from which the snapshot space will be
       allocated. Required with action change_snap_cpg.
  ss_spc_alloc_limit_pct:
    default: 0
    description:
      - Prevents the snapshot space of  the virtual volume from growing beyond
       the indicated percentage of the virtual volume size.
  ss_spc_alloc_warning_pct:
    default: 0
    description:
      - Generates a warning alert when the reserved snapshot space of the
       virtual volume exceeds the indicated percentage of the virtual volume
       size.
  state:
    choices:
      - present
      - absent
      - modify
      - grow
      - grow_to_size
      - change_snap_cpg
      - change_user_cpg
      - convert_type
      - set_snap_cpg
    description:
      - Whether the specified Volume should exist or not. State also provides
       actions to modify volume properties.
    required: true
  type:
    choices:
      - thin
      - thin_dedupe
      - full
    default: thin
    description:
      - Specifies the type of the volume. Required with action convert_type"
  usr_spc_alloc_limit_pct:
    default: 0
    description:
      - Prevents the user space of the TPVV from growing beyond the indicated
       percentage of the virtual volume size. After reaching this limit, any
       new writes to the virtual volume will fail.
  usr_spc_alloc_warning_pct:
    default: 0
    description:
      - Generates a warning alert when the user data space of the TPVV exceeds
       the specified percentage of the virtual volume size.
  volume_name:
    description:
      - Name of the Virtual Volume.
    required: true
  wait_for_task_to_end:
    default: false
    description:
      - Setting to true makes the resource to wait until a task asynchronous
       operation, for ex convert type ends.
    type: bool
extends_documentation_fragment: hpe3par
version_added: 2.7
'''

EXAMPLES = r'''
    - name: Create Volume sample_volume
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: present
        volume_name: sample_volume
        cpg: sample_cpg
        size: 1024
        snap_cpg: sample_cpg

    - name: Change provisioning type of Volume sample_volume to thin
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: convert_type
        volume_name: sample_volume
        type: thin
        cpg: sample_cpg
        wait_for_task_to_end: true

    - name: Set Snap CPG of Volume sample_volume to sample_cpg
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: set_snap_cpg
        volume_name: sample_volume
        snap_cpg: sample_cpg

    - name: Change snap CPG of Volume sample_volume to sample_cpg
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: change_snap_cpg
        volume_name: sample_volume
        snap_cpg: sample_cpg
        wait_for_task_to_end: false

    - name: Grow Volume sample_volume by 1 GiB
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: grow
        volume_name: sample_volume
        size: 1
        size_unit: GiB

    - name: Grow Volume sample_volume to 5 GiB
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: grow_to_size
        volume_name: sample_volume
        size: 5
        size_unit: GiB

    - name: Rename Volume sample_volume to renamed_volume
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: modify
        volume_name: sample_volume
        new_name: renamed_volume

    - name: Delete Volume sample_volume
      hpe3par_volume:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: absent
        volume_name: sample_volume
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
APP_TYPE = "ansible-3par-client"


def convert_to_binary_multiple(size, size_unit):
    if size_unit == 'GiB':
        suffix = 'G'
    if size_unit == 'MiB':
        suffix = 'M'
    if size_unit == 'TiB':
        suffix = 'T'

    size_kib = basic.human_to_bytes(str(size) + suffix)
    return int(size_kib / (1024 * 1024))


def get_volume_type(volume_type):
    enum_type = ''
    if volume_type == 'thin':
        enum_type = ['TPVV', 1]
    elif volume_type == 'thin_dedupe':
        enum_type = ['TDVV', 3]
    elif volume_type == 'full':
        enum_type = ['FPVV', 2]
    return enum_type


def create_volume(
        client_obj,
        volume_name,
        cpg,
        size,
        size_unit,
        type,
        compression,
        snap_cpg):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    if cpg is None:
        return (False, False, "Volume creation failed. Cpg is null")
    if size is None:
        return (
            False,
            False,
            "Volume creation failed. Volume size is null")
    if size_unit is None:
        return (
            False,
            False,
            "Volume creation failed. Volume size_unit is null")
    try:
        if not client_obj.volumeExists(volume_name):
            tpvv = False
            tdvv = False
            if type == 'thin':
                tpvv = True
            elif type == 'thin_dedupe':
                tdvv = True
            size_in_mib = convert_to_binary_multiple(
                size, size_unit)
            optional = {'tpvv': tpvv, 'tdvv': tdvv, 'snapCPG': snap_cpg,
                        'compression': compression,
                        'objectKeyValues': [
                            {'key': 'type', 'value': 'ansible-3par-client'}]}
            client_obj.createVolume(volume_name, cpg, size_in_mib, optional)
        else:
            return (True, False, "Volume already present")
    except exceptions.ClientException as e:
        return (False, False, "Volume creation failed | %s" % e)
    return (True, True, "Created volume %s successfully." % volume_name)


def delete_volume(
        client_obj,
        volume_name):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    try:
        if client_obj.volumeExists(volume_name):
            client_obj.deleteVolume(volume_name)
        else:
            return (True, False, "Volume does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Volume delete failed | %s" % e)
    return (True, True, "Deleted volume %s successfully." % volume_name)


def grow(
        client_obj,
        volume_name,
        size,
        size_unit):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    if size is None:
        return (False, False, "Grow volume failed. Volume size is null")
    if size_unit is None:
        return (
            False,
            False,
            "Grow volume failed. Volume size_unit is null")
    try:
        size_mib = convert_to_binary_multiple(size, size_unit)
        client_obj.growVolume(volume_name, size_mib)
    except exceptions.ClientException as e:
        return (False, False, "Grow volume failed | %s" % e)
    return (
        True, True, "Grown volume %s by %s %s successfully." %
        (volume_name, size, size_unit))


def grow_to_size(
        client_obj,
        volume_name,
        size,
        size_unit):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    if size is None:
        return (
            False,
            False,
            "Grow_to_size volume failed. Volume size is null")
    if size_unit is None:
        return (
            False,
            False,
            "Grow_to_size volume failed. Volume size_unit is null")
    try:
        if client_obj.volumeExists(
                volume_name):
            if client_obj.getVolume(
                    volume_name).size_mib < convert_to_binary_multiple(
                    size, size_unit):
                client_obj.growVolume(volume_name, convert_to_binary_multiple(
                    size, size_unit) - client_obj.getVolume(
                    volume_name).size_mib)
            else:
                return (
                    True,
                    False,
                    "Volume size already >= %s %s" % (size, size_unit))
        else:
            return (
                False,
                False,
                "Volume does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Volume Grow To Size failed | %s" % e)
    return (
        True, True, "Grown volume %s to %s %s successfully." %
        (volume_name, size, size_unit))


def change_snap_cpg(
        client_obj,
        volume_name,
        snap_cpg,
        wait_for_task_to_end):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    if snap_cpg is None:
        return (False, False, "Change snap CPG failed. Snap CPG is null")
    try:
        if client_obj.volumeExists(volume_name):
            if client_obj.getVolume(volume_name).snap_cpg != snap_cpg:
                snp_cpg = 2
                task = client_obj.tuneVolume(
                    volume_name, snp_cpg, {
                        'snapCPG': snap_cpg})
                if wait_for_task_to_end:
                    client_obj.waitForTaskToEnd(task.task_id)
            else:
                return (True, False, "Snap CPG already set to %s" % snap_cpg)
        else:
            return (False, False, "Volume does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Change snap CPG failed | %s" % e)
    return (True, True, "Changed snap CPG to %s successfully." % snap_cpg)


def change_user_cpg(
        client_obj,
        volume_name,
        cpg,
        wait_for_task_to_end):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    if cpg is None:
        return (False, False, "Change user CPG failed. Snap CPG is null")
    try:
        if client_obj.volumeExists(volume_name):
            if client_obj.getVolume(volume_name).user_cpg != cpg:
                usr_cpg = 1
                task = client_obj.tuneVolume(
                    volume_name, usr_cpg, {'userCPG': cpg})
                if wait_for_task_to_end:
                    client_obj.waitForTaskToEnd(task.task_id)
            else:
                return (True, False, "user CPG already set to %s" % cpg)
        else:
            return (False, False, "Volume does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Change user CPG failed | %s" % e)
    return (True, True, "Changed user CPG to %s successfully." % cpg)


def convert_type(
        client_obj,
        volume_name,
        cpg,
        type,
        wait_for_task_to_end,
        keep_vv,
        compression):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    if cpg is None:
        return (
            False,
            False,
            "Convert volume type failed. User CPG is null")
    if type is None:
        return (
            False,
            False,
            "Convert volume type failed. Volume type is null")
    try:
        provisioning_type = client_obj.getVolume(volume_name).provisioning_type
        if provisioning_type == 1:
            volume_type = 'FPVV'
        elif provisioning_type == 2:
            volume_type = 'TPVV'
        elif provisioning_type == 6:
            volume_type = 'TDVV'
        else:
            volume_type = 'UNKNOWN'

        if client_obj.volumeExists(volume_name):
            if (volume_type != get_volume_type(type)[0] or
                    volume_type == 'UNKNOWN'):
                new_vol_type = get_volume_type(type)[1]
                usr_cpg = 1
                optional = {'userCPG': cpg,
                            'conversionOperation': new_vol_type,
                            'keepVV': keep_vv
                            }

                task = client_obj.tuneVolume(volume_name,
                                             usr_cpg,
                                             optional)
                if wait_for_task_to_end:
                    client_obj.waitForTaskToEnd(task.task_id)
            else:
                return (
                    True,
                    False,
                    "Provisioning type already set to %s" %
                    type)
        else:
            return (
                False,
                False,
                "Volume does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Provisioning type change failed | %s" % e)
    return (
        True,
        True,
        "Provisioning type changed to %s successfully." %
        type
    )


def modify_volume(
        client_obj,
        volume_name,
        new_name,
        expiration_hours,
        retention_hours,
        ss_spc_alloc_warning_pct,
        ss_spc_alloc_limit_pct,
        usr_spc_alloc_warning_pct,
        usr_spc_alloc_limit_pct,
        rm_ss_spc_alloc_warning,
        rm_usr_spc_alloc_warning,
        rm_exp_time,
        rm_usr_spc_alloc_limit,
        rm_ss_spc_alloc_limit,
        user_cpg,
        snap_cpg):
    if len(volume_name) < 1 or len(volume_name) > 31:
        return (False, False, "Volume create failed. Volume name must be atleast 1 character and not more than 31 characters")
    try:
        volume_mods = {
            'expirationHours': expiration_hours,
            'newName': new_name,
            'retentionHours': retention_hours,
            'ssSpcAllocWarningPct': ss_spc_alloc_warning_pct,
            'ssSpcAllocLimitPct': ss_spc_alloc_limit_pct,
            'usrSpcAllocWarningPct': usr_spc_alloc_warning_pct,
            'usrSpcAllocLimitPct': usr_spc_alloc_limit_pct,
            'rmSsSpcAllocWarning': rm_ss_spc_alloc_warning,
            'rmUsrSpcAllocWarning': rm_usr_spc_alloc_warning,
            'rmExpTime': rm_exp_time,
            'rmSsSpcAllocLimit': rm_ss_spc_alloc_limit,
            'rmUsrSpcAllocLimit': rm_usr_spc_alloc_limit,
            'userCPG': user_cpg,
            'snapCPG': snap_cpg}
        client_obj.modifyVolume(volume_name, volume_mods, APP_TYPE)
    except exceptions.ClientException as e:
        return (False, False, "Modify Volume failed | %s" % e)
    return (True, True, "Modified Volume %s successfully." % volume_name)


def main():
    module = AnsibleModule(argument_spec=hpe3par.volume_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(
            msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]

    volume_name = module.params["volume_name"]
    size = module.params["size"]
    size_unit = module.params["size_unit"]
    cpg = module.params["cpg"]
    compression = module.params["compression"]
    snap_cpg = module.params["snap_cpg"]
    wait_for_task_to_end = module.params["wait_for_task_to_end"]

    new_name = module.params["new_name"]
    expiration_hours = module.params["expiration_hours"]
    retention_hours = module.params["retention_hours"]
    ss_spc_alloc_warning_pct = module.params["ss_spc_alloc_warning_pct"]
    ss_spc_alloc_limit_pct = module.params["ss_spc_alloc_limit_pct"]
    usr_spc_alloc_warning_pct = module.params["usr_spc_alloc_warning_pct"]
    usr_spc_alloc_limit_pct = module.params["usr_spc_alloc_limit_pct"]
    rm_ss_spc_alloc_warning = module.params["rm_ss_spc_alloc_warning"]
    rm_usr_spc_alloc_warning = module.params["rm_usr_spc_alloc_warning"]
    rm_exp_time = module.params["rm_exp_time"]
    rm_usr_spc_alloc_limit = module.params["rm_usr_spc_alloc_limit"]
    rm_ss_spc_alloc_limit = module.params["rm_ss_spc_alloc_limit"]
    compression = module.params["compression"]
    keep_vv = module.params["keep_vv"]
    type = module.params["type"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    # States
    if module.params["state"] == "present":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = create_volume(
                client_obj,
                volume_name, cpg, size, size_unit, type, compression, snap_cpg)
        except Exception as e:
            module.fail_json(msg="Volume create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = delete_volume(
                client_obj,
                volume_name)
        except Exception as e:
            module.fail_json(msg="Volume delete failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "grow":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = grow(
                client_obj,
                volume_name, size, size_unit)
        except Exception as e:
            module.fail_json(msg="Volume grow failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "grow_to_size":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = grow_to_size(
                client_obj,
                volume_name, size, size_unit)
        except Exception as e:
            module.fail_json(msg="Volume grow to size failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "change_snap_cpg":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = change_snap_cpg(
                client_obj,
                volume_name, snap_cpg, wait_for_task_to_end)
        except Exception as e:
            module.fail_json(msg="Volume change snap CPG failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "change_user_cpg":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = change_user_cpg(
                client_obj,
                volume_name, cpg, wait_for_task_to_end)
        except Exception as e:
            module.fail_json(msg="Volume change user CPG failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "convert_type":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = convert_type(
                client_obj,
                volume_name, cpg, type, wait_for_task_to_end, keep_vv, compression)
        except Exception as e:
            module.fail_json(msg="Volume convert type failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "modify":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                modify_volume(client_obj, volume_name,
                              new_name, expiration_hours, retention_hours,
                              ss_spc_alloc_warning_pct, ss_spc_alloc_limit_pct,
                              usr_spc_alloc_warning_pct, usr_spc_alloc_limit_pct,
                              rm_ss_spc_alloc_warning, rm_usr_spc_alloc_warning,
                              rm_exp_time, rm_usr_spc_alloc_limit,
                              rm_ss_spc_alloc_limit, None, None))
        except Exception as e:
            module.fail_json(msg="Volume modify failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "set_snap_cpg":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = modify_volume(
                client_obj,
                volume_name, None, None, None, None, None, None, None, None, None,
                None, None, None, None, snap_cpg)
        except Exception as e:
            module.fail_json(msg="Volume modify failed | %s" % e)
        finally:
            client_obj.logout()

    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
