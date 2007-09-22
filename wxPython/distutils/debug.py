import os

# This module should be kept compatible with Python 1.5.2.

__revision__ = "$Id: debug.py,v 1.1.2.1 2003/01/21 22:14:33 RD Exp $"

# If DISTUTILS_DEBUG is anything other than the empty string, we run in
# debug mode.
DEBUG = os.environ.get('DISTUTILS_DEBUG')

