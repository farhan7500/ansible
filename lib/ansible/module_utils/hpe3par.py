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
