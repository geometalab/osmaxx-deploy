import root
from command_definitions import Compose, Docker, volume_exists

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
    Compose(['pull']),
    Compose(['up', '-d', 'osm_db']),
    Compose(['up', '-d', 'osm_importer']),
    Compose(['ps']),
]

change = [
    Compose(['pull']),
    Compose(['up', '-d', 'osm_db']),
    Compose(['up', '-d', 'osm_importer']),
    Compose(['ps']),
]

stop = [

]
