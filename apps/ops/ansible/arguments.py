# -*- coding: utf-8 -*-

__all__ = ['CopyArguments']


class CopyArguments:
    def __init__(self, src, dest, mode, group):
        self.src = src
        self.dest = dest
        self.mode = mode
        self.group = group


class GetUrlArguments:
    def __init__(self, url, dest, mode, username='', password=''):
        self.url = url
        self.dest = dest
        self.mode = mode
        self.username = username
        self.password = password
