import root
from command_definitions import Compose, has_succeeded_or_is_running, container_exists

health_check = [
    Compose(['ps']),
]

pre_start = root.pre_start
# Currently fails because of missing networks: https://github.com/docker/compose/issues/2908
# pre_start += [
#     Compose(['create', '--no-recreate', 'coast_land_sea_database']),
#     Compose(['create', '--no-recreate', 'coast_land_sea_importer']),
# ]

start = [
    Compose(
        ['up', '-d', 'coast_land_sea_database'],
        predicate=lambda: not container_exists('coast_land_sea_database')
    ),
    Compose(
        ['up', '-d', 'coast_land_sea_importer'],
        predicate=lambda: not has_succeeded_or_is_running('coast_land_sea_importer')
    ),
]

change = [
    Compose(['pull']),
    Compose(['up', '-d', 'coast_land_sea_database']),
    Compose(['up', '-d', 'coast_land_sea_importer']),
] + start

stop = [
    Compose(['stop', 'coast_land_sea_database', 'coast_land_sea_importer']),
]
