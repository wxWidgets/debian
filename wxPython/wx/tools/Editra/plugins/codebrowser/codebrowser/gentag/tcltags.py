###############################################################################
# Name: tcltags.py                                                            #
# Purpose: Generate Tags for Tcl Scripts                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: tcltags.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
  Generate a DocStruct object that captures the structure of a Tcl Scripts.
Currently supports searching for Procedure definitions.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: tcltags.py 56505 2008-10-25 03:04:13Z CJP $"
__revision__ = "$Revision: 56505 $"

#--------------------------------------------------------------------------#
# Dependancies
import taglib
import parselib

#--------------------------------------------------------------------------#

def GenerateTags(buff):
    """Create a DocStruct object that represents a Tcl Script
    @param buff: a file like buffer object (StringIO)

    """
    rtags = taglib.DocStruct()
    rtags.SetElementDescription('procedure', "Procedure Definitions")

    for lnum, line in enumerate(buff):
        line = line.strip()

        # Skip comment and empty lines
        if line.startswith(u"#") or not line:
            continue

        # Check for Procedure defs
        if parselib.IsToken(line, 0, u'proc'):
            parts = line.split()
            if len(parts) > 1:
                name = parts[1]
                if u"::" in name:
                    spaces = name.split("::")
                    space_l = rtags.GetElement('namespace', spaces[0])
                    if space_l == None:
                        space_l = taglib.Namespace(spaces[0], lnum)
                        rtags.AddElement('namespace', space_l)
                    space_l.AddElement('procedure', taglib.Procedure(spaces[-1], lnum))
                else:
                    rtags.AddElement('procedure', taglib.Procedure(parts[1], lnum))

    return rtags

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
