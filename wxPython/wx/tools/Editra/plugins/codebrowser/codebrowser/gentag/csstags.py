###############################################################################
# Name: csstags.py                                                            #
# Purpose: Generate Tags for Cascading Style Sheets                           #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: csstags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Cascading Style
Sheet. Currently supports parsing of global identities and classes.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: csstags.py 53001 2008-04-04 04:08:04Z CJP $"
__revision__ = "$Revision: 53001 $"

#--------------------------------------------------------------------------#
# Dependancies
import taglib
import parselib

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents a Cascading Style Sheets
    @param buff: a file like buffer object (StringIO)
    @todo: add support for parsing selectors and grouping classes and
           identities of each selector in a subscope.

    """
    rtags = taglib.DocStruct()

    # Setup document structure
#    rtags.SetElementDescription('tag', "Selectors")
    # Use variables node for global identities
    rtags.SetElementDescription('variable', "Identities")
    # Use classes for global classes
    # Uses DocStruct builtin

    c_tag = None      # Currenly found tag
    incomment = False # Inside a comment
    indef = False     # Inside a style definition {}

    for lnum, line in enumerate(buff):
        line = line.strip()
        llen = len(line)
        idx = 0
        while idx < len(line):
            # Skip Whitespace
            idx = parselib.SkipWhitespace(line, idx)

            # Check if valid item to add to document
#            if c_tag is not None and line[idx] == u'{':
#                rtags.AddElement('tag', c_tag)
#                c_tag = None

            # Check for coments
            if llen > idx+1 and line[idx] == u'/' and line[idx+1] == u'*':
                idx += 2
                incomment = True
            elif llen > idx+1 and line[idx] == u'*' and line[idx+1] == u'/':
                idx += 2
                incomment = False

            # At end of line
            if idx >= llen:
                break

            # Look for tags
            if incomment:
                idx += 1
            elif line[idx] == u'{':
                idx += 1
                indef = True
            elif indef and line[idx] == u'}':
                idx += 1
                indef = False
            elif not indef and line[idx] in (u'.', u'#'):
                if idx == 0 or line[idx-1].isspace():
                    name = parselib.GetFirstIdentifier(line[idx+1:])
                    if name is not None:
                        name = line[idx] + name
                        if line[idx] == u'.':
                            rtags.AddClass(taglib.Class(name, lnum))
                        else:
                            rtags.AddVariable(taglib.Variable(name, lnum))
                        idx += len(name)
                idx += 1
            else:
                idx += 1

    return rtags

#-----------------------------------------------------------------------------#
# Utilities
class Tag(taglib.Scope):
    """Tag Scope Object, Tag derives from Scope so it can
    contain identities and classes

    """
    def __init__(self, name, line, scope=None):
        taglib.Scope.__init__(self, name, line, "tag", scope)

#-----------------------------------------------------------------------------#
# Test
if __name__ == '__main__':
    import sys
    import StringIO
    fhandle = open(sys.argv[1])
    txt = fhandle.read()
    fhandle.close()
    tags = GenerateTags(StringIO.StringIO(txt))
    print "\n\nElements:"
    for element in tags.GetElements():
        print "\n%s:" % element.keys()[0]
        for val in element.values()[0]:
            print "%s [%d]" % (val.GetName(), val.GetLine())
    print "END"
