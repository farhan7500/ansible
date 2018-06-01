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
short_description: Manage HPE 3PAR Host
author:
  - Farhan Nomani (@farhan7500)
  - Gautham P Hegde (@gautamphegde)
description: On HPE 3PAR - Create Host. - Delete Host. - Add Initiator Chap.
 - Remove Initiator Chap. - Add Target Chap. - Remove Target Chap.
 - Add FC Path to Host - Remove FC Path from Host - Add ISCSI Path to Host
 - Remove ISCSI Path from Host
module: hpe3par_host
options:
  chap_name:
    description:
      - The chap name. Required with actions add_initiator_chap,
       add_target_chap
  chap_secret:
    description:
      - The chap secret for the host or the target. Required with actions
       add_initiator_chap, add_target_chap"
  chap_secret_hex:
    description:
      - If true, then chapSecret is treated as Hex.
    type: bool
  force_path_removal:
    description:
      - If true, remove WWN(s) or iSCSI(s) even if there are VLUNs that are
       exported to the host.
    type: bool
  host_domain:
    description:
      - Create the host in the specified domain, or in the default domain,
       if unspecified
  host_fc_wwns:
    description:
      - Set one or more WWNs for the host. Required with action
       add_fc_path_to_host, remove_fc_path_from_host.
  host_iscsi_names:
    description:
      - Set one or more iSCSI names for the host. Required with action
       add_iscsi_path_to_host, remove_iscsi_path_from_host.
  host_name:
    description:
      - Name of the Host.
    required: true
  host_new_name:
    description:
      - New name of the Host.
    required: true
  host_persona:
    choices:
      - GENERIC
      - GENERIC_ALUA
      - GENERIC_LEGACY
      - HPUX_LEGACY
      - AIX_LEGACY
      - EGENERA
      - ONTAP_LEGACY
      - VMWARE
      - OPENVMS
      - HPUX
      - WINDOWS_SERVER
    description:
      - ID of the persona to assign to the host. Uses the default persona
       unless you specify the host persona.
  state:
    choices:
      - present
      - absent
      - modify
      - add_initiator_chap
      - remove_initiator_chap
      - add_target_chap
      - remove_target_chap
      - add_fc_path_to_host
      - remove_fc_path_from_host
      - add_iscsi_path_to_host
      - remove_iscsi_path_from_host
    description:
      - Whether the specified Host should exist or not. State also provides
       actions to add and remove initiator and target chap, add fc/iscsi path
       to host.
    required: true
extends_documentation_fragment: hpe3par
version_added: "2.6"
'''

EXAMPLES = r'''
    - name: Create Host sample_host
      hpe3par_host:
        storage_system_ip: 10.10.10.1
        storage_system_username: username
        storage_system_password: password
        state: present
        host_name: sample_host

    - name: Modify Host sample_host
      hpe3par_host:
        storage_system_ip: 10.10.10.1
        storage_system_username: username
        storage_system_password: password
        state: modify
        host_name: sample_host
        host_new_name: renamed_host

    - name: Delete Host sample_host
      hpe3par_host:
        storage_system_ip: 10.10.10.1
        storage_system_username: username
        storage_system_password: password
        state: absent
        host_name: sample_host
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


def create_host(
        client_obj,
        host_name,
        host_iscsi_names,
        host_fc_wwns,
        host_domain,
        host_persona):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    try:
        if not client_obj.hostExists(host_name):
            optional = dict()
            if host_domain is not None:
                optional['domain'] = host_domain

            if host_persona is not None:
                optional['persona'] = getattr(
                    client.HPE3ParClient, host_persona)

            client_obj.createHost(
                host_name,
                host_iscsi_names,
                host_fc_wwns,
                optional)
        else:
            return (True, False, "Host already present")
    except exceptions.ClientException as e:
        return (False, False, "Host creation failed | %s" % e)
    return (True, True, "Created host %s successfully." % host_name)


def modify_host(
        client_obj,
        host_name,
        host_new_name,
        host_persona):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    try:
        if host_persona is not None:
            host_persona = getattr(
                client.HPE3ParClient, host_persona)

        client_obj.modifyHost(
            host_name, {
                "newName": host_new_name, "persona": host_persona})
    except exceptions.ClientException as e:
        return (False, False, "Host modification failed | %s" % e)
    return (True, True, "Modified host %s successfully." % host_name)


def delete_host(
        client_obj,
        host_name):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    try:
        if client_obj.hostExists(host_name):
            client_obj.deleteHost(host_name)
        else:
            return (True, False, "Host does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Host deletion failed | %s" % e)
    return (True, True, "Deleted host %s successfully." % host_name)


