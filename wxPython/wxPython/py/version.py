"""Provides an object representing the current 'version' or 'release'
of Py as a whole.  Individual classes, such as the shell, filling and
interpreter, each have a revision property based on the CVS Revision."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: version.py,v 1.1.2.2 2003/05/03 13:20:47 PKO Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

VERSION = '0.9.2'
