import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings as settings
from parsers import INTERFACE_PARSERS
from models import InterfaceConfig
from utils import load_json_config


engine = create_engine(settings.DB_URL, echo=settings.DB_LOUD)
Session = sessionmaker(bind=engine)


def extract_interface_configs(config):
    """
    Iterate through config groups and use parse the data with available parsers
    """
    if settings.CONFIG_ROOT_KEY not in config:
        raise KeyError(f'Key `{settings.CONFIG_ROOT_KEY}` not in config.')

    interfaces = []
    for group_name, group_data in config[settings.CONFIG_ROOT_KEY].items():
        for interface in INTERFACE_PARSERS[group_name](group_data):
            interfaces.append(interface)

    return interfaces


def persist_interface_configs(session, interfaces):
    """
    Presist the parsed interfaces and link the related interfaces to port-channels
    """
    
    not_linked = {}  # for interfaces that cannot be linked on insert
    port_channels = {}  # for Port-channel interfaces to avoid db lookup

    for interface in interfaces:
        interface_db_object = InterfaceConfig(
            name=interface.name,
            description=interface.description,
            config=interface.config,
            max_frame_size=interface.max_frame_size,
            port_channel=port_channels.get(interface.port_channel_name, None)
        )
        session.add(interface_db_object)
        session.commit()

        # Cache port-channels for linking related interfaces
        if interface.name.startswith('Port-channel'):
            port_channels[interface.name] = interface_db_object

        # If interface is the "target" of any relationships
        # update all member interfaces in the `not_linked` buffer
        if interface.name in not_linked:
            for _interface in not_linked[interface.name]:
                _interface.port_channel = interface_db_object
            session.flush()
            not_linked[interface.name] = []

        # If interface is a member of port-channel 
        # and this relationship is not set yet 
        # because the port-channel has not yet been parsed,
        # add it to the `not_linked` buffer to be linked
        # once the "target" interface is persisted
        if interface.port_channel_name and not interface_db_object.port_channel:
            if interface.port_channel_name not in not_linked:
                not_linked[interface.port_channel_name] = []
            not_linked[interface.port_channel_name].append(interface_db_object)

    # Check if there are any interfaces left to link
    for port_channel, interfaces in not_linked.items():
        for interface in interfaces:
            if port_channel not in port_channels:
                logging.warning((f'Interface {interface.name} is declared as a member of '
                                 f'a non-existent port-channel {port_channel}'))
                continue
            interface_db_object.port_channel = port_channels[port_channel]
    session.flush()


if __name__ == '__main__':
    # load JSON config
    config = load_json_config(settings.CONFIG_JSON_PATH)

    # start parsing config & pushing to DB
    with Session() as session:
        interfaces = extract_interface_configs(config)
        persist_interface_configs(session, interfaces)
