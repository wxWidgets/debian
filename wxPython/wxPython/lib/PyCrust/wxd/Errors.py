"""Decorator classes for documentation and shell scripting.
"""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: Errors.py,v 1.1.2.1 2003/03/11 19:37:13 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]


# These are not the real wxPython classes. These are Python versions
# for documentation purposes. They are also used to apply docstrings
# to the real wxPython classes, which are SWIG-generated wrappers for
# C-language classes.


class PyAssertionError(AssertionError):
    """"""
    pass


class PyDeadObjectError(AttributeError):
    """Instances of wx objects that are OOR capable will have their
    __class__ attribute changed to a _wxPyDeadObject class when the
    C++ object is deleted.  Subsequent attempts to access object
    attributes will raise this error, rather than segfault."""
    pass
