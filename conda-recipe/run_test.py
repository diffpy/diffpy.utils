#!/usr/bin/env python

import pathlib
import sys

sys.path.append((pathlib.Path.cwd().parent.absolute() / "src").as_posix())

import diffpy.utils.tests

assert diffpy.utils.tests.test().wasSuccessful()
