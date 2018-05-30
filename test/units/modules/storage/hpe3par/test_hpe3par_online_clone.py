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
from ansible.modules.storage.hpe3par import hpe3par_online_clone
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import hpe3par


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.AnsibleModule')
def test_module_args(mock_module, mock_client):
    """
    hpe3par online clone - test module arguments
    """
    PARAMS_FOR_PRESENT = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': 'base_volume',
        'dest_cpg': 'dest_cpg',
        'tpvv': False,
        'tdvv': False,
        'snap_cpg': 'snap_cpg',
        'compression': False,
        'state': 'present',
        'secure': False
    }

    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    hpe3par_online_clone.main()
    mock_module.assert_called_with(
        argument_spec=hpe3par.online_clone_argument_spec())


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.create_online_clone')
def test_main_exit_present(mock_create_online_clone, mock_module, mock_client):
    """
    hpe3par online clone - success check
    """
    PARAMS_FOR_PRESENT = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_name': '3PAR',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': 'base_volume',
        'dest_cpg': 'dest_cpg',
        'tpvv': False,
        'tdvv': False,
        'snap_cpg': 'snap_cpg',
        'compression': False,
        'state': 'present',
        'secure': False
    }
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_create_online_clone.return_value = (
        True, True, "Created Online clone successfully.")
    hpe3par_online_clone.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Created Online clone successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.delete_clone')
def test_main_exit_absent(mock_delete_clone, mock_module, mock_client):
    """
    hpe3par online clone - success check
    """
    PARAMS_FOR_ABSENT = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_name': '3PAR',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': 'base_volume',
        'dest_cpg': None,
        'tpvv': False,
        'tdvv': False,
        'snap_cpg': 'snap_cpg',
        'compression': False,
        'state': 'absent',
        'secure': False
    }
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_ABSENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_delete_clone.return_value = (
        True, True, "Deleted Online clone successfully.")
    hpe3par_online_clone.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Deleted Online clone successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.resync_clone')
def test_main_exit_resync(mock_resync_clone, mock_module, mock_client):
    """
    hpe3par online clone - success check
    """
    PARAMS_FOR_RESYNC = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_name': '3PAR',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': None,
        'dest_cpg': None,
        'tpvv': False,
        'tdvv': False,
        'snap_cpg': 'snap_cpg',
        'compression': False,
        'state': 'resync',
        'secure': False
    }
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_RESYNC
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_resync_clone.return_value = (
        True, True, "Resynced Online clone successfully.")
    hpe3par_online_clone.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Resynced Online clone successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.client')
def test_create_online_clone(mock_client):
    mock_client.HPE3ParClient.login.return_value = None
    mock_client.HPE3ParClient.volumeExists.return_value = False
    mock_client.HPE3ParClient.copyVolume.return_value = None
    mock_client.HPE3ParClient.logout.return_value = None
    assert hpe3par_online_clone.create_online_clone(mock_client.HPE3ParClient,
                                                    'base_volume',
                                                    'test_clone',
                                                    'dest_cpg',
                                                    False,
                                                    False,
                                                    'snap_cpg',
                                                    False
                                                    ) == (True, True, "Created Online Clone %s successfully." % 'test_clone')

    mock_client.HPE3ParClient.volumeExists.return_value = True
    assert hpe3par_online_clone.create_online_clone(mock_client.HPE3ParClient,
                                                    'base_volume',
                                                    'test_clone',
                                                    'dest_cpg',
                                                    False,
                                                    False,
                                                    'snap_cpg',
                                                    False
                                                    ) == (True, False, "Clone already exists / creation in progress. Nothing to do.")
    assert hpe3par_online_clone.create_online_clone(mock_client.HPE3ParClient,
                                                    None,
                                                    'test_clone',
                                                    'dest_cpg',
                                                    False,
                                                    False,
                                                    'snap_cpg',
                                                    False
                                                    ) == (False, False, "Online clone create failed. Base volume name is null")


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.client')
def test_delete_clone(mock_client):
    mock_client.HPE3ParClient.login.return_value = True
    mock_client.HPE3ParClient.setSSHOptions.return_value = True
    mock_client.HPE3ParClient.volumeExists.return_value = True
    mock_client.HPE3ParClient.offlinePhysicalCopyExists.return_value = False
    mock_client.HPE3ParClient.onlinePhysicalCopyExists.return_value = False
    mock_client.HPE3ParClient.deleteVolume.return_value = None
    assert hpe3par_online_clone.delete_clone(mock_client.HPE3ParClient,
                                             'test_clone',
                                             'base_volume'
                                             ) == (True, True, "Deleted Online Clone %s successfully." % 'test_clone')

    mock_client.HPE3ParClient.offlinePhysicalCopyExists.return_value = True
    assert hpe3par_online_clone.delete_clone(mock_client.HPE3ParClient,
                                             'test_clone',
                                             'base_volume'
                                             ) == (False, False, "Clone/Volume is busy. Cannot be deleted")

    assert hpe3par_online_clone.delete_clone(mock_client.HPE3ParClient,
                                             'test_clone',
                                             None
                                             ) == (False, False, "Online clone delete failed. Base volume name is null")


@mock.patch('ansible.modules.storage.hpe3par.hpe3par_online_clone.client')
def test_resync_clone(mock_client):
    mock_client.HPE3ParClient.login.return_value = True
    assert hpe3par_online_clone.resync_clone(mock_client.HPE3ParClient,
                                             'test_clone'
                                             ) == (True, True, "Resync-ed Online Clone %s successfully." % 'test_clone')
