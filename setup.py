#!/usr/bin/env python

"""utils - small shared utilities for other diffpy packages

Packages:   diffpy.utils
"""

import os
import re
import sys
from setuptools import setup, find_packages

# Use this version when git data are not available, like in git zip archive.
# Update when tagging a new release.
FALLBACK_VERSION = '3.2.4'

# versioncfgfile holds version data for git commit hash and date.
# It must reside in the same directory as version.py.
MYDIR = os.path.dirname(os.path.abspath(__file__))
versioncfgfile = os.path.join(MYDIR, 'src/diffpy/utils/version.cfg')
gitarchivecfgfile = os.path.join(MYDIR, '.gitarchive.cfg')

# determine if we run with Python 3.
PY3 = (sys.version_info[0] == 3)


def gitinfo():
    from subprocess import Popen, PIPE
    kw = dict(stdout=PIPE, cwd=MYDIR, universal_newlines=True)
    proc = Popen(['git', 'describe', '--tags', '--match=[v,V,[:digit:]]*'], **kw)
    desc = proc.stdout.read()
    proc = Popen(['git', 'log', '-1', '--format=%H %ct %ci'], **kw)
    glog = proc.stdout.read()
    rv = {}
    rv['version'] = '.post'.join(desc.strip().split('-')[:2]).lstrip('v').lstrip('V')
    rv['commit'], rv['timestamp'], rv['date'] = glog.strip().split(None, 2)
    return rv


def getversioncfg():
    if PY3:
        from configparser import RawConfigParser
    else:
        from ConfigParser import RawConfigParser
    vd0 = dict(version=FALLBACK_VERSION, commit='', date='', timestamp=0)
    # first fetch data from gitarchivecfgfile, ignore if it is unexpanded
    g = vd0.copy()
    cp0 = RawConfigParser(vd0)
    cp0.read(gitarchivecfgfile)
    if len(cp0.get('DEFAULT', 'commit')) > 20:
        g = cp0.defaults()
        mx = re.search(r'\btag: [vV]?(\d[^,]*)', g.pop('refnames'))
        if mx:
            g['version'] = mx.group(1)
    # then try to obtain version data from git.
    gitdir = os.path.join(MYDIR, '.git')
    if os.path.exists(gitdir) or 'GIT_DIR' in os.environ:
        print(g['version'])
        try:
            g = gitinfo()
        except OSError:
            pass
    print(g['version'])
    # finally, check and update the active version file
    cp = RawConfigParser()
    cp.read(versioncfgfile)
    print(cp.defaults(), g['version'])
    d = cp.defaults()
    rewrite = not d or (g['commit'] and (
        g['version'] != d.get('version') or g['commit'] != d.get('commit')))
    if rewrite:
        cp.set('DEFAULT', 'version', g['version'])
        cp.set('DEFAULT', 'commit', g['commit'])
        cp.set('DEFAULT', 'date', g['date'])
        cp.set('DEFAULT', 'timestamp', g['timestamp'])
        with open(versioncfgfile, 'w') as fp:
            cp.write(fp)
    return cp

versiondata = getversioncfg()

with open(os.path.join(MYDIR, 'README.rst')) as fp:
    long_description = fp.read()

# define distribution
setup_args = dict(
    name = "diffpy.utils",
    version = versiondata.get('DEFAULT', 'version'),
    # version = '3.2.4',
    packages = find_packages(os.path.join(MYDIR, 'src')),
    package_dir = {'' : 'src'},
    test_suite = 'diffpy.utils.tests',
    include_package_data = True,
    zip_safe = False,
    author = 'Simon J.L. Billinge group',
    author_email = 'sb2896@columbia.edu',
    maintainer = 'Simon J.L. Billinge group',
    maintainer_email = 'sb2896@columbia.edu',
    description = "Shared utilities for diffpy packages.",
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    license = 'BSD-style license',
    url = "https://github.com/diffpy/diffpy.utils/",
    keywords = "text data parsers wx grid",
    classifiers = [
        # List of possible values at
        # http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)

# End of file
