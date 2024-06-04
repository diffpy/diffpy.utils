#!/usr/bin/env python

import pathlib
import sys

import diffpy.utils.tests

sys.path.append((pathlib.Path.cwd().parent.absolute() / "src").as_posix())


assert diffpy.utils.tests.test().wasSuccessful()
