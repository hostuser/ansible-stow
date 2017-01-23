#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: stow
short_description: Manage links to dotfiles
'''

import json
import os
from ansible.module_utils.basic import AnsibleModule

IGNORE_STRING="frkl"

def stow(module, stow_version):

    params = module.params

    state = params['state']
    name = params['name']
    source_dir = params['source_dir']
    target_dir = params['target_dir']

    if stow_version.startswith("1") or stow_version.startswith("2.0"):
        ignore_parameter = ""
    else:
        ignore_parameter = "--ignore={}".format(IGNORE_STRING)

    cmd = "stow -v {} -d {} -t {} -R {}".format(ignore_parameter, source_dir, target_dir, name)

    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if rc == 0:
        module.exit_json(changed=True, stderr=stderr)
    else:
        module.fail_json(msg="failed to stow ( {} ) {}: {}".format(cmd, name, stderr))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent']),
            name=dict(required=True),
            source_dir=dict(required=True),
            target_dir=dict(required=True),
            use=dict(default='stow')
        )
    )

    cmd = "stow --version"
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if rc == 0:
        stow_version = stdout.split()[-1]
        # module.exit_json(changed=True, version=stow_version)
    else:
        module.fail_json("Can't execute/find 'stow': {}".format(stderr))

    stow(module, stow_version)

if __name__ == '__main__':
    main()
