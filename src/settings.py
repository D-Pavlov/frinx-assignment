import os
from pathlib import Path


## Database settings
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_URL = (f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
DB_LOUD = bool(os.environ.get('DB_LOUD', False))


##
CONFIG_JSON_PATH = Path(os.environ['CONFIG_JSON_PATH'])
CONFIG_ROOT_KEY = 'frinx-uniconfig-topology:configuration'
SUPPORTED_INTERFACES = [
    'TenGigabitEthernet',
    'GigabitEthernet',
    'Port-channel',
    # 'BDI',
    # 'Loopback',
]
