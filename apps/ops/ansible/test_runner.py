# -*- coding: utf-8 -*-
#

import unittest
import sys
from django.test import TestCase
from ops.ansible.arguments import CopyArguments, GetUrlArguments

sys.path.insert(0, "../..")

from ops.ansible.runner import AdHocRunner, CommandRunner, CopyRunner, GetUrlRunner
from ops.ansible.inventory import BaseInventory


class TestAdHocRunner(unittest.TestCase):
    def setUp(self):
        host_data = [
            {
                "hostname": "testserver",
                "ip": "192.168.244.185",
                "port": 22,
                "username": "root",
                "password": "redhat",
            },
        ]
        inventory = BaseInventory(host_data)
        self.runner = AdHocRunner(inventory)

    def test_run(self):
        tasks = [
            {"action": {"module": "shell", "args": "ls"}, "name": "run_cmd"},
            {"action": {"module": "shell", "args": "whoami"}, "name": "run_whoami"},
        ]
        ret = self.runner.run(tasks, "all")
        print(ret.results_summary)
        print(ret.results_raw)


class TestCommandRunner(unittest.TestCase):
    def setUp(self):
        host_data = [
            {
                "hostname": "ebs",
                "ip": "182.92.219.104",
                "port": 3299,
                "username": "easemob",
                "private_key": '/home/shan/.ssh/id_rsa'
            },
        ]
        inventory = BaseInventory(host_data)
        self.runner = CommandRunner(inventory)

    def test_execute(self):
        res = self.runner.execute('ls', 'all')
        print(res.results_command)
        print(res.results_raw)


class TestCopyRunner(TestCase):
    def setUp(self):
        host_data = [
            {
                "hostname": "ebs",
                "ip": "182.92.219.104",
                "port": 3299,
                "username": "easemob",
                "private_key": '/home/shan/.ssh/id_rsa'
            },
        ]
        inventory = BaseInventory(host_data)
        self.runner = CopyRunner(inventory)

    def test_execute(self):
        files_args = [
            CopyArguments(src='/tmp/a', dest='/tmp/abc/', group='easemob', mode='0644'),
            CopyArguments(src='/tmp/b', dest='/tmp/abc/', group='easemob', mode='0644'),
        ]
        res = self.runner.copy(pattern='all', files_args=files_args)
        print(res.results_command)
        # print(res.results_raw)


class TestGetUrlRunner(unittest.TestCase):
    def setUp(self):
        host_data = [
            {
                "hostname": "ebs",
                "ip": "182.92.219.104",
                "port": 3299,
                "username": "easemob",
                "private_key": '/home/shan/.ssh/id_rsa'
            },
        ]
        inventory = BaseInventory(host_data)
        self.runner = GetUrlRunner(inventory)

    def test_execute(self):
        url_args = [
            GetUrlArguments(url='http://www.baidu.com', dest='/tmp/baidu', mode='0644'),
            GetUrlArguments(url='http://www.easemob.com', dest='/tmp/easemob', mode='0644'),
        ]
        res = self.runner.get(pattern='all', url_args=url_args)
        print(res.results_command)
        print(res.results_raw)


if __name__ == "__main__":
    unittest.main()
