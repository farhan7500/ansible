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
from ansible.modules.storage.hpe3par import hpe3par_offline_clone
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import hpe3par

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.create_offline_clone')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.AnsibleModule')
def test_module_args(mock_module, mock_create_offline_clone):
    """
    hpe3par offline clone - test module arguments
    """
    PARAMS_FOR_PRESENT = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': 'base_volume',
        'dest_cpg': 'dest_cpg',
        'save_snapshot': False,
        'priority': 'MEDIUM',
        'skip_zero': False,
        'state': 'present',
        'secure': False
    }

    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    mock_create_offline_clone.return_value = (True, True, "Created Offline Clone successfully.")
    hpe3par_offline_clone.main()
    mock_module.assert_called_with(
        argument_spec=hpe3par.offline_clone_argument_spec())
        
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.create_offline_clone')
def test_main_exit_present(mock_create_offline_clone, mock_module, mock_client):
    """
    hpe3par offline clone - success check
    """
    PARAMS_FOR_PRESENT = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_name': '3PAR',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': 'base_volume',
        'dest_cpg': 'dest_cpg',
        'save_snapshot': False,
        'priority': 'MEDIUM',
        'skip_zero': False,
        'state': 'present',
        'secure': False
    }
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_PRESENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_create_offline_clone.return_value = (
        True, True, "Created Offline clone successfully.")
    hpe3par_offline_clone.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Created Offline clone successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.delete_clone')
def test_main_exit_absent(mock_delete_clone, mock_module, mock_client):
    """
    hpe3par offline clone - success check
    """
    PARAMS_FOR_ABSENT = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_name': '3PAR',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': 'base_volume',
        'dest_cpg': None,
        'save_snapshot': None,
        'priority': None,
        'skip_zero': None,
        'state': 'absent',
        'secure': False
    }
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_ABSENT
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_delete_clone.return_value = (
        True, True, "Deleted Offline clone successfully.")
    hpe3par_offline_clone.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Deleted Offline clone successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.resync_clone')
def test_main_exit_resync(mock_resync_clone, mock_module, mock_client):
    """
    hpe3par offline clone - success check
    """
    PARAMS_FOR_RESYNC = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_name': '3PAR',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': None,
        'dest_cpg': None,
        'save_snapshot': None,
        'priority': None,
        'skip_zero': None,
        'state': 'resync',
        'secure': False
    }
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_RESYNC
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_resync_clone.return_value = (
        True, True, "Resynced Offline clone successfully.")
    hpe3par_offline_clone.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Resynced Offline clone successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.AnsibleModule')
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.stop_clone')
def test_main_exit_stop(mock_stop_clone, mock_module, mock_client):
    """
    hpe3par offline clone - success check
    """
    PARAMS_FOR_RESYNC = {
        'storage_system_ip': '192.168.0.1',
        'storage_system_name': '3PAR',
        'storage_system_username': 'USER',
        'storage_system_password': 'PASS',
        'clone_name': 'test_clone',
        'base_volume_name': 'base_volume',
        'dest_cpg': None,
        'save_snapshot': None,
        'priority': None,
        'skip_zero': None,
        'state': 'stop',
        'secure': False
    }
    # This creates a instance of the AnsibleModule mock.
    mock_module.params = PARAMS_FOR_RESYNC
    mock_module.return_value = mock_module
    instance = mock_module.return_value
    mock_stop_clone.return_value = (
        True, True, "Stopped Offline clone successfully.")
    hpe3par_offline_clone.main()
    # AnsibleModule.exit_json should be called
    instance.exit_json.assert_called_with(
        changed=True, msg="Stopped Offline clone successfully.")
    # AnsibleModule.fail_json should not be called
    assert instance.fail_json.call_count == 0
    
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
def test_create_offline_clone(mock_client):
    mock_client.HPE3ParClient.login.return_value = True
    mock_client.HPE3ParClient.setSSHOptions.return_value = True
    mock_client.HPE3ParClient.copyVolume.return_value = True
    mock_client.HPE3ParClient.onlinePhysicalCopyExists.return_value = False
    mock_client.HPE3ParClient.offlinePhysicalCopyExists.return_value = False
    mock_client.HPE3ParClient.logout.return_value = None
    assert hpe3par_offline_clone.create_offline_clone(mock_client.HPE3ParClient,
                                                                'test_clone',
                                                                'base_volume',
                                                                'dest_cpg',
                                                                False,
                                                                False,
                                                                'MEDIUM'
                                                                ) == (True, True, "Created Offline Clone %s successfully." % 'test_clone')

    mock_client.HPE3ParClient.onlinePhysicalCopyExists.return_value = True
    assert hpe3par_offline_clone.create_offline_clone(mock_client.HPE3ParClient,
                                                                'test_clone',
                                                                'base_volume',
                                                                'dest_cpg',
                                                                False,
                                                                False,
                                                                'MEDIUM'
                                                                ) == (True, False, "Clone already exists / creation in progress. Nothing to do.")
    assert hpe3par_offline_clone.create_offline_clone(mock_client.HPE3ParClient,
                                                                'test_clone',
                                                                None,
                                                                'dest_cpg',
                                                                False,
                                                                False,
                                                                'MEDIUM'
                                                                ) == (False, False, "Offline clone create failed. Base volume name is null")
                                                                
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
def test_resync_clone(mock_client):
    mock_client.HPE3ParClient.login.return_value = True
    assert hpe3par_offline_clone.resync_clone(mock_client.HPE3ParClient,
                                                        'test_clone'
                                                        ) == (True, True, "Resync-ed Offline Clone %s successfully." % 'test_clone')

