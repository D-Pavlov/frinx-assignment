from dataclasses import dataclass
from typing import Union, Dict

from settings import SUPPORTED_INTERFACES


@dataclass
class Interface:
    name: str
    description: Union[str, None] = None
    max_frame_size: Union[int, None] = None
    port_channel_name: Union[str, None] = None
    config: Union[dict, None] = None


# Interface parser for Cisco IOS-XE-native devices
def parse_interfaces_cisco_ios_xe_native(config: Dict) -> list[Interface]:
    if 'interface' not in config:
        raise KeyError('Config not valid - key `interface` not found.')

    if not isinstance(ifcs := config['interface'], dict):
        raise TypeError((f'Config not valid - `interface` expected '
                         f'to be a key-value map, got {type(ifcs)} instead.'))

    parsed_interfaces = []
    for interface_type, interfaces in config['interface'].items():
        if SUPPORTED_INTERFACES and interface_type not in SUPPORTED_INTERFACES:
            continue

        if not isinstance(ifcs := interfaces, list):
            raise TypeError((f'Config not valid - `interface[{interface_type}]` '
                             f'expected to be a list, got {type(ifcs)} instead.'))

        for i, interface in enumerate(interfaces):
            print(f'{type(interface)=}')
            print(f'{interface=}')
            if not isinstance(interface, dict):
                raise TypeError((f'Interface `{interface_type}[{i}]` expected '
                                  f'to be a key-value map, got {type(interface)} instead.'))

            if 'name' not in interface:
                raise KeyError(f'Interface `{interface_type}[{i}]` missing `name`.')

            if 'mtu' in interface \
                and (mtu := interface['mtu']) is not None \
                and not isinstance(mtu, int):
                    raise ValueError((f'Value for `mtu` expected to be null or integer, '
                                      f'got {type(mtu)} instead.'))

            found_interface = Interface(
                name=f'{interface_type}{interface["name"]}',
                description=interface.get('description', None),
                max_frame_size=interface.get('mtu', None),
                config=interface
            )

            if (pc_key := 'Cisco-IOS-XE-ethernet:channel-group') in interface:
                pc_name = f'Port-channel{interface[pc_key]["number"]}'
                found_interface.port_channel_name = pc_name

            parsed_interfaces.append(found_interface)

    return parsed_interfaces


# Expose parsers
INTERFACE_PARSERS = {
    'Cisco-IOS-XE-native:native': parse_interfaces_cisco_ios_xe_native,
}