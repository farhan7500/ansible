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
short_description: Manage HPE 3PAR VLUN
author:
  - Farhan Nomani (@farhan7500)
  - Gautham P Hegde (@gautamphegde)
description: On HPE 3PAR - Export volume to host. - Export volumeset to host.
 - Export volume to hostset. - Export volumeset to hostset. - Unexport volume
 from host. - Unexport volumeset from host. - Unexport volume from hostset. -
 Unexport volumeset from hostset.
module: hpe3par_vlun
options:
  autolun:
    default: false
    description:
      - States whether the lun number should be autosigned.
    type: bool
  card_port:
    description:
      - Port number on the FC card.
  host_name:
    description:
      - Name of the host to which the volume or VV set is to be exported.
  host_set_name:
    description:
      - Name of the host set to which the volume or VV set is to be exported.
       Required with action export_volume_to_hostset,
       unexport_volume_from_hostset, export_volumeset_to_hostset,
       unexport_volumeset_from_hostset
  lunid:
    description:
      - LUN ID.
  node_val:
    description:
      - System node.
  slot:
    description:
      - PCI bus slot in the node.
  state:
    choices:
      - export_volume_to_host
      - unexport_volume_from_host
      - export_volumeset_to_host
      - unexport_volumeset_from_host
      - export_volume_to_hostset
      - unexport_volume_from_hostset
      - export_volumeset_to_hostset
      - unexport_volumeset_from_hostset
    description:
      - Whether the specified export should exist or not.
    required: true
  volume_name:
    description:
      - Name of the volume to export.
    required: true
  volume_set_name:
    description:
      - Name of the VV set to export.\nRequired with action
       export_volumeset_to_host, unexport_volumeset_from_host,
       export_volumeset_to_hostset, unexport_volumeset_from_hostset.
extends_documentation_fragment: hpe3par
version_added: 2.6
'''

EXAMPLES = r'''
    - name: Create VLUN
      hpe3par_vlun:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: export_volume_to_host
        volume_name: sample_volume
        host_name: sample_host
        lunid: 110
        autolun: false

    - name: Create VLUN
      hpe3par_vlun:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: export_volume_to_hostset
        volume_name: sample_volume
        host_set_name: sample_hostset
        lunid: 110
        autolun: false

    - name: Create VLUN
      hpe3par_vlun:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: export_volumeset_to_host
        volume_set_name: sample_volumeset
        host_name: sample_host
        lunid: 110
        autolun: false

    - name: Create VLUN
      hpe3par_vlun:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: export_volumeset_to_hostset
        volume_set_name: sample_volumeset
        host_set_name: sample_hostset
        lunid: 110
        autolun: false

    - name: Delete VLUN
      hpe3par_vlun:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: unexport_volume_from_host
        volume_name: sample_volume
        lunid: 110
        autolun: false
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


def export_volume_to_host(
        client_obj,
        volume_name,
        lunid,
        host_name,
        node_val,
        slot,
        card_port,
        autolun):
    try:
        if (host_name is None and node_val is None and slot is None and
                card_port is None):
            return (
                False,
                False,
                'Attribute host_name or port positions or both need to be \
specified to create a vlun')

        if host_name is None and (
                node_val is None or slot is None or card_port is None):
            return (
                False,
                False,
                'Node, Slot and Port need to be specified to create a vlun')

        port_pos = None

        if node_val is not None and slot is not None and card_port is not None:
            port_pos = {'node': node_val, 'slot': slot, 'cardPort': card_port}

        if autolun:
            client_obj.createVLUN(
                volume_name,
                lunid,
                host_name,
                port_pos,
                None,
                None,
                autolun)
        else:
            if lunid:
                if not client_obj.vlunExists(
                        volume_name, lunid, host_name, port_pos):
                    client_obj.createVLUN(
                        volume_name,
                        lunid,
                        host_name,
                        port_pos,
                        None,
                        None,
                        autolun)
                else:
                    return (True, False, "VLUN already present")
            else:
                return (False, False, "Lun ID is required")
    except exceptions.ClientException as e:
        return (False, False, "VLUN creation failed | %s" % e)
    return (True, True, "Created VLUN successfully.")


