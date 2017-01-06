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

IGNORE_STRING="freckles*"

def stow(module):

    params = module.params

    state = params['state']
    name = params['name']
    source_dir = params['source_dir']
    target_dir = params['target_dir']

    cmd = "stow -v --ignore={} -d {} -t {} -R {}".format(IGNORE_STRING, source_dir, target_dir, name)

    rc, stdout, stderr = module.run_command(cmd, check_rc=False)

    if rc == 0:
        module.exit_json(changed=True, stderr=stderr)
    else:
        module.fail_json(msg="failed to stow {}: {}".format(name, stderr))


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

    stow(module)

if __name__ == '__main__':
    main()
