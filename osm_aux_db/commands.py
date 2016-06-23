import root
from command_definitions import Compose, has_succeeded_or_is_running

health_check = [
    Compose(['ps']),
]

pre_start = root.pre_start
# Currently fails because of missing networks: https://github.com/docker/compose/issues/2908
# pre_start += [
#     Compose(['create', '--no-recreate', 'osmboundaries_database']),
#     Compose(['create', '--no-recreate', 'osmboundaries_importer']),
# ]

start = [
    Compose(['up', '-d', 'osmboundaries_database']),
    Compose(
        ['up', '-d', 'osmboundaries_importer'],
        predicate=lambda: not has_succeeded_or_is_running('osmboundaries_importer')
    ),
]

change = [
    Compose(['pull']),
] + start

stop = [
    Compose(['stop', 'osmboundaries_database', 'osmboundaries_importer']),
]
