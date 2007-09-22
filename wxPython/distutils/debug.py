import os

# This module should be kept compatible with Python 1.5.2.

__revision__ = "$Id: debug.py,v 1.1.2.2 2003/02/21 21:45:58 RD Exp $"

# If DISTUTILS_DEBUG is anything other than the empty string, we run in
# debug mode.
DEBUG = os.environ.get('DISTUTILS_DEBUG')

