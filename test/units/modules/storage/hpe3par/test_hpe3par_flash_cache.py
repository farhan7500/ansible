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
sys.modules['hpe3parclient'] = mock.Mock()
sys.modules['hpe3parclient.exceptions'] = mock.Mock()
from ansible.modules.storage.hpe3par import hpe3par_flash_cache as flash_cache
from ansible.module_utils.basic import AnsibleModule as ansible
from ansible.module_utils import hpe3par
import pytest


PARAMS_FOR_PRESENT = {'storage_system_ip': '192.168.0.1', 'storage_system_username': 'USER',
                      'storage_system_password': 'PASS', 'size_in_gib': 1024, 'mode': 1, 'state': 'present'}

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.AnsibleModule')
def test_module_args(mock_module, mock_client):
    """
    hpe3par flash cache - test module arguments
    """

    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    flash_cache.main()
    mock_module.assert_called_with(
        argument_spec=hpe3par.flash_cache_argument_spec())

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.create_flash_cache')
def test_main_exit_functionality_success_without_issue_attr_dict(mock_create_flash_cache, mock_module, mock_client):
    """
    hpe3par flash cache - success check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_client.HPE3PARClient.login.return_value=True
    mock_create_flash_cache.return_value = (True, True, "Created Flash Cache successfully.")
    flash_cache.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Created Flash Cache successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.create_flash_cache')
def test_main_exit_functionality_fail(mock_create_flash_cache, mock_module, mock_client):
    """
    hpe3par flash cache - exit fail check
    """
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_client.HPE3PARClient.login.return_value=True
    mock_create_flash_cache.return_value = (False, False, "Flash Cache creation failed.")
    flash_cache.main()

    # AnsibleModule.exit_json should not be activated
    assert instance.exit_json.call_count == 0
    # AnsibleModule.fail_json should be called
    instance.fail_json.assert_called_with(msg='Flash Cache creation failed.')

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
def test_create_flash_cache_size_in_gib_empty(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    result = flash_cache.create_flash_cache(mock_client, None, None)

    assert result == (
        False,
        False,
        "Flash Cache creation failed. Size is null",
    )

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
def test_create_flash_cache_create_already_present(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    result = flash_cache.create_flash_cache(mock_client, 1024, None)
    assert result == (True, False, "Flash Cache already present")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
def test_create_flash_cache_create_sucess_login(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    mock_client.HPE3ParClient.flashCacheExists.return_value = False
    result = flash_cache.create_flash_cache(mock_client.HPE3ParClient, 1024, None)
    assert result == (True, True, "Created Flash Cache successfully.")

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
def test_delete_flash_cache_create_absent(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    result = flash_cache.delete_flash_cache(mock_client)
    assert result == (True, True, "Deleted Flash Cache successfully.")
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_flash_cache.client')
def test_delete_flash_cache_create_present(mock_client):
    """
    hpe3par flash cache - create a flash cache
    """
    result = flash_cache.delete_flash_cache(mock_client)
    assert result == (True, True, "Deleted Flash Cache successfully.")

