# -*- coding: utf-8 -*-
###############################################################################
# Name: handlers.py                                                           #
# Purpose: File Type Handlers                                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""File Type Handlers
The file type handlers are used to handle the execution of and output of the
different file types that they represent. Each handler manages its own settings
and configuration.

It is easy to extend the filetypes supported by the Launch plugin through this
interface. To add support for a new filetype simply derive a new class from the
base L{FileTypeHandler} and override any of the following methods to provide
custom functionality.

Required Overrides:
__init__ : define default command mapping and default command
__name__ : set the name of the handler, this should be the file type

Other Overrides:
GetEnvironment : Return a dictionary of environmental variables to run the
                 process within
HandleHotSpot : Action to perform when a hotspot is clicked on in the output
                buffer.
StyleText : Perform custom styling on the text as its added, line by line

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: handlers.py 59439 2009-03-08 22:43:06Z CJP $"
__revision__ = "$Revision: 59439 $"

__all__ = ['GetHandlerById', 'GetHandlerByName', 'GetState',
           'SetState', 'DEFAULT_HANDLER']

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import re

# Editra Libraries
import eclib.outbuff as outbuff
import syntax.synglob as synglob

#-----------------------------------------------------------------------------#
# Globals
DEFAULT_HANDLER = 'handler'

# Ansi escape sequence color table
# For coloring shell script output
RE_ANSI_START = re.compile(r'\[[34][0-9];01m')
RE_ANSI_FORE = re.compile('\[3[0-9]m')
RE_ANSI_BLOCK = re.compile('\[[34][0-9]m*.*?\[m')
RE_ANSI_END = re.compile(r'\[[0]{0,1}m')
RE_ANSI_ESC = re.compile('\[[0-9]+m')
ANSI = {
        ## Forground colours ##
        '[30m' : (1, '#000000'),  # Black
        '[31m' : (2, '#FF0000'),  # Red
        '[32m' : (3, '#00FF00'),  # Green
        '[33m' : (4, '#FFFF00'),  # Yellow
        '[34m' : (5, '#0000FF'),  # Blue
        '[35m' : (6, '#FF00FF'),  # Magenta
        '[36m' : (7, '#00FFFF'),  # Cyan
        '[37m' : (8, '#FFFFFF'),  # White
        #'[39m' : default

        ## Background colour ##
        '[40m' : (011, '#000000'),  # Black
        '[41m' : (012, '#FF0000'),  # Red
        '[42m' : (013, '#00FF00'),  # Green
        '[43m' : (014, '#FFFF00'),  # Yellow
        '[44m' : (015, '#0000FF'),  # Blue
        '[45m' : (016, '#FF00FF'),  # Magenta
        '[46m' : (017, '#00FFFF'),  # Cyan
        '[47m' : (020, '#FFFFFF'),  # White
        #'[49m' : default
        }

# Process Start/Exit Regular Expression
RE_PROC_SE = re.compile('>{3,3}.*' + os.linesep)

#-----------------------------------------------------------------------------#
# Public Handler Api for use outside this module
def GetHandlerById(lang_id):
    """Get a handler for the specified language id"""
    if lang_id in HANDLERS:
        return HANDLERS[lang_id]
    else:
        return HANDLERS[0]

def GetHandlerByName(name):
    """Get an output handler by name"""
    for handler in HANDLERS.values():
        if name.lower() == handler.GetName().lower():
            return handler
    else:
        return HANDLERS[0]

def GetState():
    """Get a dictionary capturing the current state of all handlers
    @return: dict { handlername : (default, [commands]) }

    """
    rdict = dict()
    for handler in HANDLERS.values():
        rdict[handler.GetName()] = (handler.GetDefault(), handler.GetCommands())
    return rdict

def SetState(state):
    """Set the state of all handlers based on a dictionary of values
    @param state: dict { handlername : (default, [(alias, command), ]) }

    """
    for ftype, vals in state.iteritems():
        handler = GetHandlerByName(ftype)
        handler.SetCommands(vals[1])
        handler.SetDefault(vals)