def unexport_volume_from_host(
        client_obj,
        volume_name,
        lunid,
        host_name,
        node_val,
        slot,
        card_port):
    try:
        port_pos = None

        if volume_name is not None and volume_name:
            if (host_name is not None and host_name) or (node_val is not None and slot is not None and card_port is not None):
                if (node_val is not None and slot is not None and card_port is not None):
                    port_pos = {
                        'node': node_val,
                        'slot': slot,
                        'cardPort': card_port
                    }
                if lunid is not None:
                    if client_obj.vlunExists(volume_name, lunid, host_name, port_pos):
                        client_obj.deleteVLUN(
                            volume_name, lunid, host_name, port_pos)
                    else:
                        return (False, False, "VLUN does not exist")
                else:
                    return (False, False, "Lun ID is required")
            else:
                return (False, False, 'Node, Slot and Port or host name need to be specified to unexport a vlun')
        else:
            return (False, False, "Volume name is required")
    except exceptions.ClientException as e:
        return (False, False, "VLUN deletion failed | %s" % e)
    return (True, True, "Deleted VLUN successfully.")


def export_volume_to_hostset(
        client_obj,
        volume_name,
        lunid,
        host_set_name,
        node_val,
        slot,
        card_port,
        autolun):
    try:
        if volume_name is None:
            return (
                False,
                False,
                'Attribute volume name is required for vlun creation')

        if host_set_name is None:
            return (
                False,
                False,
                'Attribute hostset_name is required to export a vlun')
        else:
            host_set_name = 'set:' + host_set_name

        port_pos = None

        if node_val is not None and slot is not None and card_port is not None:
            port_pos = {'node': node_val, 'slot': slot, 'cardPort': card_port}

        if autolun:
            client_obj.createVLUN(
                volume_name,
                lunid,
                host_set_name,
                port_pos,
                None,
                None,
                autolun)
        else:
            if lunid:
                if not client_obj.vlunExists(
                        volume_name, lunid, host_set_name, port_pos):
                    client_obj.createVLUN(
                        volume_name,
                        lunid,
                        host_set_name,
                        port_pos,
                        None,
                        None,
                        autolun)
                else:
                    return (True, False, "VLUN already present")
            else:
                return (False, False, "Lun ID is required")

    except exceptions.ClientException as e:
        return (False, False, "VLUN creation failed | %s" % e)
    return (True, True, "Created VLUN successfully.")


def unexport_volume_from_hostset(
        client_obj,
        volume_name,
        lunid,
        host_set_name,
        node_val,
        slot,
        card_port):
    try:
        if host_set_name is None and (
                node_val is None or slot is None or card_port is None):
            return (
                False,
                False,
                'Node, Slot and Port or host name need to be specified to \
unexport a vlun')

        if host_set_name is None:
            return (
                False,
                False,
                'Attribute hostset_name is required to unexport a vlun')
        else:
            host_set_name = 'set:' + host_set_name

        port_pos = None
        if lunid is not None:
            if client_obj.vlunExists(volume_name, lunid, host_set_name, port_pos):
                client_obj.deleteVLUN(volume_name, lunid,
                                      host_set_name, port_pos)
            else:
                return (False, False, "VLUN does not exist")
        else:
            return (False, False, "Lun ID is required")
    except exceptions.ClientException as e:
        return (False, False, "VLUN deletion failed | %s" % e)
    return (True, True, "Deleted VLUN successfully.")


