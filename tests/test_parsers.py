import pytest
import parsers


def test_cisco_config_missing_interfaces_raises():
    config = {}  # config that does not contain the `interface` key

    with pytest.raises(KeyError):
        _ = parsers.parse_interfaces_cisco_ios_xe_native(config)


def test_cisco_config_interfaces_not_grouped_by_type_raises():
    config = {
        'interface': [],
    }

    with pytest.raises(TypeError):
        _ = parsers.parse_interfaces_cisco_ios_xe_native(config)


def test_cisco_config_interface_group_not_list_raises():
    config = {
        'interface': {
            'Port-channel': {}
        }
    }

    with pytest.raises(TypeError):
        _ = parsers.parse_interfaces_cisco_ios_xe_native(config)


def test_cisco_config_interface_not_a_dictionary_raises():
    config = {
        'interface': {
            'Port-channel': ['value']
        },
    }

    with pytest.raises(TypeError):
        _ = parsers.parse_interfaces_cisco_ios_xe_native(config)


def test_cisco_config_interface_missing_name_raises():
    config = {
        'interface': {
            'Port-channel': [
                {
                    'other-key-than-name': 'value'
                }
            ]
        },
    }

    with pytest.raises(KeyError):
        _ = parsers.parse_interfaces_cisco_ios_xe_native(config)


def test_cisco_config_interface_max_frame_size_not_integer_raises():
    config = {
        'interface': {
            'Port-channel': [
                {
                    'name': 'TestInterface',
                    'mtu': 'not a number',
                }
            ]
        },
    }

    with pytest.raises(ValueError):
        _ = parsers.parse_interfaces_cisco_ios_xe_native(config)


def test_cisco_pass():
    ifc_config = {
        'name': 'TestInterface',
        'description': 'Member of Port-channel1',
        'Cisco-IOS-XE-ethernet:channel-group': {
            'number': 1
        }
    }
    config = {
        'interface': {
            'GigabitEthernet': [ifc_config]
        }
    }

    interface = parsers.Interface(
        name='GigabitEthernetTestInterface',
        description='Member of Port-channel1',
        max_frame_size=None,
        config=ifc_config,
        port_channel_name='Port-channel1'
    )

    found = parsers.parse_interfaces_cisco_ios_xe_native(config)

    assert len(found) == 1
    assert found[0] == interface