def add_initiator_chap(
        client_obj,
        host_name,
        chap_name,
        chap_secret,
        chap_secret_hex):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    if chap_name is None:
        return (
            False,
            False,
            "Host modification failed. Chap name is null",
        )
    if chap_secret is None:
        return (
            False,
            False,
            "Host modification failed. chap_secret is null",
        )
    try:
        if chap_secret_hex and len(chap_secret) != 32:
            return (
                False,
                False,
                "Add initiator chap failed. Chap secret hex is false and chap \
secret less than 32 characters",
            )
        if not chap_secret_hex and (
                len(chap_secret) < 12 or len(chap_secret) > 16):
            return (
                False,
                False,
                "Add initiator chap failed. Chap secret hex is false and chap \
secret less than 12 characters or more than 16 characters",
            )
        client_obj.modifyHost(host_name,
                              {'chapOperationMode':
                               client.HPE3ParClient.CHAP_INITIATOR,
                               'chapOperation':
                               HPE3ParClient.HOST_EDIT_ADD,
                               'chapName': chap_name,
                               'chapSecret': chap_secret,
                               'chapSecretHex': chap_secret_hex})
    except exceptions.ClientException as e:
        return (False, False, "Add initiator chap failed | %s" % e)
    return (True, True, "Added initiator chap.")


def remove_initiator_chap(
        client_obj,
        host_name):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    try:
        client_obj.modifyHost(
            host_name, {
                'chapOperation': HPE3ParClient.HOST_EDIT_REMOVE})
    except exceptions.ClientException as e:
        return (False, False, "Remove initiator chap failed | %s" % e)
    return (True, True, "Removed initiator chap.")


def initiator_chap_exists(
        client_obj,
        host_name):
    try:
        return client_obj.getHost(host_name).initiator_chap_enabled
    except exceptions.ClientException as e:
        return e


def add_target_chap(
        client_obj,
        host_name,
        chap_name,
        chap_secret,
        chap_secret_hex):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    if chap_name is None:
        return (
            False,
            False,
            "Host modification failed. Chap name is null",
        )
    if chap_secret is None:
        return (
            False,
            False,
            "Host modification failed. chap_secret is null",
        )
    if chap_secret_hex and len(chap_secret) != 32:
        return (
            False,
            False,
            'Attribute chap_secret must be 32 hexadecimal characters if \
chap_secret_hex is true',
        )
    if not chap_secret_hex and (
            len(chap_secret) < 12 or len(chap_secret) > 16):
        return (
            False,
            False,
            'Attribute chap_secret must be 12 to 16 character if \
chap_secret_hex is false',
        )
    try:
        if initiator_chap_exists(
                client_obj,
                host_name):
            mod_request = {
                'chapOperationMode': client.HPE3ParClient.CHAP_TARGET,
                'chapOperation': HPE3ParClient.HOST_EDIT_ADD,
                'chapName': chap_name,
                'chapSecret': chap_secret,
                'chapSecretHex': chap_secret_hex}
            client_obj.modifyHost(host_name, mod_request)
        else:
            return (True, False, "Initiator chap does not exist")
    except exceptions.ClientException as e:
        return (False, False, "Add target chap failed | %s" % e)
    return (True, True, "Added target chap.")


def remove_target_chap(
        client_obj,
        host_name):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    try:
        mod_request = {
            'chapOperation': HPE3ParClient.HOST_EDIT_REMOVE,
            'chapRemoveTargetOnly': True}
        client_obj.modifyHost(host_name, mod_request)
    except exceptions.ClientException as e:
        return (False, False, "Remove target chap failed | %s" % e)
    finally:
        client_obj.logout()
    return (True, True, "Removed target chap.")


def add_fc_path_to_host(
        client_obj,
        host_name,
        host_fc_wwns):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    if host_fc_wwns is None:
        return (
            False,
            False,
            "Host modification failed. host_fc_wwns is null",
        )
    try:
        mod_request = {
            'pathOperation': HPE3ParClient.HOST_EDIT_ADD,
            'FCWWNs': host_fc_wwns}
        client_obj.modifyHost(host_name, mod_request)
    except exceptions.ClientException as e:
        return (False, False, "Add FC path to host failed | %s" % e)
    return (True, True, "Added FC path to host successfully.")


