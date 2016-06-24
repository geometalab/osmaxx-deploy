import glob
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
        env_file_path = "{}/*.env".format(project)
        if len(glob.glob(env_file_path)) > 0:
            put(local_path="{}/*.env".format(project), remote_path="{}/".format(project))

        self.base_command += [
            '-f', compose_main_file, '-f', compose_host_file
        ]
        super(Compose, self).execute(project, hostname)


def is_running(container_name, name_is_regex=False):
    if not name_is_regex:
        container_name = re.escape(container_name)
    result = run('docker ps')
    m = re.search(r'\ {}\r?$'.format(container_name), result, flags=re.MULTILINE)
    return m is not None


def has_succeeded(container_name, name_is_regex=False):
    if not name_is_regex:
        container_name = re.escape(container_name)
    result = run('docker ps -a')
    pattern = r'{status}.*{container_name}\r?$'.format(status=re.escape('Exited (0)'), container_name=container_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def container_exists(container_name, name_is_regex=False):
    if not name_is_regex:
        container_name = re.escape(container_name)
    result = run('docker ps -a')
    pattern = r'.*{container_name}\r?$'.format(container_name=container_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def has_succeeded_or_is_running(container_name, name_is_regex=False):
    return is_running(container_name, name_is_regex=name_is_regex) or has_succeeded(container_name, name_is_regex=name_is_regex)


def net_exists(network_name, name_is_regex=False):
    if not name_is_regex:
        network_name = re.escape(network_name)
    result = run('docker network ls')
    pattern = r'\s+{network_name}\s+'.format(network_name=network_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def volume_exists(volume_name, name_is_regex=False):
    if not name_is_regex:
        volume_name = re.escape(volume_name)
    result = run('docker volume ls')
    pattern = r'\b{}\r?$'.format(volume_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None
