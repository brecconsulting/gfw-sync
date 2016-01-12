#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
# enable debugging

import sys

if len(sys.argv) > 2:
	print "Content-Type: text/html"
	print
	print '<html><head><meta http-equiv="refresh" content="0; url=http://gfw2-data.s3.amazonaws.com/forest_use/logging/zip/gfw_logging.zip" /></head><body></body></html>'

	#print '{"name": "%s"}' % sys.argv[2]
else: 
	print "Content-Type: application/json"
	print
	print '{"error": "no argument given"}'

 



