#!/usr/bin/env python3
#
# Simple test suite

import os
import sys
import unittest
import subprocess

try:
  from pathlib import Path
except ImportError:
  from pathlib2 import Path  # python2 backport

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))


def module_call(args, env=None):
    cmd = [sys.executable, '-m', '{{ cookiecutter.app_name }}']
    cmd.extend(args)
    print()
    print(" ".join(cmd))
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        env=env
    )
    stdout, stderr = p.communicate()

    return (stdout + stderr), p.returncode


class Test(unittest.TestCase):
    def test_foo(self):
        self.assertTrue(True)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