#-----------------------------------------------------------------------------#
# Handler Base Class and Handler implementations
#
class FileTypeHandler(object):
    """Base default Output handler all output handlers should derive from
    this class. This base class is used when an output handler is request
    but no special one exists.

    """
    def __init__(self):
        object.__init__(self)
        self.commands = dict()
        self.default = ''

    __name__ = DEFAULT_HANDLER

    def AppendCommand(self, cmd):
        """Add a command to the list of commands known to this handler
        @param cmd: Tuple of (Command alias, executable path or name)

        """
        if isinstance(cmd, tuple):
            self.commands[cmd[0]] = cmd[1]
        else:
            # Bad data
            pass

    def GetAliases(self):
        """Get the list of command aliases"""
        return sorted(self.commands.keys())

    def GetCommand(self, alias):
        """Get the command for a given alias"""
        return self.commands.get(alias, alias)

    def GetCommands(self):
        """Get the set of commands available for this file type"""
        return sorted(self.commands.items())

    def GetDefault(self):
        """Get the prefered default command
        @return: string

        """
        return self.default

    def GetEnvironment(self):
        """Get the dictionary of environmental variables to run the
        command under.

        """
        return os.environ

    def GetName(self):
        """Get the name of this handler"""
        return self.__name__

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Handle hotspot clicks. Called when a hotspot is clicked
        in an output buffer of this file type.
        @param mainw: MainWindow instance that created the launch instance
        @param outbuffer: Buffer the click took place in
        @param line: line number of the hotspot region in the buffer
        @param fname: path of the script that was run to produce the output that
                      contains the hotspot.

        """
        pass

    def FilterInput(self, text):
        """Filter incoming text return the text to be displayed
        @param text: The incoming text to filter before putting in buffer

        """
        return text

    def SetCommands(self, cmds):
        """Set the list of commands known by the handler
        @param cmds: list of command tuples

        """
        if not isinstance(cmds, list):
            raise TypeError, "SetCommands expects a list of tuples"
        else:
            sdict = dict()
            for cmd in cmds:
                if len(cmd) == 2:
                    sdict[cmd[0]] = cmd[1]

            if len(sdict.keys()):
                self.commands.clear()
                self.commands.update(sdict)

            # Reset default if it has been removed
            if self.default not in self.commands:
                keys = self.commands.keys()
                if len(keys):
                    self.default = keys[0]

    def SetDefault(self, cmd):
        """Set the prefered default command
        @param cmd: Command alias/path tuple to set as the preffered one
        @postcondition: if cmd is not in the saved command list it will be
                        added to that list.

        """
        cmd = [ cmd[0].strip(), cmd[1] ]
        if cmd[0] not in self.GetAliases():
            self.AppendCommand(cmd)
        self.default = cmd[0]

    def StyleText(self, stc, start, txt):
        """Style the text in the given buffer
        @param stc: stc based buffer to apply styling to
        @param start: start of text that was just added to buffer
        @param txt: text that was just added at start point

        """
        # Highlight Start and End lines in info style
        for info in RE_PROC_SE.finditer(txt):
            sty_s = start + info.start()
            sty_e = start + info.end()
            stc.StartStyling(sty_s, 0xff)
            stc.SetStyling(sty_e - sty_s, outbuff.OPB_STYLE_INFO)

#-----------------------------------------------------------------------------#

class AdaHandler(FileTypeHandler):
    """FileTypeHandler for Ada"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = {'gcc -c' : 'gcc -c'}
        self.default = 'gcc -c'

    __name__ = 'ada'

#-----------------------------------------------------------------------------#

