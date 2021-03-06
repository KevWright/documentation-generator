#!/usr/bin/python

# The MIT License (MIT)
#
# Copyright (c) 2013 CFEngine AS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import cfdoc_environment as environment
import cfdoc_metadata as metadata
import cfdoc_linkresolver as linkresolver
import cfdoc_macros as macros
import cfdoc_printsource as printsource
import cfdoc_git as git
import sys
import os
from time import gmtime, strftime

config = environment.validate()
config["log_file"] = config["markdown_directory"] + "/cfdoc_log.markdown"
if os.path.exists(config["log_file"]):
	os.remove(config["log_file"])
logfile = open(config["log_file"], "w")
logfile.write("---\n")
logfile.write("layout: printable\n")
logfile.write("title: \"Documentation Issues\"\n")
logfile.write("published: true\n")
logfile.write("alias: cfdoc_log.html\n")
logfile.write("---\n")
logfile.write("\n")
logfile.write("Documentation generated at %s GMT\n" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
logfile.write("\n")
logfile.write("# Logging\n")
logfile.write("\n")
logfile.close()

try:
	git.createData(config)
except:
	print "cfdoc_preprocess: Fatal error generating git tags"
	sys.stdout.write("       Exception: ")
	print sys.exc_info()
	exit(1)

try:
	metadata.run(config)
except:
	print "cfdoc_preprocess: Fatal error setting meta data"
	sys.stdout.write("       Exception: ")
	print sys.exc_info()
	exit(2)

try:
	linkresolver.run(config)
except:
	print "cfdoc_preprocess: Fatal error generating link map"
	sys.stdout.write("       Exception: ")
	print sys.exc_info()
	exit(3)

try:
	macros.run(config)
except:
	print "cfdoc_macros: Error generating documentation from syntax maps"
	sys.stdout.write("      Exception: ")
	print sys.exc_info()

# generate links to known targets
linkresolver.apply(config)

# create printable sources from completely pre-processed markdown

try:
	printsource.run(config)
except:
	print "cfdoc_printsource: Error generating print-pages"
	sys.stdout.write("      Exception: ")
	print sys.exc_info()

exit(0)