def remove_fc_path_from_host(
        client_obj,
        host_name,
        host_fc_wwns,
        force_path_removal):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    if host_fc_wwns is None:
        return (
            False,
            False,
            "Host modification failed. host_fc_wwns is null",
        )
    try:
        mod_request = {
            'pathOperation': HPE3ParClient.HOST_EDIT_REMOVE,
            'FCWWNs': host_fc_wwns,
            'forcePathRemoval': force_path_removal}
        client_obj.modifyHost(host_name, mod_request)
    except exceptions.ClientException as e:
        return (False, False, "Remove FC path from host failed | %s" % e)
    return (True, True, "Removed FC path from host successfully.")


def add_iscsi_path_to_host(
        client_obj,
        host_name,
        host_iscsi_names):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    if host_iscsi_names is None:
        return (
            False,
            False,
            "Host modification failed. host_iscsi_names is null",
        )
    try:
        mod_request = {
            'pathOperation': HPE3ParClient.HOST_EDIT_ADD,
            'iSCSINames': host_iscsi_names}
        client_obj.modifyHost(host_name, mod_request)
    except exceptions.ClientException as e:
        return (False, False, "Add ISCSI path to host failed | %s" % e)
    return (True, True, "Added ISCSI path to host successfully.")


def remove_iscsi_path_from_host(
        client_obj,
        host_name,
        host_iscsi_names,
        force_path_removal):
    if len(host_name) < 1 or len(host_name) > 31:
        return (False, False, "Host create failed. Host name must be atleast 1 character and not more than 31 characters")
    if host_iscsi_names is None:
        return (
            False,
            False,
            "Host modification failed. host_iscsi_names is null",
        )
    try:
        mod_request = {
            'pathOperation': HPE3ParClient.HOST_EDIT_REMOVE,
            'iSCSINames': host_iscsi_names,
            'forcePathRemoval': force_path_removal}
        client_obj.modifyHost(host_name, mod_request)
    except exceptions.ClientException as e:
        return (
            False,
            False,
            "Remove ISCSI path from host failed | %s" %
            e,
        )
    return (True, True, "Removed ISCSI path from host successfully.")


def main():

    module = AnsibleModule(argument_spec=hpe3par.host_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(
            msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]

    host_name = module.params["host_name"]
    host_new_name = module.params["host_new_name"]
    host_domain = module.params["host_domain"]
    host_fc_wwns = module.params["host_fc_wwns"]
    host_iscsi_names = module.params["host_iscsi_names"]
    host_persona = module.params["host_persona"]
    chap_name = module.params["chap_name"]
    chap_secret = module.params["chap_secret"]
    chap_secret_hex = module.params["chap_secret_hex"]
    force_path_removal = module.params["force_path_removal"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    # States
    if module.params["state"] == "present":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = create_host(
                client_obj, host_name, host_iscsi_names, host_fc_wwns, host_domain,
                host_persona)
        except Exception as e:
            module.fail_json(msg="Host create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "modify":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = modify_host(
                client_obj, host_name, host_new_name, host_persona)
        except Exception as e:
            module.fail_json(msg="Host modify failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = delete_host(
                client_obj, host_name)
        except Exception as e:
            module.fail_json(msg="Host delete failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "add_initiator_chap":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = add_initiator_chap(
                client_obj, host_name, chap_name, chap_secret, chap_secret_hex)
        except Exception as e:
            module.fail_json(msg="Host add initiator chap failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "remove_initiator_chap":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                remove_initiator_chap(client_obj, host_name))
        except Exception as e:
            module.fail_json(msg="Host remove initiator chap failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "add_target_chap":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = add_target_chap(
                client_obj, host_name, chap_name, chap_secret, chap_secret_hex)
        except Exception as e:
            module.fail_json(msg="Host add target chap failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "remove_target_chap":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = remove_target_chap(
                client_obj, host_name)
        except Exception as e:
            module.fail_json(msg="Host remove target chap failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "add_fc_path_to_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = add_fc_path_to_host(
                client_obj, host_name, host_fc_wwns)
        except Exception as e:
            module.fail_json(msg="Host add fc path to host failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "remove_fc_path_from_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                remove_fc_path_from_host(client_obj, host_name,
                                         host_fc_wwns, force_path_removal))
        except Exception as e:
            module.fail_json(
                msg="Host remove fc path from host failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "add_iscsi_path_to_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = add_iscsi_path_to_host(
                client_obj, host_name, host_iscsi_names)
        except Exception as e:
            module.fail_json(msg="Host add iscsi path to host failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "remove_iscsi_path_from_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                remove_iscsi_path_from_host(client_obj, host_name,
                                            host_iscsi_names, force_path_removal))
        except Exception as e:
            module.fail_json(msg="Host add iscsi path to host failed | %s" % e)
        finally:
            client_obj.logout()

    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
