import re

from fabric.api import run, put

from host_setup import DOCKER_COMPOSE_EXECUTABLE, mkdir, provide_docker_compose


class CallList(object):
    def __init__(self, command, predicate=lambda: True):
        self.command_list = command
        self.base_command = ['echo']
        self.predicate = predicate

    def execute(self, project, hostname):
        commands = self.base_command + \
                   [command.format(project=project, hostname=hostname) for command in self.command_list]
        if self.predicate():
            return run(' '.join(commands))


class Docker(CallList):
    def __init__(self, command, predicate=lambda: True):
        super(Docker, self).__init__(command=command, predicate=predicate)
        self.base_command = ['docker']


class Compose(CallList):
    def __init__(self, command, predicate=lambda: True):
        super(Compose, self).__init__(command=command, predicate=predicate)
        self.base_command = [DOCKER_COMPOSE_EXECUTABLE]

    def execute(self, project, hostname, environment=None):
        provide_docker_compose()
        compose_main_file = '{0}/docker-compose.yml'.format(project)
        compose_host_file = '{0}/{1}.yml'.format(project, hostname)

        mkdir(project)

        put(local_path=compose_main_file, remote_path=compose_main_file)
        put(local_path=compose_host_file, remote_path=compose_host_file)

        self.base_command += [
            '-f', compose_main_file, '-f', compose_host_file
        ]
        super(Compose, self).execute(project, hostname)


def is_running(container_name):
    result = run('docker ps')
    m = re.search(r'\ {}\r?$'.format(re.escape(container_name)), result, flags=re.MULTILINE)
    return m is not None


def has_succeeded(container_name):
    result = run('docker ps -a')
    pattern = r'{status}.*{container_name}\r?$'.format(status=re.escape('Exited (0)'), container_name=re.escape(container_name))
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def has_succeeded_or_is_running(container_name):
    return is_running(container_name) or has_succeeded(container_name)


def net_exists(network_name):
    result = run('docker network ls')
    return " " + network_name + " " in result


def volume_exists(volume_name):
    result = run('docker volume ls')
    pattern = r'\b{}\r?$'.format(re.escape(volume_name))
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None
