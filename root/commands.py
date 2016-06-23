from command_definitions import Docker, net_exists


health_check = []

pre_start = [
    Docker(['network', 'create', '-d', 'bridge', 'osm'], predicate=lambda: not net_exists('osm')),
]

start = []

change = []

stop = []
