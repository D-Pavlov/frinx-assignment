import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import models
import settings


@pytest.fixture(scope='session')
def connection():
    engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        os.environ.get('TEST_DB_USER'),
        os.environ.get('TEST_DB_PASS'),
        os.environ.get('TEST_DB_HOST'),
        os.environ.get('TEST_DB_PORT'),
        os.environ.get('TEST_DB_NAME'),
    ))

    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()

    yield

    models.Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


def test_interface_config_created(db_session):
    db_session.add(models.InterfaceConfig(
        name='GigabitEthernetTest',
        connection=None,
        description='test ethernet interface',
        config={
            'name': 'Test',
            'description': 'test ethernet interface',
            'mpu': 600,
        }
    ))
    db_session.commit()