def export_volumeset_to_host(
        client_obj,
        volume_set_name,
        lunid,
        host_name,
        node_val,
        slot,
        card_port,
        autolun):
    try:
        if volume_set_name is None:
            return (
                False,
                False,
                'Attribute volumeset name is required for vlun creation')

        if (host_name is None and node_val is None and slot is None and
                card_port is None):
            return (
                False,
                False,
                'Attribute host_name or port positions or both need to be \
specified to create a vlun')

        if host_name is None and (
                node_val is None or slot is None or card_port is None):
            return (
                False,
                False,
                'All port positions (node,slot,cardport) are required to \
create a vlun')

        if volume_set_name:
            volume_set_name = 'set:' + volume_set_name

        port_pos = None

        if node_val is not None and slot is not None and card_port is not None:
            port_pos = {'node': node_val, 'slot': slot, 'cardPort': card_port}

        if autolun:
            client_obj.createVLUN(
                volume_set_name,
                lunid,
                host_name,
                port_pos,
                None,
                None,
                autolun)
        else:
            if lunid:
                if not client_obj.vlunExists(
                        volume_set_name, lunid, host_name, port_pos):
                    client_obj.createVLUN(
                        volume_set_name,
                        lunid,
                        host_name,
                        port_pos,
                        None,
                        None,
                        autolun)
                else:
                    return (True, False, "VLUN already present")
            else:
                return (False, False, "Lun ID is required")
    except exceptions.ClientException as e:
        return (False, False, "VLUN creation failed | %s" % e)
    return (True, True, "Created VLUN successfully.")


def unexport_volumeset_from_host(
        client_obj,
        volume_set_name,
        lunid,
        host_name,
        node_val,
        slot,
        card_port):
    try:
        if host_name is None and (
                node_val is None or slot is None or card_port is None):
            return (
                False,
                False,
                'Node, Slot and Port or host name need to be specified to \
unexport a vlun')

        if volume_set_name is None:
            return (
                False,
                False,
                'Attribute volume_set_name is required to unexport a vlun')
        else:
            volume_set_name = 'set:' + volume_set_name

        port_pos = None
        if node_val is not None and slot is not None and card_port is not None:
            port_pos = {'node': node_val, 'slot': slot, 'cardPort': card_port}
        if lunid is not None:
            if client_obj.vlunExists(volume_set_name, lunid, host_name, port_pos):
                client_obj.deleteVLUN(
                    volume_set_name, lunid, host_name, port_pos)
            else:
                return (True, False, "VLUN does not exist")
        else:
            return (False, False, "Lun ID is required")
    except exceptions.ClientException as e:
        return (False, False, "VLUN deletion failed | %s" % e)
    return (True, True, "Deleted VLUN successfully.")


def export_volumeset_to_hostset(
        client_obj,
        volume_set_name,
        lunid,
        host_set_name,
        node_val,
        slot,
        card_port,
        autolun):
    try:
        if volume_set_name is None:
            return (
                False,
                False,
                'Attribute volumeset name is required for vlun creation')

        if host_set_name is None:
            return (
                False,
                False,
                'Attribute hostset name is required for vlun creation')

        if volume_set_name is not None and host_set_name is not None:
            volume_set_name = 'set:' + volume_set_name
            host_set_name = 'set:' + host_set_name
        else:
            return (
                False,
                False,
                'Attribute hostset_name and volumeset_name is required to \
export a vlun')

        port_pos = None

        if node_val is not None and slot is not None and card_port is not None:
            port_pos = {'node': node_val, 'slot': slot, 'cardPort': card_port}

        if autolun:
            client_obj.createVLUN(
                volume_set_name,
                lunid,
                host_set_name,
                port_pos,
                None,
                None,
                autolun)
        else:
            if lunid:
                if not client_obj.vlunExists(
                        volume_set_name, lunid, host_set_name, port_pos):
                    client_obj.createVLUN(
                        volume_set_name,
                        lunid,
                        host_set_name,
                        port_pos,
                        None,
                        None,
                        autolun)
                else:
                    return (True, False, "VLUN already present")
            else:
                return (False, False, "Lun ID is required")
    except exceptions.ClientException as e:
        return (False, False, "VLUN creation failed | %s" % e)
    return (True, True, "Created VLUN successfully.")


