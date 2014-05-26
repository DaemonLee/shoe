#!/usr/bin/env python2

'''
	A simple little script to convert Local Shared Objects to json than back again for easy editing.
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
#import the required jibberjabs
import sys
import json
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

if sys.argv[1].endswith(".sol"):
	solToJson(sys.argv[1])
elif sys.argv[1].endswith(".json"):
	jsonToSol(sys.argv[1])
else:
	print('Make sure the file extensions are either .json or .sol!')