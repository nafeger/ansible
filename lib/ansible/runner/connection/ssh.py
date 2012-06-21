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

################################################

import os
import time
import subprocess
import shlex
import pipes
import random
import select
import fcntl

from ansible import errors

class SSHConnection(object):
    ''' ssh based connections '''

    def __init__(self, runner, host, port):
        self.runner = runner
        self.host = host
        self.port = port

    def connect(self):
        ''' connect to the remote host '''

        self.common_args = ["-o", "StrictHostKeyChecking=no"]
        if self.port is not None:
            self.common_args += ["-o", "Port=%d" % (self.port)]
        if self.runner.private_key_file is not None:
            self.common_args += ["-o", "IdentityFile="+self.runner.private_key_file]
        extra_args = os.getenv("ANSIBLE_SSH_ARGS", None)
        if extra_args is not None:
            self.common_args += shlex.split(extra_args)
        self.userhost = "%s@%s" % (self.runner.remote_user, self.host)

        return self

    def exec_command(self, cmd, tmp_path,sudo_user,sudoable=False):
        ''' run a command on the remote host '''

        ssh_cmd = ["ssh", "-tt"] + self.common_args + [self.userhost]
        if self.runner.sudo and sudoable:
            # Rather than detect if sudo wants a password this time, -k makes 
            # sudo always ask for a password if one is required. The "--"
            # tells sudo that this is the end of sudo options and the command
            # follows.  Passing a quoted compound command to sudo (or sudo -s)
            # directly doesn't work, so we shellquote it with pipes.quote() 
            # and pass the quoted string to the user's shell.  We loop reading
            # output until we see the randomly-generated sudo prompt set with
            # the -p option.
            randbits = ''.join(chr(random.randint(ord('a'), ord('z'))) for x in xrange(32))
            prompt = '[sudo via ansible, key=%s] password: ' % randbits
            sudocmd = 'sudo -k && sudo -p "%s" -u %s -- "$SHELL" -c %s' % (
                prompt, sudo_user, pipes.quote(cmd))
            sudo_output = ''
            ssh_cmd.append(sudocmd)
            p = subprocess.Popen(ssh_cmd, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if self.runner.sudo_pass:
                fcntl.fcntl(p.stdout, fcntl.F_SETFL,
                            fcntl.fcntl(p.stdout, fcntl.F_GETFL) | os.O_NONBLOCK)
                while not sudo_output.endswith(prompt):
                    rfd, wfd, efd = select.select([p.stdout], [],
                                                  [p.stdout], self.runner.timeout)
                    if p.stdout in rfd:
                        chunk = p.stdout.read()
                        if not chunk:
                            raise errors.AnsibleError('ssh connection closed waiting for sudo password prompt')
                        sudo_output += chunk
                    else:
                        (stdout, stderr) = p.communicate()
                        raise errors.AnsibleError('ssh connection error waiting for sudo password prompt')
                p.stdin.write(self.runner.sudo_pass + '\n')
                fcntl.fcntl(p.stdout, fcntl.F_SETFL, fcntl.fcntl(p.stdout, fcntl.F_GETFL) & ~os.O_NONBLOCK)
        else:
            ssh_cmd.append(cmd)
            p = subprocess.Popen(ssh_cmd, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return (p.stdin, p.stdout, '')

    def put_file(self, in_path, out_path):
        ''' transfer a file from local to remote '''
        if not os.path.exists(in_path):
            raise errors.AnsibleFileNotFound("file or module does not exist: %s" % in_path)
        sftp_cmd = ["sftp"] + self.common_args + [self.userhost]
        p = subprocess.Popen(sftp_cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate("put %s %s\n" % (in_path, out_path))
        if p.returncode != 0:
            raise errors.AnsibleError("failed to transfer file to %s:\n%s\n%s" % (out_path, stdout, stderr))

    def fetch_file(self, in_path, out_path):
        ''' fetch a file from remote to local '''
        if not os.path.exists(in_path):
            raise errors.AnsibleFileNotFound("file or module does not exist: %s" % in_path)
        sftp_cmd = ["sftp"] + self.common_args + [self.userhost]
        p = subprocess.Popen(sftp_cmd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate("get %s %s\n" % (in_path, out_path))
        if p.returncode != 0:
            raise errors.AnsibleError("failed to transfer file from %s:\n%s\n%s" % (in_path, stdout, stderr))

    def close(self):
        ''' terminate the connection '''
        pass
