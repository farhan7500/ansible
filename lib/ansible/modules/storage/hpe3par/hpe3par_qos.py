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
short_description: Manage HPE 3PAR QoS Rules
author:
  - Farhan Nomani (@farhan7500)
  - Gautham P Hegde (@gautamphegde)
description: On HPE 3PAR - Create QoS Rule. - Delete QoS Rule. - Modify QoS
 Rule.
module: hpe3par_qos
options:
  bwmax_limit_kb:
    default: -1
    description:
      - Bandwidth rate maximum limit in kilobytes per second.
  bwmax_limit_op:
    choices:
      - ZERO
      - NOLIMIT
    description:
      - When set to 1, the bandwidth maximum limit is 0. When set to 2, the
       bandwidth maximum limit is none (NoLimit).
  bwmin_goal_kb:
    default: -1
    description:
      - Bandwidth rate minimum goal in kilobytes per second.
  bwmin_goal_op:
    choices:
      - ZERO
      - NOLIMIT
    description:
      - When set to 1, the bandwidth minimum goal is 0. When set to 2, the
       bandwidth minimum goal is none (NoLimit).
  default_latency:
    default: false
    description:
      - If true, set latencyGoal to the default value. If false and the
       latencyGoal value is positive, then set the value. Default is false.
    type: bool
  enable:
    default: false
    description:
      - If true, enable the QoS rule for the target object. If false, disable
       the QoS rule for the target object.
    type: bool
  iomax_limit:
    default: -1
    description:
      - I/O-per-second maximum limit.
  iomax_limit_op:
    choices:
      - ZERO
      - NOLIMIT
    description:
      - When set to 1, the I/O maximum limit is 0. When set to 2, the I/O
       maximum limit is none (NoLimit).
  iomin_goal:
    default: -1
    description:
      - I/O-per-second minimum goal.
  iomin_goal_op:
    choices:
      - ZERO
      - NOLIMIT
    description:
      - When set to 1, the I/O minimum goal is 0. When set to 2, the I/O
       minimum goal is none (NoLimit).
  latency_goal:
    description:
      - Latency goal in milliseconds. Do not use with latencyGoaluSecs.
  latency_goal_usecs:
    description:
      - Latency goal in microseconds. Do not use with latencyGoal.
  priority:
    choices:
      - LOW
      - NORMAL
      - HIGH
    default: LOW
    description:
      - QoS priority.
  qos_target_name:
    description:
      - The name of the target object on which the new QoS rules will be
       created.
    required: true
  state:
    choices:
      - present
      - absent
      - modify
    description:
      - Whether the specified QoS Rule should exist or not. State also
       provides actions to modify QoS Rule.
    required: true
  type:
    choices:
      - vvset
      - sys
    description:
      - Type of QoS target.
extends_documentation_fragment: hpe3par
version_added: 2.7
'''

EXAMPLES = r'''
    - name: Create QoS
      hpe3par_qos:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: present
        qos_target_name: all_others
        priority: NORMAL
        bwmin_goal_kb: 200
        bwmax_limit_kb: 200
        iomin_goal_op: NOLIMIT
        default_latency: true
        enable: true
        bwmin_goal_op: NOLIMIT
        bwmax_limit_op: NOLIMIT
        latency_goal_usecs: 20
        type: sys
        iomax_limit_op: NOLIMIT

    - name: Modify QoS
      hpe3par_qos:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: modify
        qos_target_name: all_others
        priority: NORMAL
        bwmin_goal_kb: 200
        bwmax_limit_kb: 200
        iomin_goal_op: NOLIMIT
        default_latency: true
        enable: true
        bwmin_goal_op: NOLIMIT
        bwmax_limit_op: NOLIMIT
        latency_goal_usecs: 20
        type: sys
        iomax_limit_op: NOLIMIT

    - name: Delete QoS
      hpe3par_qos:
        storage_system_ip: 10.10.0.1
        storage_system_username: username
        storage_system_password: password
        state: absent
        qos_target_name: 'all_others'
        type: sys
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


