#!/usr/bin/env python

import sys
import pathlib
sys.path.append((pathlib.Path.cwd().parent.absolute() / "src").as_posix())

import diffpy.utils.tests
assert diffpy.utils.tests.test().wasSuccessful()