@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
def test_stop_clone(mock_client):
    mock_client.HPE3ParClient.login.return_value = True
    mock_client.HPE3ParClient.setSSHOptions.return_value = True
    mock_client.HPE3ParClient.volumeExists.return_value = True
    mock_client.HPE3ParClient.offlinePhysicalCopyExists.return_value = True
    mock_client.HPE3ParClient.stopOfflinePhysicalCopy.return_value = None
    assert hpe3par_offline_clone.stop_clone(mock_client.HPE3ParClient,
                                                      'test_clone',
                                                      'base_volume'
                                                      ) == (True, True, "Stopped Offline Clone %s successfully." % 'test_clone')

    mock_client.HPE3ParClient.volumeExists.return_value = False
    assert hpe3par_offline_clone.stop_clone(mock_client.HPE3ParClient,
                                                      'test_clone',
                                                      'base_volume'
                                                      ) == (True, False, "Offline Cloning not in progress")
    assert hpe3par_offline_clone.stop_clone(mock_client.HPE3ParClient,
                                                      'test_clone',
                                                      None
                                                      ) == (False, False, "Offline clone stop failed. Base volume name is null")
                                                      
@mock.patch('ansible.modules.storage.hpe3par.hpe3par_offline_clone.client')
def test_delete_clone(mock_client):
    mock_client.HPE3ParClient.login.return_value = True
    mock_client.HPE3ParClient.setSSHOptions.return_value = True
    mock_client.HPE3ParClient.volumeExists.return_value = True
    mock_client.HPE3ParClient.offlinePhysicalCopyExists.return_value = False
    mock_client.HPE3ParClient.onlinePhysicalCopyExists.return_value = False
    mock_client.HPE3ParClient.deleteVolume.return_value = None
    assert hpe3par_offline_clone.delete_clone(mock_client.HPE3ParClient,
                                                        'test_clone',
                                                        'base_volume'
                                                        ) == (True, True, "Deleted Offline Clone %s successfully." % 'test_clone')

    mock_client.HPE3ParClient.offlinePhysicalCopyExists.return_value = True
    assert hpe3par_offline_clone.delete_clone(mock_client.HPE3ParClient,
                                                        'test_clone',
                                                        'base_volume'
                                                        ) == (False, False, "Clone/Volume is busy. Cannot be deleted")
    assert hpe3par_offline_clone.delete_clone(mock_client.HPE3ParClient,
                                                        'test_clone',
                                                        None
                                                        ) == (False, False, "Offline clone delete failed. Base volume name is null")
