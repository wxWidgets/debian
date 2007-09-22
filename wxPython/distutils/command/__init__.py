"""distutils.command

Package containing implementation of all the standard Distutils
commands."""

# This module should be kept compatible with Python 1.5.2.

__revision__ = "$Id: __init__.py,v 1.1.2.2 2003/02/21 21:45:53 RD Exp $"

__all__ = ['build',
           'build_py',
           'build_ext',
           'build_clib',
           'build_scripts',
           'clean',
           'install',
           'install_lib',
           'install_headers',
           'install_scripts',
           'install_data',
           'sdist',
           'bdist',
           'bdist_dumb',
           'bdist_rpm',
           'bdist_wininst',
           # These two are reserved for future use:
           #'bdist_sdux',
           #'bdist_pkgtool',
           # Note:
           # bdist_packager is not included because it only provides
           # an abstract base class
          ]