#!/usr/bin/python

## func command line interface & client lib
##
## Copyright 2007,2008 Red Hat, Inc
## +AUTHORS
##
## This software may be freely redistributed under the terms of the GNU
## general public license.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import sys


import command
import func.module_loader as module_loader

from func.overlord import client,base_command

class FuncCommandLine(command.Command):

    name = "func"
    usage = "func [--options] \"hostname glob\" module method [arg1] [arg2] ... "

    subCommandClasses = []

    def __init__(self):
        modules = module_loader.load_modules('func/overlord/cmd_modules/', base_command.BaseCommand)
        for x in modules.keys():
           self.subCommandClasses.append(modules[x].__class__)
        command.Command.__init__(self)

    def do(self, args):
        pass

    def addOptions(self):
        self.parser.add_option('', '--version', action="store_true",
            help="show version information")

    # just some ugly goo to try to guess if arg[1] is hostnamegoo or
    # a command name
    def _isGlob(self, str):
        if str.find("*") or str.find("?") or str.find("[") or str.find("]"):
            return True
        return False
        
    def handleArguments(self, args):
        if len(args) < 2:
            sys.stderr.write("see the func manpage for usage\n")
            sys.exit(411)
        minion_string = args[0]
        # try to be clever about this for now
        if client.is_minion(minion_string) or self._isGlob(minion_string):
            self.server_spec = minion_string
            args.pop(0)
        # if it doesn't look like server, assume it
        # is a sub command? that seems wrong, what about
        # typo's and such? How to catch that? -akl
        # maybe a class variable self.data on Command?

    def handleOptions(self, options):
        if options.version:
            #FIXME
            sys.stderr.write("version is NOT IMPLEMENTED YET\n")
