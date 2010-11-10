#!/usr/bin/env python
try:
    from distutils.core import setup, Extension
    from distutils.sysconfig import get_python_inc
    from distutils.command.build_py import build_py
except ImportError:
    print "Error importing distutils (required), please insure it is installed."
    raise

try:
    import numpy
except ImportError:
    print "Error importing NumPy (required), is it not properly installed?"
    raise

from os import environ, getcwd
import os.path
import subprocess
import sys

include_dirs  = []
lib_dirs      = []
linking_flags = []
cpp_flags     = []
libs          = [
                'EXOAnalysisManager',
                'EXOUtilities',
                'EXOReconstruction',
                'EXOCalibUtilities',
                'EXOBinaryPackage'
                ]
swig_flags    = ['-c++', '-dirprot']

include_dirs.append(numpy.__path__[0])
include_dirs.append(get_python_inc(plat_specific=1))
include_dirs.append(os.path.join(getcwd(), 'src'))


exo_out_dir = environ.get('EXOOUT')
if not exo_out_dir:
    # Means that there is a tmp installation
    from getpass import getuser
    print "EXOOUT not defined, assuming the offline software and EXOBinary lives in:"
    exo_out_dir = os.path.join('/tmp', getuser(), 'exoout') 
    print "  ", exo_out_dir

include_dirs.append(os.path.join(exo_out_dir, 'include'))
lib_dirs.append(os.path.join(exo_out_dir, 'lib'))

# Get ROOT information
DEVNULL = open('/dev/null', 'wb')
if subprocess.call(['root-config', '--incdir'], stdout=DEVNULL) != 0:
    print 'ERROR calling root-config, is it in your path?'
    sys.exit(1)

include_dirs.append(subprocess.Popen(['root-config', '--incdir'],
                                     stdout=subprocess.PIPE).communicate()[0].strip())
lib_dirs.append(subprocess.Popen(['root-config', '--libdir'],
                                     stdout=subprocess.PIPE).communicate()[0].strip())

temp_root_libs = subprocess.Popen(['root-config', '--libs'],
                                   stdout=subprocess.PIPE).communicate()[0]

# Grabbing the library names from root-config
libs.extend( [ word[2:].strip() for word in temp_root_libs.split() if word[:2] == '-l' ] )

temp_root_cflags = subprocess.Popen(['root-config', '--cflags'],
                                      stdout=subprocess.PIPE).communicate()[0]

cpp_flags.extend( [ word.strip() for word in temp_root_cflags.split() if word[:2] != '-I' ] )

# We shut off MYSQL and G4.  This only matters for the interface
# exported to Python.
# If the EXOAnalysis package was compiled against those libraries
# it should still work just fine.  Sometime in the future,
# support for MYSQL and G4 will be turned on.   
defines = [('NOMYSQL', '1'),
           ('NOG4',    '1')]

swig_flags.extend(['-I' + dir for dir in include_dirs])

debug = environ.get("DISTUTILS_DEBUG")
if debug:
    print "Include directories: \n ", '\n  '.join(include_dirs)
    print "Library directories: \n ", '\n  '.join(lib_dirs)
    print "Liraries:\n "            , '\n  '.join(libs)
    print "CPP Flags:\n "           , '\n  '.join(cpp_flags)
    print "SWIG Flags:\n "          , '\n  '.join(swig_flags)

dist = setup(name         = "PyEXOAnalysis",
             version      = "0.1",
             description  = "Python bindings for the EXOAnalysis offline software package",
             author       = "Michael Marino",
             author_email = "michael.marino@ph.tum.de",
             url          = "https://github.com/mgmarino/PyEXOAnalysis",
             options      = {'build_ext':{'swig_opts': ' '.join(swig_flags)}},
             package_dir  = {'pyexo' : 'src'},
             packages     = ['pyexo'],
             #ext_package  = "PyEXOAnalysis",
             ext_modules  = [Extension('pyexo._PyEXOAnalysis',
                                      ['src/PyEXOAnalysis_interface.i'],
                                      include_dirs  = include_dirs,
                                      swig_opts     = swig_flags, 
                                      define_macros = defines,
                                      library_dirs  = lib_dirs,
                                      libraries     = libs
                                      )])

# Hack to ensure we collect PyEXOAnalysis.py into pyexo
build_py_run = build_py(dist)
build_py_run.ensure_finalized()
build_py_run.run()
