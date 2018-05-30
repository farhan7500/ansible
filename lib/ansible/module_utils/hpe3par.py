storage_system_spec = {
    "storage_system_ip": {
        "required": True,
        "type": "str"
    },
    "storage_system_username": {
        "required": True,
        "type": "str",
        "no_log": True
    },
    "storage_system_password": {
        "required": True,
        "type": "str",
        "no_log": True
    },
    "secure": {
        "type": "bool",
        "default": False
    }
}


def cpg_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent'],
            "type": 'str'
        },
        "cpg_name": {
            "required": True,
            "type": "str"
        },
        "domain": {
            "type": "str"
        },
        "growth_increment": {
            "type": "float",
            "default": -1.0
        },
        "growth_increment_unit": {
            "type": "str",
            "choices": ['TiB', 'GiB', 'MiB'],
            "default": 'GiB'
        },
        "growth_limit": {
            "type": "float",
            "default": -1.0
        },
        "growth_limit_unit": {
            "type": "str",
            "choices": ['TiB', 'GiB', 'MiB'],
            "default": 'GiB'
        },
        "growth_warning": {
            "type": "float",
            "default": -1.0
        },
        "growth_warning_unit": {
            "type": "str",
            "choices": ['TiB', 'GiB', 'MiB'],
            "default": 'GiB'
        },
        "raid_type": {
            "required": False,
            "type": "str",
            "choices": ['R0', 'R1', 'R5', 'R6']
        },
        "set_size": {
            "required": False,
            "type": "int",
            "default": -1
        },
        "high_availability": {
            "type": "str",
            "choices": ['PORT', 'CAGE', 'MAG']
        },
        "disk_type": {
            "type": "str",
            "choices": ['FC', 'NL', 'SSD']
        }
    }
    spec.update(storage_system_spec)
    return spec


def flash_cache_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent'],
            "type": 'str'
        },
        "size_in_gib": {
            "type": "int"
        },
        "mode": {
            "type": "int"
        }
    }
    spec.update(storage_system_spec)
    return spec


def host_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": [
                'present',
                'absent',
                'modify',
                'add_initiator_chap',
                'remove_initiator_chap',
                'add_target_chap',
                'remove_target_chap',
                'add_fc_path_to_host',
                'remove_fc_path_from_host',
                'add_iscsi_path_to_host',
                'remove_iscsi_path_from_host'
            ],
            "type": 'str'
        },
        "host_name": {
            "type": "str",
            "reuqired": True
        },
        "host_domain": {
            "type": "str"
        },
        "host_new_name": {
            "type": "str"
        },
        "host_fc_wwns": {
            "type": "list"
        },
        "host_iscsi_names": {
            "type": "list"
        },
        "host_persona": {
            "type": "str",
            "choices": [
                "GENERIC",
                "GENERIC_ALUA",
                "GENERIC_LEGACY",
                "HPUX_LEGACY",
                "AIX_LEGACY",
                "EGENERA",
                "ONTAP_LEGACY",
                "VMWARE",
                "OPENVMS",
                "HPUX",
                "WINDOWS_SERVER"
            ]
        },
        "force_path_removal": {
            "type": "bool"
        },
        "chap_name": {
            "type": "str"
        },
        "chap_secret": {
            "type": "str"
        },
        "chap_secret_hex": {
            "type": "bool"
        }
    }
    spec.update(storage_system_spec)
    return spec


def hostset_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent', 'add_hosts', 'remove_hosts'],
            "type": 'str'
        },
        "hostset_name": {
            "required": True,
            "type": "str"
        },
        "domain": {
            "type": "str"
        },
        "setmembers": {
            "type": "list"
        }
    }
    spec.update(storage_system_spec)
    return spec


def offline_clone_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent', 'resync', 'stop'],
            "type": 'str'
        },
        "clone_name": {
            "type": "str",
            "required": True
        },
        "base_volume_name": {
            "type": "str"
        },
        "dest_cpg": {
            "type": "str"
        },
        "save_snapshot": {
            "type": "bool"
        },
        "priority": {
            "type": "str",
            "choices": ['HIGH', 'MEDIUM', 'LOW'],
            "default": "MEDIUM"
        },
        "skip_zero": {
            "type": "bool"
        }
    }
    spec.update(storage_system_spec)
    return spec


def online_clone_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent', 'resync'],
            "type": 'str'
        },
        "clone_name": {
            "required": True,
            "type": "str"
        },
        "base_volume_name": {
            "type": "str"
        },
        "dest_cpg": {
            "type": "str",
        },
        "tpvv": {
            "type": "bool",
        },
        "tdvv": {
            "type": "bool",
        },
        "snap_cpg": {
            "type": "str",
        },
        "compression": {
            "type": "bool",
        }
    }
    spec.update(storage_system_spec)
    return spec


