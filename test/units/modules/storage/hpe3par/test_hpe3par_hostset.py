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
from ansible.modules.storage.hpe3par import hpe3par_hostset as hostset
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import hpe3par


PARAMS_FOR_PRESENT = {'state': 'present', 'storage_system_username': 'USER',
                      'storage_system_ip': '192.168.0.1', 'storage_system_password': 'PASS',
                      'hostset_name': 'hostset', 'domain': 'domain', 'setmembers': 'new', 'secure': False}

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.AnsibleModule')
def test_module_args(mock_module, mock_client):
    """
    hpe3par host set - test module arguments
    """

    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    hostset.main()
    mock_module.assert_called_with(
        argument_spec=hpe3par.hostset_argument_spec())
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.create_hostset')
def test_main_exit_functionality_success_without_issue_attr_dict(mock_hostset, mock_module, mock_client):
    """
    hpe3par hostset - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_hostset.return_value = (
        True, True, "Created hostset host successfully.")
    hostset.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Created hostset host successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.create_hostset')
def test_main_exit_functionality_fail(mock_hostset, mock_module, mock_client):
    """
    hpe3par hostset - exit fail check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_hostset.return_value = (
        False, False, "hostset creation failed.")
    hostset.main()

    # AnsibleModule.exit_json should not be activated
    assert instance.exit_json.call_count == 0
    # AnsibleModule.fail_json should be called
    instance.fail_json.assert_called_with(msg='hostset creation failed.')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_create_hostset_create_already_present(mock_client):
    """
    hpe3par hostset - create a hostset
    """
    result = hostset.create_hostset(
        mock_client, "host", None, None)
    assert result == (True, False, "Hostset already present")
    

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_create_hostset_create_sucess(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.hostSetExists.return_value = False
    result = hostset.create_hostset(
        mock_client.HPE3ParClient, "hostname", "domain", ["member1"])
    assert result == (True, True, "Created Hostset hostname successfully.")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_create_hostset_create_fail(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.hostSetExists.return_value = True
    result = hostset.create_hostset(
        mock_client.HPE3ParClient, "hostname", "domain", ["member1"])
    assert result == (True, False, 'Hostset already present')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_delete_hostset_success(mock_client):
    """
    hpe3par hostset - delete a hostset
    """
    mock_client.hostSetExists.return_value = True
    mock_client.return_value = mock_client
    result = hostset.delete_hostset(mock_client, "host")
    assert result == (True, True, 'Deleted Hostset host successfully.')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_delete_hostset_fail(mock_client):
    """
    hpe3par hostset - delete a hostset
    """
    mock_client.hostSetExists.return_value = False
    mock_client.return_value = mock_client
    result = hostset.delete_hostset(mock_client, "host")
    assert result == (True, False, "Hostset does not exist")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_add_host_to_hostset_hostset_setmembers_empty(mock_client):
    """
    hpe3par hostset - create a hostset
    """
    result = hostset.add_hosts(
        mock_client, "hostset", None)

    assert result == (
        False,
        False,
        "setmembers delete failed. Setmembers is null")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_add_host_to_hostset_hostset_create_sucess_login(mock_client):
    """
    hpe3par hostset - create a hostset
    """
    result = hostset.add_hosts(
        mock_client, "host", ["members"])
    assert result == (True, True, 'Added hosts successfully.')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_add_host_to_hostset_hostset_doesnt_exists(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.hostSetExists.return_value = False
    result = hostset.add_hosts(
        mock_client.HPE3ParClient, "hostname", ["member1"])
    assert result == (False, False, "Hostset does not exist")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_add_host_to_hostset_No_new_members_to_add_to_the_Host_set(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.getHostSet.return_value.setmembers = [
        "member1"]
    result = hostset.add_hosts(
        mock_client.HPE3ParClient, "hostname", ["member1"])
    assert result == (True, False, "No new members to add to the Host set hostname. Nothing to do.")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_add_host_to_hostset_No_new_members_to_add_to_the_Host_set_login(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.getHostSet.return_value.setmembers = []
    result = hostset.add_hosts(
        mock_client.HPE3ParClient, "hostname", ["member1"])
    assert result == (True, True, 'Added hosts successfully.')

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_add_host_to_hostset_No_new_members_to_add_to_the_Host_set_login_setmembers_none(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.getHostSet.return_value.setmembers = None
    result = hostset.add_hosts(
        mock_client.HPE3ParClient, "hostname", ["member1"])
    assert result == (True, True, 'Added hosts successfully.')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_remove_host_from_hostset_hostset_setmembers_empty(mock_client):
    """
    hpe3par hostset - create a hostset
    """
    result = hostset.remove_hosts(
        mock_client, "hostset", None)

    assert result == (
        False,
        False,
        "setmembers delete failed. Setmembers is null")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_remove_host_from_hostset_hostset_create_sucess_login(mock_client):
    """
    hpe3par hostset - create a hostset
    """
    mock_client.hostSetExists.return_value = True
    mock_client.getHostSet.return_value.setmembers = ["members"]
    mock_client.return_value = mock_client
    result = hostset.remove_hosts(
        mock_client, "host", ["members"])
    assert result == (True, True, 'Removed hosts successfully.')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_remove_host_from_hostset_hostset_doesnt_exists(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.hostSetExists.return_value = False
    result = hostset.remove_hosts(
        mock_client.HPE3ParClient, "hostname", ["member1"])
    assert result == (True, False, "Hostset does not exist")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_remove_host_from_hostset_No_new_members_to_remove_from_the_Host_set(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.getHostSet.return_value.setmembers = []
    result = hostset.remove_hosts(
        mock_client.HPE3ParClient, "hostname", ["member1"])
    assert result == (True, False, "No members to remove from the Host set hostname. Nothing to do.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
def test_remove_host_from_hostset_No_new_members_to_remove_from_the_Host_set_setmembers_none(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.getHostSet.return_value.setmembers = None
    result = hostset.remove_hosts(
        mock_client.HPE3ParClient, "hostname", ["member1"])
    assert result == (True, True, 'Removed hosts successfully.')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.create_hostset')
def test_main_exit_functionality_success(mock_hostset, mock_module, mock_client):
    """
    hpe3par hostset - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "present"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_hostset.return_value = (
        True, True, "Created hostset host successfully.")
    hostset.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Created hostset host successfully.")
		
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.add_hosts')
def test_main_exit_functionality_success_without_issue_attr_dict_add_hosts(mock_hostset, mock_module, mock_client):
	"""
	hpe3par hostset - success check
	"""
	# This creates a instance of the AnsibleModule mock.
	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.params["state"] = "add_hosts"
	mock_module.return_value = mock_module
	instance = mock_module.return_value
	mock_hostset.return_value = (
		True, True, "add_hosts hostset host successfully.")
	hostset.main()
	# AnsibleModule.exit_json should be called
	instance.exit_json.assert_called_with(
		changed=True, msg="add_hosts hostset host successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_hostset.remove_hosts')
def test_main_exit_functionality_success_without_issue_attr_dict_remove_hosts(mock_hostset, mock_module, mock_client):
	"""
	hpe3par hostset - success check
	"""
	# This creates a instance of the AnsibleModule mock.
	mock_module.params = PARAMS_FOR_PRESENT
	mock_module.params["state"] = "remove_hosts"
	mock_module.return_value = mock_module
	instance = mock_module.return_value
	mock_hostset.return_value = (
		True, True, "remove_hosts hostset host successfully.")
	hostset.main()
	# AnsibleModule.exit_json should be called
	instance.exit_json.assert_called_with(
		changed=True, msg="remove_hosts hostset host successfully.")
