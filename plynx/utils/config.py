import yaml
import os.path
from collections import namedtuple

CONFIG_NAME = 'config.yaml'
_config = None

MasterConfig = namedtuple('MasterConfig', 'host port')
WorkerConfig = namedtuple('WorkerConfig', 'user')
MongoConfig = namedtuple('MongoConfig', 'user password host port')
StorageConfig = namedtuple('StorageConfig', 'scheme resources stderr stdout worker')
AuthConfig = namedtuple('AuthConfig', 'secret_key')
WebConfig = namedtuple('WebConfig', 'endpoint')
DemoConfig = namedtuple('DemoConfig', 'graph_ids')

Config = namedtuple(
    'Config',
    [
        'master',
        'worker',
        'db',
        'storage',
        'auth',
        'web',
        'demo',
    ]
)


def __init__():
    global _config
    with open(CONFIG_NAME) as f:
        _config = yaml.safe_load(f)
    print _config


def get_master_config():
    return MasterConfig(
        host=_config.get('master', {}).get('host', '127.0.0.1'),
        port=int(_config.get('master', {}).get('port', 10000)),
    )


def get_worker_config():
    return WorkerConfig(
        user=_config.get('worker', {}).get('user', ''),
    )


def get_db_config():
    return MongoConfig(
        user=_config.get('mongodb', {}).get('user', ''),
        password=_config.get('mongodb', {}).get('password', ''),
        host=_config.get('mongodb', {}).get('host', '127.0.0.1'),
        port=int(_config.get('mongodb', {}).get('port', 27017))
    )


def get_storage_config():
    home = os.path.expanduser("~")
    return StorageConfig(
        scheme=_config.get('storage', {}).get('scheme', 'file'),
        resources=_config.get('storage', {}).get('resources', os.path.join(home, 'plynx', 'data')),
        stderr=_config.get('storage', {}).get('stderr', os.path.join(home, 'plynx', 'data')),
        stdout=_config.get('storage', {}).get('stdout', os.path.join(home, 'plynx', 'data')),
        worker=_config.get('storage', {}).get('worker', os.path.join(home, 'plynx', 'data')),
    )


def get_auth_config():
    return AuthConfig(
        secret_key=_config.get('auth', {}).get('secret_key', 'SECRET_KEY'),
    )


def get_web_config():
    return WebConfig(
        endpoint=_config.get('web', {}).get('endpoint', 'http://127.0.0.1:3000'),
    )


def get_demo_config():
    return DemoConfig(
        graph_ids=_config.get('demo', {}).get('graph_ids', []),
    )


def get_config():
    return Config(
        master=get_master_config(),
        worker=get_worker_config(),
        db=get_db_config(),
        storage=get_storage_config(),
        auth=get_auth_config(),
        web=get_web_config(),
        demo=get_demo_config(),
    )


__init__()