def qos_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent', 'modify'],
            "type": 'str'
        },
        "qos_target_name": {
            "required": True,
            "type": "str"
        },
        "type": {
            "choices": ['vvset', 'sys'],
            "type": "str"
        },
        "priority": {
            "choices": ['LOW', 'NORMAL', 'HIGH'],
            "default": 'LOW',
            "type": "str"
        },
        "bwmin_goal_kb": {
            "type": "int",
            "default": -1
        },
        "bwmax_limit_kb": {
            "type": "int",
            "default": -1
        },
        "iomin_goal": {
            "type": "int",
            "default": -1
        },
        "iomax_limit": {
            "type": "int",
            "default": -1
        },
        "bwmin_goal_op": {
            "type": "str",
            "choices": ['ZERO', 'NOLIMIT']
        },
        "bwmax_limit_op": {
            "type": "str",
            "choices": ['ZERO', 'NOLIMIT']
        },
        "iomin_goal_op": {
            "type": "str",
            "choices": ['ZERO', 'NOLIMIT']
        },
        "iomax_limit_op": {
            "type": "str",
            "choices": ['ZERO', 'NOLIMIT']
        },
        "latency_goal": {
            "type": "int"
        },
        "default_latency": {
            "type": "bool",
            "default": False
        },
        "enable": {
            "type": "bool",
            "default": False
        },
        "latency_goal_usecs": {
            "type": "int"
        }
    }
    spec.update(storage_system_spec)
    return spec


def snapshot_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent', 'modify', 'restore_offline',
                        'restore_online'],
            "type": 'str'
        },
        "snapshot_name": {
            "required": True,
            "type": "str"
        },
        "base_volume_name": {
            "type": "str"
        },
        "read_only": {
            "type": "bool"
        },
        "expiration_time": {
            "type": "int",
        },
        "retention_time": {
            "type": "int"
        },
        "expiration_unit": {
            "type": "str",
            "choices": ['Hours', 'Days'],
            "default": 'Hours'
        },
        "retention_unit": {
            "type": "str",
            "choices": ['Hours', 'Days'],
            "default": 'Hours'
        },
        "expiration_hours": {
            "type": "int",
            "default": 0
        },
        "retention_hours": {
            "type": "int",
            "default": 0
        },
        "priority": {
            "type": "str",
            "choices": ['HIGH', 'MEDIUM', 'LOW'],
        },
        "allow_remote_copy_parent": {
            "type": "bool"
        },
        "new_name": {
            "type": "str"
        },
        "rm_exp_time": {
            "type": "bool"
        }
    }
    spec.update(storage_system_spec)
    return spec


def vlun_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": [
                'export_volume_to_host',
                'unexport_volume_from_host',
                'export_volumeset_to_host',
                'unexport_volumeset_from_host',
                'export_volume_to_hostset',
                'unexport_volume_from_hostset',
                'export_volumeset_to_hostset',
                'unexport_volumeset_from_hostset'],
            "type": 'str'},
        "volume_name": {
            "type": "str"},
        "volume_set_name": {
            "type": "str"},
        "lunid": {
            "type": "int"},
        "autolun": {
            "type": "bool",
            "default": False},
        "host_name": {
            "type": "str"},
        "host_set_name": {
            "type": "str"},
        "node_val": {
            "type": "int"},
        "slot": {
            "type": "int"},
        "card_port": {
            "type": "int"}}
    spec.update(storage_system_spec)
    return spec


def volume_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present',
                        'absent',
                        'modify',
                        'grow',
                        'grow_to_size',
                        'change_snap_cpg',
                        'change_user_cpg',
                        'convert_type',
                        'set_snap_cpg'
                        ],
            "type": 'str'
        },
        "volume_name": {
            "required": True,
            "type": "str"
        },
        "cpg": {
            "type": "str",
            "default": None
        },
        "size": {
            "type": "float",
            "default": None
        },
        "size_unit": {
            "choices": ['MiB', 'GiB', 'TiB'],
            "type": 'str',
            "default": 'MiB'
        },
        "snap_cpg": {
            "type": "str"
        },
        "wait_for_task_to_end": {
            "type": "bool",
            "default": False
        },
        "new_name": {
            "type": "str",
        },
        "expiration_hours": {
            "type": "int",
            "default": 0
        },
        "retention_hours": {
            "type": "int",
            "default": 0
        },
        "ss_spc_alloc_warning_pct": {
            "type": "int",
            "default": 0
        },
        "ss_spc_alloc_limit_pct": {
            "type": "int",
            "default": 0
        },
        "usr_spc_alloc_warning_pct": {
            "required": False,
            "type": "int",
            "default": 0
        },
        "usr_spc_alloc_limit_pct": {
            "type": "int",
            "default": 0
        },
        "rm_ss_spc_alloc_warning": {
            "type": "bool",
            "default": False
        },
        "rm_usr_spc_alloc_warning": {
            "type": "bool",
            "default": False
        },
        "rm_exp_time": {
            "type": "bool",
            "default": False
        },
        "rm_usr_spc_alloc_limit": {
            "type": "bool",
            "default": False
        },
        "rm_ss_spc_alloc_limit": {
            "type": "bool",
            "default": False
        },
        "compression": {
            "type": "bool",
            "default": False
        },
        "type": {
            "choices": ['thin', 'thin_dedupe', 'full'],
            "type": "str",
            "default": "thin"
        },
        "keep_vv": {
            "type": "str",
        }
    }
    spec.update(storage_system_spec)
    return spec


def volumeset_argument_spec():
    spec = {
        "state": {
            "required": True,
            "choices": ['present', 'absent', 'add_volumes', 'remove_volumes'],
            "type": 'str'
        },
        "volumeset_name": {
            "required": True,
            "type": "str"
        },
        "domain": {
            "type": "str"
        },
        "setmembers": {
            "type": "list"
        }
    }
    spec.update(storage_system_spec)
    return spec
