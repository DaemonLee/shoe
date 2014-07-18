#!/usr/bin/env python2

"""
    shoe - A simple little script to convert Local Shared Objects to json then back again for easy editing.
    Copyright (C) 2014  Daemon Lee Schmidt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import __future__
import os
import platform
import mimetypes
import json
import argparse

from pyamf import sol
import subprocess


class insole:
    def __init__(self, strictencoding=False, encodingversion=3):
        """
            The main class that does all the encoding and decoding of the sol and json files.
            As well as handling spawning editors.
        """
        self.encodingversion = encodingversion
        self.strictencoding = strictencoding

    def tojson(self, infile):
        """Open a Local Shared Object, convert it to a json, dump it to a file."""
        open(infile, 'rb')
        lso = sol.load(infile)

        with open(infile[:-4] + '.json', 'w') as outfile:
            json.dump(lso, outfile, indent=4, separators=(',', ': '))

    def tosol(self, infile):
        """Open a json file, insert it into a sol, save sol."""
        lso = sol.SOL(infile[:-5])
        injson = json.load(open(infile, 'r'))

        for keys in injson.keys():
            lso[keys] = injson[keys]

        # TODO add "strict" support
        if self.strictencoding:
            print("Strict encoding is not implemented yet!")

        sol.save(lso, infile[:-5] + '.sol', encoding=self.encodingversion)

    def spawneditor(self, infile):  # TODO Finish writing "spawneditor" for at least Linux
        self.tojson(infile)

        theplatform = platform.system()

        if theplatform == 'Windows':
            print('TODO Windows stuff')  # TODO Windows stuff
            self.tosol(infile[:-4] + '.json')
        elif theplatform == 'Darwin':
            print('TODO Mac Stuff')  # TODO Mac stuff
            self.tosol(infile[:-4] + '.json')
        else:
            if os.getenv('DISPLAY', False):
                subprocess.call(['xdg-open', infile[:-3] + 'json'])  # TODO Fix this by making it blocking
                self.tosol(infile[:-4] + '.json')
            elif os.getenv('EDITOR', False):
                subprocess.call([os.environ["EDITOR"], infile[:-3] + 'json'])
                self.tosol(infile[:-4] + '.json')
            else:
                print("Your default $EDITOR environment variable isn't setup!")


# shoe itself

# Parser related things
parser = argparse.ArgumentParser(
    description="A simple little script to convert Local Shared Objects to json then back again for easy editing.")
parser.add_argument("infile", help="a .sol or .json file for converting")
parser.add_argument("-s", "--strict", action="store_true", help="Enable strict mode for extra standards following")
parser.add_argument("-0", "--amf0", action="store_const", help="enable AMF0 legacy encoding", const=0, default=3)
parser.add_argument("-e", "--edit", action="store_true", help="open up a editor after converting, then convert back")

args = parser.parse_args()

# Create the shoe
shoe = insole(args.strict, args.amf0)

# The science

#spawn editor or convert to json
if args.infile.endswith(".sol"):
    if args.edit:
        shoe.spawneditor(args.infile)
    else:
        shoe.tojson(args.infile)
elif mimetypes.guess_type(args.infile) == ('application/json', None):
    shoe.tosol(args.infile)
else:
    print("Something terrible happened! Most likely with the mimetype or extension of the file you put in!")