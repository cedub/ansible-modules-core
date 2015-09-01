#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Christian West <west.christianj@gmail.com>
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

DOCUMENTATION = '''
---
module: repo_vars
short_description: Retrieve variables from a repository's ansible.json file
description:
  - This module allows a developer to create an ansible manifest file that 
    resides in a git repository.  The file is read in and the variables are
    made available at execution time for subsequent tasks in the playbook or
    role.
  - The file should be of type I(json).
  - Currently, the file should be called I(ansible.json) but support could be
    added to create a custom file name in the future.
  - Sample json may look like C({"primary_language": "python"}).  This would
    make the variable C(primary_language) available for use within subsequent
    plays.
version_added: 0.1
author:
  - "Christian West (@cedub)"
options:
  path:
    description:
      - Path to the variables file
    required: true
'''

EXAMPLES = '''
description: Add variables from a repo
- repo_vars: path=/opt/app_name/app_name/
  register: rv
'''


class RepoVars(object):

    class InvalidPathError(Exception):
        pass

    def __init__(self, module, **kwargs):
        self.module = module
        self.path = kwargs['path']

    def read_vars(self):
        if not self.path:
            return {}

        try:
            import os
            f = open(os.path.join(self.path, 'ansible.json'), 'r')
        except IOError:
            return {}
        try:
            return json.load(f.read())
        except ValueError:
            return {}
        f.close()


def main():
    arg_spec = dict(
        path=dict(default=None),
    )
    module = AnsibleModule(
        argument_spec=arg_spec
    )

    path = module.params['path']

    try:
        repo_vars = RepoVars(module, path=path)
    except RepoVars.InvalidPathError,e:
        module.fail_json(msg=e.message)

    return_vals = repo_vars.read_vars()

    # Always setting changed to false since the values will be set with each
    # run of the playbook.  It's decided this should just always be set to false
    # since nothing is ever actually changed.
    return_vals['changed'] = False

    module.exit_json(**return_vals)

# Import module snippets
from ansible.module_utils.basic import *
main()
