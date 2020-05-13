# -*- coding: utf-8 -*-
#

__all__ = [
    'AnsibleError',
    'AnsibleModuleArgsError'
]


class AnsibleError(Exception):
    pass


class AnsibleModuleArgsError(AnsibleError):
    pass
