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
import sys
sys.modules['hpe3par_sdk'] = mock.Mock()
sys.modules['hpe3par_sdk.client'] = mock.Mock()
sys.modules['hpe3par_sdk.client.HPE3ParClient'] = mock.Mock()
sys.modules['hpe3parclient'] = mock.Mock()
sys.modules['hpe3parclient.exceptions'] = mock.Mock()
from ansible.modules.storage.hpe3par import hpe3par_host as host
from ansible.module_utils.basic import AnsibleModule as ansible
from ansible.module_utils import hpe3par
import pytest


PARAMS_FOR_PRESENT = {'state': 'present', 'storage_system_ip': '192.168.0.1', 'storage_system_username': 'USER',
                      'storage_system_password': 'PASS', 'host_name': 'host', 'host_domain': 'domain', 'host_new_name': 'new',
                      'host_fc_wwns': ['PASS'], 'host_iscsi_names': ['host'], 'host_persona': 'GENERIC', 'force_path_removal': 'true',
                      'chap_name': 'chap', 'chap_secret': 'secret', 'chap_secret_hex': 'true', 'secure': False}


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
def test_module_args(mock_module, mock_client):
    """
    hpe3par flash cache - test module arguments
    """

    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    host.main()
    mock_module.assert_called_with(
        argument_spec=hpe3par.host_argument_spec())

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.create_host')
def test_main_exit_functionality_success_without_issue_attr_dict(mock_host, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_host.return_value = (
        True, True, "Created host host successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Created host host successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.create_host')
def test_main_exit_functionality_fail(mock_host, mock_module, mock_client):
    """
    hpe3par host - exit fail check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_host.return_value = (
        False, False, "Host creation failed.")
    mock_client.HPE3ParClient.login.return_value=True
    host.main()

    # AnsibleModule.exit_json should not be activated
    assert instance.exit_json.call_count == 0
    # AnsibleModule.fail_json should be called
    instance.fail_json.assert_called_with(msg='Host creation failed.')
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_create_host_create_already_present(mock_client):
    """
    hpe3par host - create a host
    """
    result = host.create_host(
        mock_client, "host", None, None, None, None)
    assert result == (True, False, "Host already present")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_delete_host_create_already_present(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.hostExists.return_value = False
    result = host.delete_host(
        mock_client.HPE3ParClient, "hostname")
    assert result == (True, False, "Host does not exist")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_modify_host_create_success(mock_client):
    """
    hpe3par host - Modify a host
    """
    result = host.modify_host(
        mock_client.HPE3ParClient, "host_name", None, None)
    assert result == (True, True, "Modified host host_name successfully.")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_initiator_chap_chapname_empty(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_initiator_chap(
        mock_client, "host", None, None, None)

    assert result == (
        False,
        False,
        "Host modification failed. Chap name is null")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_initiator_chap_chapsecret_empty(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_initiator_chap(
        mock_client, "host", "chap", None, None)

    assert result == (
        False,
        False,
        "Host modification failed. chap_secret is null")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_initiator_chap_chaphex_true(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_initiator_chap(
        mock_client, "user", "chap", "secret", True)

    assert result == (
        False,
        False,
        "Add initiator chap failed. Chap secret hex is false and chap secret less than 32 characters"
    )

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_initiator_chap_chaphex_false(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_initiator_chap(
        mock_client, "user", "chap", "secret", False)

    assert result == (
        False,
        False,
        "Add initiator chap failed. Chap secret hex is false and chap secret less than 12 characters or more than 16 characters"
    )

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_initiator_chap_success(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    mock_client.HPE3ParClient.CHAP_INITIATOR = 1
    mock_client.HPE3ParClient.HOST_EDIT_ADD = 1
    result = host.add_initiator_chap(
        mock_client, "host", "chap", "secretsecretsecretsecretsecret12", True)

    assert result == (
        True, True, "Added initiator chap.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.initiator_chap_exists')
def test_add_target_chap_exists(mock_initiator_chap_exists, mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    mock_initiator_chap_exists.return_value = False
    result = host.add_target_chap(mock_client.HPE3ParClient, "host", "chap", "secretsecretsecretsecretsecret12", True)

    assert result == (
        True, False, "Initiator chap does not exist")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_target_chap_success(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    mock_client.HPE3ParClient.CHAP_TARGET = 1
    mock_client.HPE3ParClient.HOST_EDIT_ADD = 1
    result = host.add_target_chap(
        mock_client, "host", "chap", "secretsecretsecretsecretsecret12", True)

    assert result == (
        True, True, "Added target chap.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_initiator_chap_exists_sucess(mock_client):
    """
    hpe3par host - initiator_chap_exists
    """
    mock_client.getHost.return_value.initiator_chap_enabled = True
    result = host.initiator_chap_exists(mock_client, "host")
    assert result == True
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_target_chap_chapname_empty(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_target_chap(
        mock_client, "host", None, None, None)

    assert result == (
        False,
        False,
        "Host modification failed. Chap name is null")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_target_chap_chapsecret_empty(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_target_chap(
        mock_client, "host", "chap", None, None)

    assert result== (
        False,
        False,
        "Host modification failed. chap_secret is null")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_target_chap_chaphex_true(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_target_chap(
        mock_client, "host", "chap", "secret", True)

    assert result == (
        False,
        False,
        "Attribute chap_secret must be 32 hexadecimal characters if chap_secret_hex is true")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_target_chap_chaphex_false(mock_client):
    """
    hpe3par host - add_initiator_chap
    """
    result = host.add_target_chap(
        mock_client, "host", "chap", "secret", False)

    assert result == (
        False,
        False,
        "Attribute chap_secret must be 12 to 16 character if chap_secret_hex is false")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_initiator_chap_exists_sucess(mock_client):
    """
    hpe3par host - initiator_chap_exists
    """
    mock_client.getHost.return_value.initiator_chap_enabled = True
    result = host.initiator_chap_exists(
        mock_client, "host")
    assert result == True
    

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_remove_initiator_chap_sucess(mock_client):
    """
    hpe3par host - remove_initiator_chap
    """
    mock_client.HPE3ParClient.HOST_EDIT_REMOVE = 1
    result = host.remove_initiator_chap(
        mock_client, "host")

    assert result == (
        True, True, "Removed initiator chap.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_remove_target_chap_success(mock_client):
    """
    hpe3par host - remove_target_chap
    """
    mock_client.HPE3ParClient.HOST_EDIT_REMOVE = 1
    result = host.remove_target_chap(
        mock_client.HPE3ParClient, "host")

    assert result == (
        True, True, "Removed target chap.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_FC_empty(mock_client):
    """
    hpe3par host - add_fc_path_to_host
    """
    result = host.add_fc_path_to_host(
        mock_client, "host", None)

    assert result == (
        False,
        False,
        "Host modification failed. host_fc_wwns is null")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_add_FC_success(mock_client):
    """
    hpe3par host - add_fc_path_to_host
    """
    mock_client.HPE3ParClient.HOST_EDIT_ADD = 1
    result = host.add_fc_path_to_host(
        mock_client.HPE3ParClient, "host", "iscsi")

    assert result == (
        True, True, "Added FC path to host successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_remove_fc_fcwwns_empty(mock_client):
    """
    hpe3par host - remove_fc_path_from_host
    """
    result = host.remove_fc_path_from_host(
        mock_client, "host", None, None)

    assert result == (
        False,
        False,
        "Host modification failed. host_fc_wwns is null")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_remove_fc_sucess(mock_client):
    """
    hpe3par host - remove_fc_path_from_host
    """
    mock_client.HPE3ParClient.HOST_EDIT_REMOVE = 1
    result = host.remove_fc_path_from_host(
        mock_client, "host", "fcwwns", None)

    assert result == (
        True, True, "Removed FC path from host successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_remove_iscsi_empty(mock_client):
    """
    hpe3par host - remove_iscsi_path_from_host
    """
    result = host.remove_iscsi_path_from_host(
        mock_client, "host", None, None)

    assert result == (
        False,
        False,
        "Host modification failed. host_iscsi_names is null")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
def test_remove_iscsi_sucess(mock_client):
    """
    hpe3par host - remove_iscsi_path_from_host
    """
    mock_client.HPE3ParClient.HOST_EDIT_REMOVE = 1
    result = host.remove_iscsi_path_from_host(
        mock_client, "host", "iscsi", None)

    assert result == (
        True, True, "Removed ISCSI path from host successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.create_host')
def test_main_exit_functionality_success_without_issue_attr_dict_present(mock_host, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "present"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_client.HPE3ParClient.login.return_value = True
    mock_host.return_value = (
        True, True, "Created host host successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Created host host successfully.")
        

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.create_host')
def test_main_exit_functionality_success_without_issue_attr_dict_modify(mock_host, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "modify"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Modified host host successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.add_initiator_chap')
def test_main_exit_functionality_success_without_issue_attr_dict_add_initiator_chap(mock_add_initiator_chap, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "add_initiator_chap"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_add_initiator_chap.return_value = (
        True, True, "Add_initiator_chap successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Add_initiator_chap successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.add_initiator_chap')
def test_main_exit_functionality_success_without_issue_attr_dict_add_initiator_chap(mock_add_initiator_chap, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "add_initiator_chap"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_add_initiator_chap.return_value = (
        True, True, "Add_initiator_chap successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Add_initiator_chap successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.add_initiator_chap')
def test_main_exit_functionality_success_without_issue_attr_dict_add_initiator_chap(mock_add_initiator_chap, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "add_initiator_chap"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_add_initiator_chap.return_value = (
        True, True, "Add_initiator_chap successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Add_initiator_chap successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.remove_initiator_chap')
def test_main_exit_functionality_success_without_issue_attr_dict_remove_initiator_chap(mock_add_initiator_chap, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "remove_initiator_chap"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_add_initiator_chap.return_value = (
        True, True, "Remove_initiator_chap successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Remove_initiator_chap successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.add_target_chap')
def test_main_exit_functionality_success_without_issue_attr_dict_add_target_chap(
        mock_add_target_chap, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "add_target_chap"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_add_target_chap.return_value = (
        True, True, "add_target_chap successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="add_target_chap successfully.")



@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.add_fc_path_to_host')
def test_main_exit_functionality_success_without_issue_attr_dict_add_fc_path_to_host(mock_add_fc_path_to_host, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "add_fc_path_to_host"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_add_fc_path_to_host.return_value = (
        True, True, "add_fc_path_to_host successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="add_fc_path_to_host successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.remove_fc_path_from_host')
def test_main_exit_functionality_success_without_issue_attr_dict_remove_fc_path_from_host(mock_remove_fc_path_from_host, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "remove_fc_path_from_host"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_remove_fc_path_from_host.return_value = (
        True, True, "remove_fc_path_from_host successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="remove_fc_path_from_host successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.add_iscsi_path_to_host')
def test_main_exit_functionality_success_without_issue_attr_dict_add_iscsi_path_to_host(mock_add_iscsi_path_to_host, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "add_iscsi_path_to_host"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_add_iscsi_path_to_host.return_value = (
        True, True, "add_iscsi_path_to_host successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="add_iscsi_path_to_host successfully.")
    # AnsibleModule.fail_json should not be called
    # self.assertEqual(instance.fail_json.call_count, 0)

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.remove_iscsi_path_from_host')
def test_main_exit_functionality_success_without_issue_attr_dict_remove_iscsi_path_from_host(
        mock_remove_iscsi_path_from_host, mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "remove_iscsi_path_from_host"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_remove_iscsi_path_from_host.return_value = (
        True, True, "remove_iscsi_path_from_host successfully.")
    host.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="remove_iscsi_path_from_host successfully.")
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_host.AnsibleModule')
def test_main_exit_functionality_success_without_issue_attr_dict_remove_target_chap(
        mock_module, mock_client):
    """
    hpe3par host - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.params["state"] = "remove_target_chap"
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    host.remove_target_chap = mock.Mock(return_value=(
        True, True, "Remove_target_chap successfully."))
    host.main()
    # AnsibleModule.exit_json should be called
    mock_module.exit_json.assert_called_with(
        changed=True, msg="Remove_target_chap successfully.")