def create_qos_rule(
        client_obj,
        qos_target_name,
        type,
        priority,
        bwmin_goal_kb,
        bwmax_limit_kb,
        iomin_goal,
        iomax_limit,
        bwmin_goal_op,
        bwmax_limit_op,
        iomin_goal_op,
        iomax_limit_op,
        latency_goal,
        default_latency,
        enable,
        latency_goal_usecs):
    if len(qos_target_name) < 1 or len(qos_target_name) > 31:
        return (False, False, "QoS create failed. QoS target name must be atleast 1 character and not more than 31 characters")
    if latency_goal is not None and latency_goal_usecs is not None:
        return (
            False,
            False,
            "Attributes latency_goal and latency_goal_usecs cannot be given \
at the same time for qos rules creation")
    try:
        if not client_obj.qosRuleExists(qos_target_name, type):
            qos_rules = construct_qos_rules_map(
                bwmin_goal_kb,
                bwmax_limit_kb,
                iomin_goal,
                iomax_limit,
                latency_goal,
                default_latency,
                enable,
                latency_goal_usecs,
                priority,
                bwmin_goal_op,
                bwmax_limit_op,
                iomin_goal_op,
                iomax_limit_op)

            client_obj.createQoSRules(
                qos_target_name,
                qos_rules,
                getattr(client.HPE3ParClient, type.upper()))
        else:
            return (True, False, "QoS already present")
    except exceptions.ClientException as e:
        return (False, False, "QoS creation failed | %s" % e)
    return (True, True, "Created QoS successfully.")


def modify_qos_rule(
        client_obj,
        qos_target_name,
        type,
        priority,
        bwmin_goal_kb,
        bwmax_limit_kb,
        iomin_goal,
        iomax_limit,
        bwmin_goal_op,
        bwmax_limit_op,
        iomin_goal_op,
        iomax_limit_op,
        latency_goal,
        default_latency,
        enable,
        latency_goal_usecs):
    if len(qos_target_name) < 1 or len(qos_target_name) > 31:
        return (False, False, "QoS create failed. QoS target name must be atleast 1 character and not more than 31 characters")
    try:
        qos_rules = construct_qos_rules_map(
            bwmin_goal_kb,
            bwmax_limit_kb,
            iomin_goal,
            iomax_limit,
            latency_goal,
            default_latency,
            enable,
            latency_goal_usecs,
            priority,
            bwmin_goal_op,
            bwmax_limit_op,
            iomin_goal_op,
            iomax_limit_op)
        client_obj.modifyQoSRules(qos_target_name, qos_rules, type)
    except exceptions.ClientException as e:
        return (False, False, "QoS modification failed | %s" % e)
    return (True, True, "Modified QoS successfully.")


def delete_qos_rule(
        client_obj,
        qos_target_name,
        type):
    if len(qos_target_name) < 1 or len(qos_target_name) > 31:
        return (False, False, "QoS create failed. QoS target name must be atleast 1 character and not more than 31 characters")
    try:
        if client_obj.qosRuleExists(qos_target_name, type):
            client_obj.deleteQoSRules(qos_target_name, type)
        else:
            return (True, False, "QoS does not exist")
    except exceptions.ClientException as e:
        return (False, False, "QoS delete failed | %s" % e)
    return (True, True, "Deleted QoS successfully.")


