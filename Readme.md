# OSMaxx generic docker deployment

## Prerequisites

Server with:

- Docker
- python-virtualenv

## Testing

### Local-Machine-Setup

For testing the deployment logic, we let a Vagrant box stand in for the target server. Other methods should work as well, as long as you have a working machine with SSH access to.

Build the image:

`vagrant up`

Add the vagrant config file to your ssh-config:

`vagrant ssh-config >> ~/.ssh/config`

Try to connect to the created machine:

`ssh osmaxx-local-testing-server`

If all went well, just continue.

### Execute the test-suite

make tests

## Pip-Tools

### Installation

### prerequisites

`pip-tools` in a python 2(.7) virtualenv.

### Upgrading dependencies

`pip-compile` which is the same as `pip-compile --output-file requirements.txt requirements.in`,
followed by `pip-sync`.
