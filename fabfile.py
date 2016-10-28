from __future__ import print_function

from fabric.api import env, run

import osm_aux_db
import osmaxx

from host_setup import provide_docker_compose

env.use_ssh_config = True

OSMAXX_COMPONENT = osmaxx.__name__

ALL_COMPONENTS = {
    OSMAXX_COMPONENT: osmaxx,
}


class Action(object):
    def __init__(self, action, default_components):
        self.action = action
        self.default_components = default_components

    def perform(self, on_components):
        if isinstance(on_components, basestring):
            on_components = set(on_components.split(";"))
        assert on_components.issubset(ALL_COMPONENTS.keys())
        for component in on_components:
            component_environment = {}

            exec_string = "executing {} on {}".format(self.action, component)
            print("")
            print(exec_string)
            print("=" * len(exec_string))

            module = ALL_COMPONENTS[component]
            if hasattr(module, 'ENVIRONMENT'):
                component_environment = module.ENVIRONMENT

            for command in getattr(module, self.action):
                command.execute(project=component, hostname=env.host_string, environment=component_environment)
            print('*' * 40)

    def __call__(self, on_components=None):
        if on_components is None:
            on_components = self.default_components
        self.perform(on_components)

health_check = Action('health_check', default_components=set(ALL_COMPONENTS))
logs = Action('logs', default_components=set(ALL_COMPONENTS))
_pre_start = Action('pre_start', default_components=set(ALL_COMPONENTS))
_actual_start = Action('start', default_components=set(ALL_COMPONENTS))
_stop = Action('stop', default_components=set(ALL_COMPONENTS))
_change = Action('change', default_components=set(ALL_COMPONENTS))


def prepare_host():
    provide_docker_compose()


def start(on_components=set(ALL_COMPONENTS)):
    _pre_start(on_components=on_components)
    _actual_start(on_components=on_components)
    health_check(on_components=on_components)


def upgrade(on_components=OSMAXX_COMPONENT):
    _change(on_components=on_components)
    health_check(on_components=on_components)


def stop(on_components=set(ALL_COMPONENTS)):
    _stop(on_components=on_components)
    health_check(on_components=on_components)


def execute_command(command):
    run(command)


def host_type():
    run('uname -s')
