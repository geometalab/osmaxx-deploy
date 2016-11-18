from command_definitions import Docker, net_exists

health_check = []

pre_start = [
    Docker(['network', 'create', '-d', 'bridge', 'nginx-proxy'], predicate=lambda: not net_exists('nginx-proxy')),
]

start = []

change = []

stop = []

logs = []
