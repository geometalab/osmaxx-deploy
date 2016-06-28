import glob
import re

from fabric.api import run, put

from host_setup import DOCKER_COMPOSE_EXECUTABLE, mkdir, provide_docker_compose


class CallList(object):
    base_command = ['echo']

    def __init__(self, command, predicate=lambda: True):
        self.command_list = command
        self.predicate = predicate

    def execute(self, project, hostname, environment=None):
        if environment is None:
            environment = {}

        if self.predicate():
            command_args = [command.format(project=project, hostname=hostname) for command in self.command_list]
            command = ' '.join(
                self.base_command + command_args
            )
            return run('{} {}'.format(self._environment_strings(environment=environment), command))

    def _environment_strings(self, environment):
        return ' '.join([
            '{}={}'.format(env_var_name, env_var_value) for env_var_name, env_var_value in environment.items()
        ])


class Docker(CallList):
    base_command = ['docker']


class Compose(CallList):
    base_command = [DOCKER_COMPOSE_EXECUTABLE]

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
        super(Compose, self).execute(project, hostname, environment=environment)


def is_running(container_name, name_is_regex=False):
    if not name_is_regex:
        container_name = re.escape(container_name)
    result = run('docker ps')
    m = re.search(r'\ {}\r?$'.format(container_name), result, flags=re.MULTILINE)
    return m is not None


def is_not_running(container_name, name_is_regex=False):
    return not is_running(container_name, name_is_regex=name_is_regex)


def has_succeeded(container_name, name_is_regex=False):
    if not name_is_regex:
        container_name = re.escape(container_name)
    result = run('docker ps -a')
    pattern = r'{status}.*{container_name}\r?$'.format(status=re.escape('Exited (0)'), container_name=container_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def has_not_succeeded(container_name, name_is_regex=False):
    return not has_succeeded(container_name, name_is_regex=name_is_regex)


def container_exists(container_name, name_is_regex=False):
    if not name_is_regex:
        container_name = re.escape(container_name)
    result = run('docker ps -a')
    pattern = r'.*{container_name}\r?$'.format(container_name=container_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def container_not_exists(container_name, name_is_regex=False):
    return not container_exists(container_name, name_is_regex=name_is_regex)


def has_succeeded_or_is_running(container_name, name_is_regex=False):
    return is_running(container_name, name_is_regex=name_is_regex) or has_succeeded(container_name, name_is_regex=name_is_regex)


def not_has_succeeded_or_is_running(container_name, name_is_regex=False):
    return not has_succeeded_or_is_running(container_name, name_is_regex=name_is_regex)


def net_exists(network_name, name_is_regex=False):
    if not name_is_regex:
        network_name = re.escape(network_name)
    result = run('docker network ls')
    pattern = r'\s+{network_name}\s+'.format(network_name=network_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def net_not_exists(network_name, name_is_regex=False):
    return not net_exists(network_name, name_is_regex=name_is_regex)


def volume_exists(volume_name, name_is_regex=False):
    if not name_is_regex:
        volume_name = re.escape(volume_name)
    result = run('docker volume ls')
    pattern = r'\b{}\r?$'.format(volume_name)
    m = re.search(pattern, result, flags=re.MULTILINE)
    return m is not None


def volume_not_exists(volume_name, name_is_regex=False):
    return volume_exists(volume_name, name_is_regex=name_is_regex)
