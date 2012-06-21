# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

import os


DEFAULT_HOST_LIST      = os.environ.get('ANSIBLE_HOSTS',
    '/etc/ansible/hosts')
DEFAULT_MODULE_PATH    = os.environ.get('ANSIBLE_LIBRARY',
    '/usr/share/ansible')
DEFAULT_REMOTE_TMP     = os.environ.get('ANSIBLE_REMOTE_TMP', 
    '/$HOME/.ansible/tmp')

DEFAULT_MODULE_NAME    = 'command'
DEFAULT_PATTERN        = '*'
DEFAULT_FORKS          = os.environ.get('ANSIBLE_FORKS',5)
DEFAULT_MODULE_ARGS    = os.environ.get('ANSIBLE_MODULE_ARGS','')
DEFAULT_TIMEOUT        = os.environ.get('ANSIBLE_TIMEOUT',10)
DEFAULT_POLL_INTERVAL  = os.environ.get('ANSIBLE_POLL_INTERVAL',15)
DEFAULT_REMOTE_USER    = os.environ.get('ANSIBLE_REMOTE_USER','root')
DEFAULT_REMOTE_PASS    = None
DEFAULT_PRIVATE_KEY_FILE    = os.environ.get('ANSIBLE_REMOTE_USER',None)
DEFAULT_SUDO_PASS      = None
DEFAULT_SUDO_USER      = os.environ.get('ANSIBLE_SUDO_USER','root')
DEFAULT_REMOTE_PORT    = 22
DEFAULT_TRANSPORT      = os.environ.get('ANSIBLE_TRANSPORT','paramiko')
DEFAULT_TRANSPORT_OPTS = ['local', 'paramiko', 'ssh']

