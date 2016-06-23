import root
from command_definitions import Compose, Docker, volume_exists, container_exists, is_running

health_check = [
    Compose(['ps']),
]

pre_start = root.pre_start + [
    Docker(
        ['volume', 'create', '-d', 'local', '--name', 'osm_world_data'],
        predicate=lambda: not volume_exists('osm_world_data')
    ),
    Compose(['up', '-d', 'osm_db']),
]

start = [
    Compose(['up', '-d', 'osm_db'], predicate=lambda: not is_running('osm_db')),
    Compose(['up', '-d', 'osm_importer'], predicate=lambda: not container_exists('osm_importer')),
    Compose(['start', 'osm_db'], predicate=lambda: not is_running('osm_db')),
]

change = [
    Compose(['pull']),
    Compose(['up', '-d', 'osm_db']),
    Compose(['up', '-d', 'osm_importer']),
]

stop = [
    Compose(['stop']),
]
