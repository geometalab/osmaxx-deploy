import functools
import os
import re

import root
from ruamel import yaml
from command_definitions import Compose, container_exists, is_running


def is_not_running(service_name, name_is_regex=True):
    return not is_running(service_name, name_is_regex=name_is_regex)


def container_name_regex(service_name):
    return r'{compose_project}\_{service}\_\d+'.format(
        compose_project=re.escape(ENVIRONMENT['COMPOSE_PROJECT_NAME']),
        service=re.escape(service_name),
    )

ENVIRONMENT = dict(
    COMPOSE_PROJECT_NAME='osmaxx2',
)

health_check = [
    Compose(['ps']),
]

pre_start = root.pre_start + [
    Compose(
        ['run', '--rm', 'frontend', 'python3', 'web_frontend/manage.py', 'createsuperuser'],
        predicate=lambda: not container_exists(container_name_regex('frontenddatabase'), name_is_regex=True)
    ),
]
# Currently fails because of missing networks: https://github.com/docker/compose/issues/2908
# pre_start += [
#     Compose(['create', '--no-recreate', 'frontenddatabase']),
#     Compose(['create', '--no-recreate', '']),
# ]

with open(os.path.join(os.path.dirname(__file__), 'docker-compose.yml')) as f:
    SERVICE_NAMES = yaml.load(f)['services'].keys()

start = [
    Compose(
        ['up', '-d', service],
        predicate=functools.partial(is_not_running, container_name_regex(service))
    )
    for service in SERVICE_NAMES
]

change = [
    Compose(['pull']),
    Compose(['up', '-d']),
]

stop = [
    Compose(['stop']),
]

logs = [
    Compose(['logs']),
]

