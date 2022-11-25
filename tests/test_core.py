import pytest

from assignment import extract_interface_configs
from parsers import Interface


@pytest.fixture
def ifc_configs():
    return [
        {
            "name": 1,
            "description": "test",
            "mtu": 9000,
        },
        {
            "name": '0/0/1',
            "description": "test",
        },
        {
            "name": '0/0/2',
            "description": "member of Portchannel1",
            "mtu": 9001,
            "Cisco-IOS-XE-ethernet:channel-group": {
                "number": 1,
            },
        },
    ]


@pytest.fixture
def config(ifc_configs):
    return {
        'frinx-uniconfig-topology:configuration': {
            'Cisco-IOS-XE-native:native': {
                'interface': {
                    'Port-channel': [ifc_configs[0]],
                    'GigabitEthernet': [ifc_configs[1]],
                    'TenGigabitEthernet': [ifc_configs[2]],
                }
            }
        }
    }


@pytest.fixture
def interfaces(ifc_configs):
    return [
        Interface(
            name='Port-channel1',
            description='test',
            max_frame_size=9000,
            config=ifc_configs[0]
        ),
        Interface(
            name='GigabitEthernet0/0/1',
            description='test',
            config=ifc_configs[1]
        ),
        Interface(
            name='TenGigabitEthernet0/0/2',
            description='member of Portchannel1',
            max_frame_size=9001,
            config=ifc_configs[2],
            port_channel_name='Port-channel1'
        ),
    ]


def test_interfaces_extracted_pass(config, interfaces):
    parsed_interfaces = extract_interface_configs(config)

    for interface, parsed in zip(interfaces, parsed_interfaces):
        assert interface == parsed