def unexport_volumeset_from_hostset(
        client_obj,
        volume_set_name,
        lunid,
        host_set_name,
        node_val,
        slot,
        card_port):
    try:
        if host_set_name is None and (
                node_val is None or slot is None or card_port is None):
            return (
                False,
                False,
                'Node, Slot and Port or host set name need to be specified to \
unexport a vlun')

        if volume_set_name is not None and host_set_name is not None:
            volume_set_name = 'set:' + volume_set_name
            host_set_name = 'set:' + host_set_name
        else:
            return (
                False,
                False,
                'Attribute hostset_name and volumeset_name is required to \
unexport a vlun')

        port_pos = None

        if lunid is not None:
            if client_obj.vlunExists(
                    volume_set_name,
                    lunid,
                    host_set_name,
                    port_pos):
                client_obj.deleteVLUN(
                    volume_set_name, lunid, host_set_name, port_pos)
            else:
                return (True, False, "VLUN does not exist")
        else:
            return (False, False, "Lun ID is required")
    except exceptions.ClientException as e:
        return (False, False, "VLUN deletion failed | %s" % e)
    return (True, True, "Deleted VLUN successfully.")


def main():
    module = AnsibleModule(argument_spec=hpe3par.vlun_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(
            msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]

    volume_name = module.params["volume_name"]
    volume_set_name = module.params["volume_set_name"]
    lunid = module.params["lunid"]
    host_name = module.params["host_name"]
    host_set_name = module.params["host_set_name"]
    node_val = module.params["node_val"]
    slot = module.params["slot"]
    card_port = module.params["card_port"]
    autolun = module.params["autolun"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    # States
    if module.params["state"] == "export_volume_to_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = export_volume_to_host(
                client_obj,
                volume_name, lunid, host_name, node_val, slot, card_port, autolun)
        except Exception as e:
            module.fail_json(msg="VLUN create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "unexport_volume_from_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = unexport_volume_from_host(
                client_obj,
                volume_name, lunid, host_name, node_val, slot, card_port)
        except Exception as e:
            module.fail_json(msg="VLUN delete failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "export_volumeset_to_hostset":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                export_volumeset_to_hostset(client_obj,
                                            volume_set_name, lunid, host_set_name,
                                            node_val, slot, card_port,
                                            autolun))
        except Exception as e:
            module.fail_json(msg="VLUN create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "unexport_volumeset_from_hostset":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                unexport_volumeset_from_hostset(client_obj,
                                                volume_set_name, lunid,
                                                host_set_name, node_val, slot,
                                                card_port))
        except Exception as e:
            module.fail_json(msg="VLUN delete failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "export_volumeset_to_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                export_volumeset_to_host(client_obj,
                                         volume_set_name, lunid, host_name,
                                         node_val, slot, card_port, autolun))
        except Exception as e:
            module.fail_json(msg="VLUN create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "unexport_volumeset_from_host":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                unexport_volumeset_from_host(client_obj,
                                             volume_set_name, lunid, host_name,
                                             node_val, slot, card_port))
        except Exception as e:
            module.fail_json(msg="VLUN delete failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "export_volume_to_hostset":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                export_volume_to_hostset(client_obj,
                                         volume_name, lunid, host_set_name,
                                         node_val, slot, card_port, autolun))
        except Exception as e:
            module.fail_json(msg="VLUN create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "unexport_volume_from_hostset":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = (
                unexport_volume_from_hostset(client_obj,
                                             volume_name, lunid, host_set_name,
                                             node_val, slot, card_port))
        except Exception as e:
            module.fail_json(msg="VLUN delete failed | %s" % e)
        finally:
            client_obj.logout()

    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
