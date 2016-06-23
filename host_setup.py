from fabric.contrib import files

from fabric.api import run

VIRTUALENV_EXECUTABLE_PATH = 'osmaxx-deploy/bin'
DOCKER_COMPOSE_EXECUTABLE = VIRTUALENV_EXECUTABLE_PATH + '/docker-compose'
PYTHON_EXECUTABLE = VIRTUALENV_EXECUTABLE_PATH + '/python'
PIP_PATH = VIRTUALENV_EXECUTABLE_PATH + '/pip'
COMPOSE_VERSION = '">=1.7.1,<1.8"'


def provide_virtualenv():
    virtualenv_create = 'virtualenv osmaxx-deploy'
    if not files.exists(PYTHON_EXECUTABLE):
        run(virtualenv_create)


def provide_docker_compose():
    provide_virtualenv()
    install_compose = '{pip} install docker-compose{COMPOSE_VERSION}'.format(pip=PIP_PATH, COMPOSE_VERSION=COMPOSE_VERSION)
    if not files.exists(DOCKER_COMPOSE_EXECUTABLE):
        run(install_compose)
    assert files.exists(DOCKER_COMPOSE_EXECUTABLE)


def mkdir(directory):
    run("mkdir -p {}".format(directory))
