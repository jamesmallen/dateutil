# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

import mypy.main
import pytest

pytestmark = pytest.mark.skipif(sys.version_info < (3, 5),
                                reason="requires python>=3.5")

@pytest.mark.parametrize('py_version', [
    '3.6',
    '3.5',
    '3.4',
    '3.3',
    '2.7',
])
def test_stubs_in_mypy(py_version):
    """
    Run mypy by stuffing arguments into sys.argv
    """
    original_argv = sys.argv
    try:
        files = []
        seen = set()
        root = 'dateutil'
        blacklist = {'test'}
        names = os.listdir(root)
        for name in names:
            full = os.path.join(root, name)
            mod, ext = os.path.splitext(name)
            if mod in seen or mod in blacklist or mod.startswith('.'):
                continue
            if ext == '.pyi':
                seen.add(mod)
                files.append(full)
            elif (os.path.isfile(os.path.join(full, '__init__.pyi')) or
                  os.path.isfile(os.path.join(full, '__init__.py'))):
                for r, ds, fs in os.walk(full):
                    ds.sort()
                    fs.sort()
                    for f in fs:
                        m, x = os.path.splitext(f)
                        if x == '.pyi':
                            fn = os.path.join(r, f)
                            seen.add(mod)
                            files.append(fn)
        assert len(files) > 0, 'No stub files found'
        flags = ['--python-version', py_version, '--strict-optional']
        sys.argv = ['mypy'] + flags + files
        print('Running', sys.argv)
        mypy.main.main('')
    finally:
        sys.argv = original_argv
