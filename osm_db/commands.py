import functools

import root
from command_definitions import Compose, Docker, volume_not_exists, is_not_running, container_not_exists

health_check = [
    Compose(['ps']),
]

pre_start = root.pre_start + [
    Docker(
        ['volume', 'create', '-d', 'local', '--name', 'osm_world_data'],
        predicate=functools.partial(volume_not_exists, 'osm_world_data')
    ),
    Compose(['up', '-d', 'osm_db']),
]

start = [
    Compose(['up', '-d', 'osm_db'], predicate=functools.partial(is_not_running, 'osm_db')),
    Compose(['up', '-d', 'osm_importer'], predicate=functools.partial(container_not_exists, 'osm_importer')),
    Compose(['start', 'osm_db'], predicate=functools.partial(is_not_running, 'osm_db')),
]

change = [
    Compose(['pull']),
    Compose(['up', '-d', 'osm_db']),
    Compose(['up', '-d', 'osm_importer']),
]

stop = [
    Compose(['stop']),
]

logs = [
    Compose(['logs']),
]
