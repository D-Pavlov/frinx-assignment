import logging

from sqlalchemy.orm import declarative_base, relationship, RelationshipProperty
from sqlalchemy import (create_engine, inspect, Column, Sequence,
                        Integer, String, JSON, ForeignKey,)

import settings


Base = declarative_base()
engine = create_engine(settings.DB_URL, echo=True)


class InterfaceConfig(Base):
    __tablename__ = 'interfaces'

    id = Column(Integer, Sequence('interface_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    connection = Column(Integer)
    description = Column(String(255))
    config = Column(JSON)
    type_ = Column('type', String(50))
    infra_type = Column(String(50))
    max_frame_size = Column(Integer)
    port_channel_id = Column(Integer, ForeignKey('interfaces.id'))
    port_channel = relationship('InterfaceConfig', remote_side=[id])

    def __repr__(self):
        return f'InterfaceConfig(name={self.name})'


def safe_db_setup(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    errors = []
    table = InterfaceConfig.__tablename__

    if table not in tables:
        InterfaceConfig.__table__.create(bind=engine, checkfirst=True)
        return

    columns = {col['name']: col for col in inspector.get_columns(table)}
    mapper = inspect(InterfaceConfig)
    print(mapper.attrs)
    for column_prop in mapper.attrs:
        if isinstance(column_prop, RelationshipProperty):
            # TODO: check if relationship is defined correctly
            pass
        else:
            for column in column_prop.columns:
                if column.key not in columns:
                    error_msg = f'Column `{column.key}` does not exist in the table `{table}`'
                    logging.error(error_msg)
                    errors.append(error_msg)
                else:
                    # TODO: check column types
                    pass

    if errors:
        err_list = '\n'.join(errors)
        raise Exception((f'Table {table} exists but is not matching the model:\n'
                         f'{err_list}'))

safe_db_setup(engine)