def construct_qos_rules_map(
        bwmin_goal_kb,
        bwmax_limit_kb,
        iomin_goal,
        iomax_limit,
        latency_goal,
        default_latency,
        enable,
        latency_goal_usecs,
        priority,
        bwmin_goal_op,
        bwmax_limit_op,
        iomin_goal_op,
        iomax_limit_op):
    qos_rules = {
        'bwMinGoalKB': bwmin_goal_kb,
        'bwMaxLimitKB': bwmax_limit_kb,
        'ioMinGoal': iomin_goal,
        'ioMaxLimit': iomax_limit,
        'latencyGoal': latency_goal,
        'defaultLatency': default_latency,
        'enable': enable,
        'latencyGoaluSecs': latency_goal_usecs
    }
    if priority is not None:
        qos_rules['priority'] = getattr(
            client.HPE3ParClient.QOSPriority, priority)

    if bwmin_goal_op is not None:
        qos_rules['bwMinGoalOP'] = getattr(client.HPE3ParClient, bwmin_goal_op)

    if bwmax_limit_op is not None:
        qos_rules['bwMaxLimitOP'] = getattr(
            client.HPE3ParClient, bwmax_limit_op)

    if iomin_goal_op is not None:
        qos_rules['ioMinGoalOP'] = getattr(client.HPE3ParClient, iomin_goal_op)

    if iomax_limit_op is not None:
        qos_rules['ioMaxLimitOP'] = getattr(
            client.HPE3ParClient, iomax_limit_op)
    return qos_rules


def main():
    module = AnsibleModule(argument_spec=hpe3par.qos_argument_spec())

    if not HAS_3PARCLIENT:
        module.fail_json(
            msg='the python hpe3par_sdk library is required (https://pypi.org/project/hpe3par_sdk)')

    storage_system_ip = module.params["storage_system_ip"]
    storage_system_username = module.params["storage_system_username"]
    storage_system_password = module.params["storage_system_password"]

    qos_target_name = module.params["qos_target_name"]
    type = module.params["type"]
    priority = module.params["priority"]
    bwmin_goal_kb = module.params["bwmin_goal_kb"]
    bwmax_limit_kb = module.params["bwmax_limit_kb"]
    iomin_goal = module.params["iomin_goal"]
    iomax_limit = module.params["iomax_limit"]
    bwmin_goal_op = module.params["bwmin_goal_op"]
    bwmax_limit_op = module.params["bwmax_limit_op"]
    iomin_goal_op = module.params["iomin_goal_op"]
    iomax_limit_op = module.params["iomax_limit_op"]
    latency_goal = module.params["latency_goal"]
    default_latency = module.params["default_latency"]
    enable = module.params["enable"]
    latency_goal_usecs = module.params["latency_goal_usecs"]
    secure = module.params["secure"]

    wsapi_url = 'https://%s:8080/api/v1' % storage_system_ip
    client_obj = client.HPE3ParClient(wsapi_url, secure)

    # States
    if module.params["state"] == "present":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = create_qos_rule(
                client_obj,
                qos_target_name, type, priority, bwmin_goal_kb,
                bwmax_limit_kb, iomin_goal, iomax_limit, bwmin_goal_op,
                bwmax_limit_op, iomin_goal_op, iomax_limit_op, latency_goal,
                default_latency, enable, latency_goal_usecs)
        except Exception as e:
            module.fail_json(msg="Clone create failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "modify":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = modify_qos_rule(
                client_obj,
                qos_target_name, type, priority, bwmin_goal_kb,
                bwmax_limit_kb, iomin_goal, iomax_limit, bwmin_goal_op,
                bwmax_limit_op, iomin_goal_op, iomax_limit_op, latency_goal,
                default_latency, enable, latency_goal_usecs)
        except Exception as e:
            module.fail_json(msg="Clone modify failed | %s" % e)
        finally:
            client_obj.logout()
    elif module.params["state"] == "absent":
        try:
            client_obj.login(storage_system_username, storage_system_password)
            return_status, changed, msg = delete_qos_rule(
                client_obj,
                qos_target_name, type)
        except Exception as e:
            module.fail_json(msg="Clone delete failed | %s" % e)
        finally:
            client_obj.logout()
    if return_status:
        module.exit_json(changed=changed, msg=msg)
    else:
        module.fail_json(msg=msg)


if __name__ == '__main__':
    main()
