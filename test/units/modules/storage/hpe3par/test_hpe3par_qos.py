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

import mock
import pytest
import sys
sys.modules['hpe3par_sdk'] = mock.Mock()
sys.modules['hpe3par_sdk.client'] = mock.Mock()
sys.modules['hpe3parclient'] = mock.Mock()
sys.modules['hpe3parclient.exceptions'] = mock.Mock()
from ansible.modules.storage.hpe3par import hpe3par_qos as qos
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import hpe3par



PARAMS_FOR_PRESENT = {'storage_system_ip': '192.168.0.1', 'storage_system_username': 'USER',
					  'storage_system_password': 'PASS', 'qos_target_name': 'target', 'type': 'vvset', 'state': 'present',
					  'priority': 'LOW', 'bwmin_goal_kb': 1, 'bwmax_limit_kb': 1, 'iomin_goal': 1, 'iomax_limit': 1, 'bwmin_goal_op': 'ZERO',
					  'bwmax_limit_op': 'ZERO', 'iomin_goal_op': 'ZERO', 'iomax_limit_op': 'ZERO', 'latency_goal': 1, 'default_latency': False,
					  'enable': False, 'latency_goal_usecs': 1, 'secure': False}


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.AnsibleModule')
def test_module_args(mock_module, mock_client):
	"""
	hpe3par flash cache - test module arguments
	"""

	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.return_value = mock_module
	qos.main()
	mock_module.assert_called_with(
		argument_spec=hpe3par.qos_argument_spec())

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.create_qos_rule')
def test_main_exit_functionality_success_without_issue_attr_dict(mock_create_qos_rule, mock_module, mock_client):
	"""
	hpe3par flash cache - success check
	"""
	# This creates a instance of the AnsibleModule mock.
	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.return_value = mock_module
	instance = mock_module.return_value
	mock_create_qos_rule.return_value = (True, True, "Created QOS successfully.")
	qos.main()
	# AnsibleModule.exit_json should be called
	instance.exit_json.assert_called_with(
		changed=True, msg="Created QOS successfully.")
	# AnsibleModule.fail_json should not be called
	assert instance.fail_json.call_count == 0

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.create_qos_rule')
def test_main_exit_functionality_fail(mock_create_qos_rule, mock_module, mock_client):
	"""
	hpe3par flash cache - exit fail check
	"""
	# This creates a instance of the AnsibleModule mock.
	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.return_value = mock_module
	instance = mock_module.return_value
	mock_create_qos_rule.return_value = (False, False, "QOS creation failed.")
	qos.main()

	# AnsibleModule.exit_json should not be activated
	assert instance.exit_json.call_count == 0
	# AnsibleModule.fail_json should be called
	instance.fail_json.assert_called_with(msg='QOS creation failed.')