class BashHandler(FileTypeHandler):
    """FileTypeHandler for Bash scripts"""
    RE_BASH_ERROR = re.compile('(.+): line ([0-9]+): .*' + os.linesep)

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(bash='bash')
        self.default = 'bash'

    __name__ = 'bash shell'

    def FilterInput(self, txt):
        """Filter out ansi escape sequences from input"""
        txt = RE_ANSI_START.sub('', txt)
        return RE_ANSI_END.sub('', txt)

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        txt = outbuffer.GetLine(line)
        match = BashHandler.RE_BASH_ERROR.findall(txt)
        ifile = None
        if len(match):
            ifile = match[0][0].split()[-1]
            try:
                line = max(int(match[0][1]) - 1, 0)
            except IndexError:
                line = 0

        # If not an absolute path then the error is in the current script
        if not os.path.isabs(ifile):
            dname = os.path.split(fname)[0]
            ifile = os.path.join(dname, ifile)

        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style NSIS output messages"""
        if _StyleError(stc, start, txt, BashHandler.RE_BASH_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(BashHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class BatchHandler(FileTypeHandler):
    """FileTypeHandler for Dos batch files"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(cmd='cmd /c')
        self.default = 'cmd'

    __name__ = 'Batch'

#-----------------------------------------------------------------------------#

