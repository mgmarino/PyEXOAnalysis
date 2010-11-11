#!/usr/bin/env python
import os
import time
import glob
import sys

list_of_numbers = [
                 401,
                 402,
                 405,
                 406,
                 412,
                 413,
                 421,
                 429,
                 459 ]

list_of_numbers = [453]
name_of_executable = "/afs/slac.stanford.edu/u/xo/mgmarino/EXOjobs/single_job_FFTW.py"
final_directory    = "/afs/slac.stanford.edu/u/xo/mgmarino/EXOData"
queue              = "xlong"
list_of_files      = [glob.glob("/nfs/slac/g/exo_data2/exo_data/data/WIPP/processed/" 
                                + str(file) + "/run*.root") for file in list_of_numbers]
list_of_files = filter(None, list_of_files)
list_of_files = [item for sublist in list_of_files for item in sublist]
for file in list_of_files:
        print "Submitting job (%s)" % file
        write_handle = os.popen("""
bsub \\
  -q %s \\
  -R rhel50\\
  %s\\
  %s\\
  %s\\
        """ % (queue, name_of_executable, final_directory, file)) 
        write_handle.close()