# Create

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_create_qos_rule_create_already_present(mock_client):
	"""
	hpe3par qos - create a qos rule
	"""
	result = qos.create_qos_rule(mock_client, 'qos_tgt', None, None, None,
								 None, None, None, None, None, None, None, None, None, None, None)
	assert result == (True, False, "QoS already present")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_create_qos_rule_create_sucess_login(mock_client):
	"""
	hpe3par qos - create a qos rule
	"""
	mock_client.HPE3ParClient.qosRuleExists.return_value = False
	mock_client.HPE3ParClient.return_value = mock_client
	result = qos.create_qos_rule(mock_client.HPE3ParClient, 'qos_tgt_name', 'vvset',
								 None, None, None, None, None, None, None, None, None, None, None, None, None)
	assert result == (True, True, "Created QoS successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_create_qos_rule_create_sucess_login_latency_goal_latency_goal_usecs(mock_client):
	"""
	hpe3par qos - create a qos rule
	"""
	mock_client.HPE3ParClient.qosRuleExists.return_value = False
	mock_client.HPE3ParClient.return_value = mock_client
	result = qos.create_qos_rule(mock_client.HPE3ParClient, 'qos_tgt_name', None,
								 None, None, None, None, None, None, None, None, None, 20, None, None, 10)
	assert result == (False, False, 'Attributes latency_goal and latency_goal_usecs cannot be given at the same time for qos rules creation')

# Delete

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_delete_qos_rule_create_already_present(mock_client):
	"""
	hpe3par qos - delete a qos rule
	"""
	mock_client.qosRuleExists.return_value = False
	mock_client.return_value = mock_client
	result = qos.delete_qos_rule(mock_client, 'qos_tgt_name', None)
	assert result == (True, False, "QoS does not exist")


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_delete_qos_rule_create_sucess_login(mock_client):
	"""
	hpe3par qos - delete a qos rule
	"""
	mock_client.HPE3ParClient.qosRuleExists.return_value = True
	mock_client.HPE3ParClient.return_value = mock_client
	result = qos.delete_qos_rule(mock_client.HPE3ParClient, 'qos_tgt_name', None)
	assert result == (True, True, "Deleted QoS successfully.")

# Modify

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_modify_qos_rule_create_already_present(mock_client):
	"""
	hpe3par qos - modify a qos rule
	"""
	result = qos.modify_qos_rule(mock_client, 'qos_tgt_name', None, None, None,
								 None, None, None, None, None, None, None, None, None, None, None)
	assert result == (True, True, "Modified QoS successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_modify_qos_rule_create_sucess_login(mock_client):
	"""
	hpe3par qos - modify a qos rule
	"""
	mock_client.HPE3ParClient.qosRuleExists.return_value = False
	mock_client.HPE3ParClient.return_value = mock_client
	result = qos.modify_qos_rule(mock_client.HPE3ParClient, 'qos_tgt_name', None, None,
								 None, None, None, None, None, None, None, None, None, None, None, None)
	assert result == (True, True, "Modified QoS successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_construct_qos_rules_map_priority(mock_client):
	"""
	hpe3par qos - construct_qos_rules
	"""
	mock_client.HPE3ParClient.QOSPriority.LOW = 1
	result = qos.construct_qos_rules_map(None, None, None, None, None, None, None, None, 'LOW', None, None, None, None)
	assert result['priority'] == 1

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_construct_qos_rules_map_bwMinGoalOP(mock_client):
	"""
	hpe3par qos - construct_qos_rules
	"""
	mock_client.HPE3ParClient.QOSPriority.LOW = 1
	mock_client.HPE3ParClient.ZERO = 1
	result = qos.construct_qos_rules_map(None, None, None, None, None, None, None, None, 'LOW', 'ZERO', None, None, None)
	assert result['bwMinGoalOP'] == 1

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_construct_qos_rules_map_bwMaxLimitOP(mock_client):
	"""
	hpe3par qos - construct_qos_rules
	"""
	mock_client.HPE3ParClient.QOSPriority.LOW = 1
	mock_client.HPE3ParClient.ZERO = 1
	result = qos.construct_qos_rules_map(None, None, None, None, None, None, None, None, 'LOW', 'ZERO', 'ZERO', None, None)
	assert result['bwMaxLimitOP'] == 1

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_construct_qos_rules_map_iomin_goal_op(mock_client):
	"""
	hpe3par qos - construct_qos_rules
	"""
	mock_client.HPE3ParClient.QOSPriority.LOW = 1
	mock_client.HPE3ParClient.ZERO = 1
	result = qos.construct_qos_rules_map(None, None, None, None, None, None, None, None, 'LOW', 'ZERO', 'ZERO', 'ZERO', None)
	assert result['ioMinGoalOP'] == 1

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
def test_construct_qos_rules_map_iomax_limit_op(mock_client):
	"""
	hpe3par qos - construct_qos_rules
	"""
	mock_client.HPE3ParClient.QOSPriority.LOW = 1
	mock_client.HPE3ParClient.ZERO = 1
	result = qos.construct_qos_rules_map(None, None, None, None, None, None, None, None, 'LOW', 'ZERO', 'ZERO', 'ZERO', 'ZERO')
	assert result['ioMaxLimitOP'] == 1

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.create_qos_rule')
def test_main_exit_functionality_success_without_issue_attr_dict_present(mock_create_qos_rule, mock_module, mock_client):
	"""
	hpe3par flash cache - success check
	"""
	# This creates a instance of the AnsibleModule mock.
	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.params["state"] = "present"
	mock_module.return_value = mock_module
	instance = mock_module.return_value
	mock_create_qos_rule.return_value = (True, True, "Created QOS successfully.")
	qos.main()
	# AnsibleModule.exit_json should be called
	instance.exit_json.assert_called_with(
		changed=True, msg="Created QOS successfully.")
	# AnsibleModule.fail_json should not be called
	assert instance.fail_json.call_count == 0

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.delete_qos_rule')
def test_main_exit_functionality_success_without_issue_attr_dict_absent(mock_delete_qos_rule, mock_module, mock_client):
	"""
	hpe3par flash cache - success check
	"""
	# This creates a instance of the AnsibleModule mock.
	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.params["state"] = "absent"
	mock_module.return_value = mock_module
	instance = mock_module.return_value
	mock_delete_qos_rule.return_value = (True, True, "Created QOS successfully.")
	qos.main()
	# AnsibleModule.exit_json should be called
	instance.exit_json.assert_called_with(
		changed=True, msg="Created QOS successfully.")
	# AnsibleModule.fail_json should not be called
	assert instance.fail_json.call_count == 0

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_qos.modify_qos_rule')
def test_main_exit_functionality_success_without_issue_attr_dict_modify(mock_modify_qos_rule, mock_module, mock_client):
	"""
	hpe3par flash cache - success check
	"""
	# This creates a instance of the AnsibleModule mock.
	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.params["state"] = "modify"
	mock_module.return_value = mock_module
	instance = mock_module.return_value
	mock_modify_qos_rule.return_value = (True, True, "Created QOS successfully.")
	qos.main()
	# AnsibleModule.exit_json should be called
	instance.exit_json.assert_called_with(
		changed=True, msg="Created QOS successfully.")
	# AnsibleModule.fail_json should not be called
	assert instance.fail_json.call_count == 0
