#!/usr/bin/env python

"""utils - small shared utilities for other diffpy packages

Packages:   diffpy.utils
"""

from setuptools import setup, find_packages

# define distribution
setup(
        name = "diffpy.utils",
        version = "0.1",
        namespace_packages = ['diffpy'],
        packages = find_packages(),
        test_suite = 'diffpy.utils.tests',
        author = 'Simon J.L. Billinge',
        author_email = 'sb2896@columbia.edu',
        maintainer = 'Pavol Juhas',
        maintainer_email = 'pj2192@columbia.edu',
        url = 'http://www.diffpy.org/',
        download_url = 'http://www.diffpy.org/packages/',
        description = "Utilities for diffpy",
        license = 'BSD',
        keywords = "diffpy utilities",
        classifiers = [
            # List of possible values at
            # http://pypi.python.org/pypi?:action=list_classifiers
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.5',
            'Topic :: Scientific/Engineering :: Physics',
        ],
)

# End of file
