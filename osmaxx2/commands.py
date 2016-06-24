import root
from command_definitions import Compose, container_exists, has_succeeded_or_is_running

COMPOSE_PROJECT_NAME = 'osmaxx2'

health_check = [
    Compose(['ps']),
]

pre_start = root.pre_start + [
    Compose(['up', '-d', 'frontenddatabase']),
    Compose(
        ['run', '--rm', 'frontend', 'python3', 'web_frontend/manage.py', 'createsuperuser'],
        predicate=lambda: not container_exists(r'[a-zA-Z0-9]+\_frontend\_[a-zA-Z0-9]+', name_is_regex=True)
    ),
]
# Currently fails because of missing networks: https://github.com/docker/compose/issues/2908
# pre_start += [
#     Compose(['create', '--no-recreate', 'frontenddatabase']),
#     Compose(['create', '--no-recreate', '']),
# ]

start = [
    Compose(
        ['up', '-d'],
        predicate=lambda: not container_exists('')
    ),
    Compose(
        ['up', '-d'],
        predicate=lambda: not has_succeeded_or_is_running('')
    ),
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