class BooHandler(FileTypeHandler):
    """FileTypeHandler for Boo"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(booi='booi')
        self.default = 'booi'

    __name__ = 'boo'

#-----------------------------------------------------------------------------#

class CamlHandler(FileTypeHandler):
    """FileTypeHandler for Caml"""
    RE_CAML_ERROR = re.compile(r'File "(.+)", line (.+), characters .+:')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(ocaml='ocaml')
        self.default = 'ocaml'

    __name__ = 'Caml'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    CamlHandler.RE_CAML_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style OCaml Information and Error messages from script output."""
        if _StyleError(stc, start, txt, CamlHandler.RE_CAML_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(CamlHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class CSHHandler(FileTypeHandler):
    """FileTypeHandler for C-Shell"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(csh='csh')
        self.default = 'csh'

    __name__ = 'c shell'

#-----------------------------------------------------------------------------#

class DHandler(FileTypeHandler):
    """FileTypeHandler for D"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(dmd='dmd -run')
        self.default = 'dmd'

    __name__ = 'd'

#-----------------------------------------------------------------------------#

class FeriteHandler(FileTypeHandler):
    """FileTypeHandler for Ferite"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(ferite='ferite')
        self.default = 'ferite'

    __name__ = 'ferite'

#-----------------------------------------------------------------------------#

class HaskellHandler(FileTypeHandler):
    """FileTypeHandler for Haskell"""
    RE_HASKELL_ERROR = re.compile('(.+):(.+):[0-9]+:.+ error .+')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = {'ghc --make' : 'ghc --make'}
        self.default = 'ghc --make'

    __name__ = 'haskell'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    HaskellHandler.RE_HASKELL_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style GHC Information and Error messages from script output."""
        if _StyleError(stc, start, txt, HaskellHandler.RE_HASKELL_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(HaskellHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class HaxeHandler(FileTypeHandler):
    """FileTypeHandler for haXe"""
    RE_HAXE_ERROR = re.compile('([a-zA-Z_.]+)\(([0-9]+)\):.*')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(neko='neko', nekoc='nekoc')
        self.default = 'nekoc'

    __name__ = 'haxe'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    HaxeHandler.RE_HAXE_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style haXe output messages"""
        if _StyleError(stc, start, txt, HaxeHandler.RE_HAXE_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(HaxeHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class HTMLHandler(FileTypeHandler):
    """FileTypeHandler for HTML"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        if u'darwin' in sys.platform:
            self.commands = dict(Safari='open -a Safari.app',
                                 Camino='open -a Camino.app',
                                 Firefox='open -a Firefox.app',
                                 Opera='open -a Opera.app')
            self.default = 'Safari'
        elif sys.platform.startswith('win'):
            self.commands = dict(ie='iexplorer.exe',
                                 firefox='firefox.exe',
                                 opera='opera.exe')
            self.default = 'ie'
        else:
            self.commands = dict(firefox='firefox',
                                 opera='opera')
            self.default = 'firefox'

    __name__ = 'html'

#-----------------------------------------------------------------------------#

class InnoSetupHandler(FileTypeHandler):
    """FileTypeHandler for Inno Setup Scripts"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(iscc='iscc.exe', Compil32='Compil32.exe /cc')
        self.default = 'iscc'

    __name__ = 'inno setup script'

#-----------------------------------------------------------------------------#

class KornHandler(FileTypeHandler):
    """FileTypeHandler for Korn Shell scripts"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(ksh='ksh')
        self.default = 'ksh'

    __name__ = 'korn shell'

#-----------------------------------------------------------------------------#

class LatexHandler(FileTypeHandler):
    """FileTypeHandler for LaTex"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(latex='latex', dvips='dvips',
                             pdflatex='pdflatex', ps2pdf='ps2pdf',
                             dvipng='dvipng', latex2html='latex2html')
        self.default = 'latex'

    __name__ = 'LaTex'

#-----------------------------------------------------------------------------#

class LuaHandler(FileTypeHandler):
    """FileTypeHandler for Lua"""
    RE_LUA_ERROR = re.compile('.*: (.+):([0-9]+):.*')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(lua='lua', luac='luac')
        self.default = 'lua'

    __name__ = 'lua'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    LuaHandler.RE_LUA_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style NSIS output messages"""
        if _StyleError(stc, start, txt, LuaHandler.RE_LUA_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(LuaHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class NewLispHandler(FileTypeHandler):
    """FileTypeHandler for newLisp"""

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(newlisp='newlisp')
        self.default = 'newlisp'

    __name__ = 'newlisp'

#-----------------------------------------------------------------------------#

class NSISHandler(FileTypeHandler):
    """FileTypeHandler for NSIS scripts"""
    RE_NSIS_ERROR = re.compile(r'Error .* "(.+)" on line ([0-9]+) ')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(makensis='makensis')
        self.default = 'makensis'

    __name__ = 'nsis'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    NSISHandler.RE_NSIS_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style NSIS output messages"""
        if _StyleError(stc, start, txt, NSISHandler.RE_NSIS_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(NSISHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class PhpHandler(FileTypeHandler):
    """FileTypeHandler for Php"""
    RE_PHP_ERROR = re.compile(r'[a-zA-Z]+ error: .* in (.+) on line ([0-9]+).*')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(php='php -f')
        self.default = 'php'

    __name__ = 'php'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    PhpHandler.RE_PHP_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style php Information and Error messages from script
        output.

        """
        if _StyleError(stc, start, txt, PhpHandler.RE_PHP_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(PhpHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class PikeHandler(FileTypeHandler):
    """FileTypeHandler for Pike"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(pike='pike')
        self.default = 'pike'

    __name__ = 'pike'

#-----------------------------------------------------------------------------#

class PerlHandler(FileTypeHandler):
    """FileTypeHandler for Perl scripts"""
    RE_PERL_ERROR = re.compile(r'.+ at (.+) line ([0-9]+)[,\.].*')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(perl='perl')
        self.default = 'perl'

    __name__ = 'perl'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    PerlHandler.RE_PERL_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style perl Information and Error messages from script
        output.

        """
        if _StyleError(stc, start, txt, PerlHandler.RE_PERL_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(PerlHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class PostScriptHandler(FileTypeHandler):
    """FileTypeHandler for Post/GhostScript"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        if sys.platform.startswith('win'):
            self.commands = dict(gswin32c='gswin32c')
            self.default = 'gs2in32c'
        elif 'darwin' in sys.platform:
            self.commands = dict(pstopdf='pstopdf')
            self.default = 'pstopdf'
        else:
            self.commands = dict(gs='gs')
            self.default = 'gs'

    __name__ = 'postscript'

#-----------------------------------------------------------------------------#

class PythonHandler(FileTypeHandler):
    """FileTypeHandler for Python"""
    RE_PY_ERROR = re.compile('File "(.+)", line ([0-9]+)') # Python Exceptions
    RE_PL_ERR = re.compile(r'\s*([REWCF]):\s*([0-9]+):.*') # Pylint Output

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(python='python -u', pylint='pylint',
                             pylinterr='pylint -e')
        self.default = 'python'

    __name__ = 'python'

    def GetEnvironment(self):
        """Get the environment to run the python script in"""
        if not hasattr(sys, 'frozen') or sys.platform.startswith('win'):
            proc_env = os.environ.copy()
        else:
            proc_env = dict()

        proc_env['PYTHONUNBUFFERED'] = '1'
        return proc_env

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        match = PythonHandler.RE_PL_ERR.match(outbuffer.GetLine(line))
        if match:
            eline = max(0, int(match.group(2)) - 1)
            _OpenToLine(fname, eline, mainw)
        else:
            ifile, line = _FindFileLine(outbuffer, line, fname,
                                        PythonHandler.RE_PY_ERROR)
            _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style python Information and Error messages from script
        output.

        """
        if _StyleError(stc, start, txt, PythonHandler.RE_PY_ERROR) or \
           _StyleError(stc, start, txt, PythonHandler.RE_PL_ERR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(PythonHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class RHandler(FileTypeHandler):
    """FileTypeHandler for R"""
    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = {'r' : 'R',
                         'Rterm' : 'Rterm',
                         'Rgui' : 'Rgui',
                         'Rscript' : 'Rscript'}
        self.default = 'Rscript'

    __name__ = 'R'

#-----------------------------------------------------------------------------#

class RubyHandler(FileTypeHandler):
    """FileTypeHandler for Ruby scripts"""
    RE_RUBY_ERROR = re.compile('(.+):([0-9]+)[:]{0,1}.*')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(ruby='ruby')
        self.default = 'ruby'

    __name__ = 'ruby'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    RubyHandler.RE_RUBY_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style NSIS output messages"""
        if _StyleError(stc, start, txt, RubyHandler.RE_RUBY_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(RubyHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class TCLHandler(FileTypeHandler):
    """FileTypeHandler for TCL/TK"""
    RE_TCL_ERROR = re.compile('\(file "(.+)" line ([0-9]+)\)')

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(wish='wish')
        self.default = 'wish'

    __name__ = 'tcl/tk'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the buffer.

        """
        txt = outbuffer.GetLine(line)
        match = TCLHandler.RE_TCL_ERROR.findall(txt)
        ifile = None
        if len(match):
            ifile = match[0][0]
            try:
                line = max(int(match[0][1]) - 1, 0)
            except IndexError:
                line = 0

        # If not an absolute path then the error is in the current script
        if not os.path.isabs(ifile):
            dname = os.path.split(fname)[0]
            ifile = os.path.join(dname, ifile)

        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style NSIS output messages"""
        if _StyleError(stc, start, txt, TCLHandler.RE_TCL_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(TCLHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#

class VBScriptHandler(FileTypeHandler):
    """FileTypeHandler for VBScript"""
    RE_VBS_ERROR = re.compile('(.+)\(([0-9]+).*' + os.linesep)

    def __init__(self):
        FileTypeHandler.__init__(self)
        self.commands = dict(cscript='CSCRIPT.exe', wscript='WSCRIPT.exe')
        self.default = 'cscript'

    __name__ = 'VBScript'

    def HandleHotSpot(self, mainw, outbuffer, line, fname):
        """Hotspots are error messages, find the file/line of the
        error in question and open the file to that point in the
        buffer.

        """
        ifile, line = _FindFileLine(outbuffer, line, fname,
                                    VBScriptHandler.RE_VBS_ERROR)
        _OpenToLine(ifile, line, mainw)

    def StyleText(self, stc, start, txt):
        """Style VBScript Information and Error messages from script output."""
        if _StyleError(stc, start, txt, VBScriptHandler.RE_VBS_ERROR):
            return
        else:
            # Highlight Start end lines this is what the
            # base classes method does.
            super(VBScriptHandler, self).StyleText(stc, start, txt)

#-----------------------------------------------------------------------------#
# Handler Object Dictionary
# Create an instance of each Handler to use as a persistent object
HANDLERS = { 0                      : FileTypeHandler(), # Null Handler
            synglob.ID_LANG_ADA     : AdaHandler(),
            synglob.ID_LANG_BASH    : BashHandler(),
            synglob.ID_LANG_BATCH   : BatchHandler(),
            synglob.ID_LANG_BOO     : BooHandler(),
            synglob.ID_LANG_CAML    : CamlHandler(),
            synglob.ID_LANG_CSH     : CSHHandler(),
            synglob.ID_LANG_D       : DHandler(),
            synglob.ID_LANG_FERITE  : FeriteHandler(),
            synglob.ID_LANG_KSH     : KornHandler(),
            synglob.ID_LANG_HASKELL : HaskellHandler(),
            synglob.ID_LANG_HAXE    : HaxeHandler(),
            synglob.ID_LANG_HTML    : HTMLHandler(),
            synglob.ID_LANG_INNO    : InnoSetupHandler(),
            synglob.ID_LANG_LATEX   : LatexHandler(),
            synglob.ID_LANG_LUA     : LuaHandler(),
            synglob.ID_LANG_NEWLISP : NewLispHandler(),
            synglob.ID_LANG_NSIS    : NSISHandler(),
            synglob.ID_LANG_PERL    : PerlHandler(),
            synglob.ID_LANG_PHP     : PhpHandler(),
            synglob.ID_LANG_PIKE    : PikeHandler(),
            synglob.ID_LANG_PS      : PostScriptHandler(),
            synglob.ID_LANG_PYTHON  : PythonHandler(),
            synglob.ID_LANG_R       : RHandler(),
            synglob.ID_LANG_RUBY    : RubyHandler(),
            synglob.ID_LANG_TEX     : LatexHandler(),
            synglob.ID_LANG_TCL     : TCLHandler(),
            synglob.ID_LANG_VBSCRIPT : VBScriptHandler() }

#-----------------------------------------------------------------------------#
# Local utility functions

def _FindFileLine(outbuffer, line, fname, regex):
    """Find and return the filename and line number found by applying
    the given regular expression to the text found in the line of the
    given buffer.
    @param outbuffer: OutputBuffer instance
    @param line: in the buffer
    @param fname: Filname that generated the error message
    @param regex: a regular exression with two groups the first group needs to
                  match the filename. The second group needs to match the line
                  number that the error is reporting

    """
    match = regex.findall(outbuffer.GetLine(line))
    ifile = None
    if len(match):
        ifile = match[0][0]
        try:
            line = max(int(match[0][1]) - 1, 0)
        except (IndexError, TypeError):
            line = 0

    # If not an absolute path then the error is relative to the
    # script that produced this error message.
    if not os.path.isabs(ifile):
        dname = os.path.split(fname)[0]
        ifile = os.path.join(dname, ifile)

    return (ifile, line)

def _OpenToLine(fname, line, mainw):
    """Open the given filename to the given line number
    @param fname: File name to open, relative paths will be converted to abs
                  paths.
    @param line: Line number to set the cursor to after opening the file
    @param mainw: MainWindow instance to open the file in

    """
    nbook = mainw.GetNotebook()
    buffers = [ page.GetFileName() for page in nbook.GetTextControls() ]
    if fname in buffers:
        page = buffers.index(fname)
        nbook.ChangePage(page)
        nbook.GetPage(page).GotoLine(line)
    else:
        nbook.OnDrop([fname])
        nbook.GetPage(nbook.GetSelection()).GotoLine(line)

def _StyleError(stc, start, txt, regex):
    """Style Error message groups
    @param stc: outputbuffer reference
    @param start: start of text just added to buffer
    @param txt: text that was just added
    @param regex: regular expression object for matching the errors
    @return: bool (True if match), (False if no match)

    """
    for group in regex.finditer(txt):
        sty_s = start + group.start()
        sty_e = start + group.end()
        stc.StartStyling(sty_s, 0xff)
        stc.SetStyling(sty_e - sty_s, outbuff.OPB_STYLE_ERROR)
    else:
        return False

    return True
