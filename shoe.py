#!/usr/bin/env python2

'''
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
'''

'''import the required jibberjabs'''
import mimetypes
import json
import argparse
from pyamf import sol
import __future__

def solToJson(infile):
	'''Open a Local Shared Object, convert it to a json, dump it to a file.'''
	open(infile, 'rb')
	lso = sol.load(infile)

	with open(infile[:-4] + '.json', 'w') as outfile:
		json.dump(lso, outfile, indent=4, separators=(',', ': '))


def jsonToSol(infile, AMFversion = 3):
	'''Open a json file, insert it into a sol, save sol.'''
	lso = sol.SOL(infile[:-5])
	injson = json.load(open(infile, 'r'))

	for keys in injson.keys():
		lso[keys] = injson[keys]

	sol.save(lso, infile[:-5] + '.sol', encoding=AMFversion)

'''shoe itself'''

'''Parser related things'''
parser = argparse.ArgumentParser(description="A simple little script to convert Local Shared Objects to json then back again for easy editing.")
amfEncoding = parser.add_mutually_exclusive_group()
parser.add_argument("infile", help="a .sol or .json file for converting")
amfEncoding.add_argument("-3", "--amf3", action="store_true", help="enable AMF3 encoding (default)")
amfEncoding.add_argument("-0", "--amf0", action="store_true", help="enable AMF0 encoding")

args = parser.parse_args()

'''The science'''
if args.infile.endswith(".sol"):
	solToJson(args.infile)
elif args.amf3 and mimetypes.guess_type(args.infile) == ('application/json', None):
	jsonToSol(args.infile, 3)
elif args.amf0 and mimetypes.guess_type(args.infile) == ('application/json', None):
	jsonToSol(args.infile, 0)
elif mimetypes.guess_type(args.infile) == ('application/json', None):
	jsonToSol(args.infile, 3)
else:
	print("Something terrble happened! Most likely with the mimetype or extension of the file you put in!")