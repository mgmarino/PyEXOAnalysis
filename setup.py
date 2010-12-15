#!/usr/bin/env python
try:
    from distutils.core import setup, Extension
    from distutils.sysconfig import get_python_inc
    from distutils.command.build_py import build_py
    from distutils.command.build_ext import build_ext
    from distutils.command.build import build
    from distutils.command.clean import clean
    from distutils import log
    from distutils.errors import *
except ImportError:
    log.error("Error importing distutils (required), please insure it is installed.")
    raise

try:
    import numpy
except ImportError:
    log.error( "Error importing NumPy (required), is it not properly installed?")
    raise

from os import environ, getcwd
import os.path
import subprocess
import sys

required_swig_version = (1, 3, 36)
base_name = "PyEXOAnalysis"
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
swig_flags    = ['-c++', '-dirprot', '-Wall']

include_dirs.append(numpy.__path__[0])
include_dirs.append(get_python_inc(plat_specific=1))
include_dirs.append(os.path.join(getcwd(), 'src'))


exo_out_dir = environ.get('EXOLIB')
if not exo_out_dir:
    # Means that there is a tmp installation
    from getpass import getuser
    exo_out_dir = os.path.join('/tmp', getuser(), 'exoout') 
    log.warn( """
EXOOUT not defined, assuming the offline software and EXOBinary lives in:
  %s
""" % exo_out_dir)


# We check MYSQL and G4.  This only matters for the interface
# exported to Python.
# If the EXOAnalysis package was compiled against those libraries
# it should still work just fine.  Sometime in the future,
# support for MYSQL and G4 will be turned on.   


defines = []

compile_with_mysql = environ.get('MYSQL')
if compile_with_mysql:
    libs.append('EXODBUtilities')
else:
    defines.append(('NOMYSQL', '1'))

no_compile_with_geant4 = environ.get('NOG4')
if not no_compile_with_geant4:
    libs.append('EXOSim')
else:
    defines.append(('NOG4', '1'))


include_dirs.append(os.path.join(exo_out_dir, 'include'))
lib_dirs.append(os.path.join(exo_out_dir, 'lib'))

# Get ROOT information
DEVNULL = open('/dev/null', 'wb')
if subprocess.call(['root-config', '--incdir'], stdout=DEVNULL) != 0:
    log.error('ERROR calling root-config, is it in your path?')

include_dirs.append(subprocess.Popen(['root-config', '--incdir'],
                                     stdout=subprocess.PIPE).communicate()[0].strip())
#lib_dirs.append(subprocess.Popen(['root-config', '--libdir'],
#                                     stdout=subprocess.PIPE).communicate()[0].strip())

#temp_root_libs = subprocess.Popen(['root-config', '--libs'],
#                                   stdout=subprocess.PIPE).communicate()[0]

# Grabbing the library names from root-config
#libs.extend( [ word[2:].strip() for word in temp_root_libs.split() if word[:2] == '-l' ] )

#temp_root_cflags = subprocess.Popen(['root-config', '--cflags'],
#                                      stdout=subprocess.PIPE).communicate()[0]

#cpp_flags.extend( [ word.strip() for word in temp_root_cflags.split() if word[:2] != '-I' ] )

swig_flags.extend(['-I' + dir for dir in include_dirs])

log.debug("Include directories: \n ", '\n  '.join(include_dirs))
log.debug("Library directories: \n ", '\n  '.join(lib_dirs))
log.debug("Liraries:\n "            , '\n  '.join(libs))
log.debug("CPP Flags:\n "           , '\n  '.join(cpp_flags))
log.debug("SWIG Flags:\n "          , '\n  '.join(swig_flags))


class PyEXO_build_ext(build_ext):
    def swig_sources( self, sources, ext ):
        import re
        # Make sure we have an appropriate version of
        # SWIG
        log.info( "Checking for swig version >= %i.%i.%i ..." % required_swig_version )
        swig = self.swig or self.find_swig()
        temp_swig_out = subprocess.Popen([swig, '-version'],
                                          stdout=subprocess.PIPE).communicate()[0]
        temp_swig_out = re.search(".*SWIG Version ([\.0-9]*).*", temp_swig_out).group(1)
        swig_version = tuple([int(num) for num in temp_swig_out.split('.')])
        if swig_version >= required_swig_version:
            log.info("yes")
        else:
            log.info("no")
            log.error("""
  Suggested SWIG version not found (version %i.%i.%i found).  
  This will result in python bindings with reduced funcationalities,
  in particular the inability to access protected class members in
  derived python classes. If this functionality is not needed,
  then ignore this message. 

  One can point the setup to an appropriate swig using 
  the build_ext option '--swig'.  For example, type both 
  
 >python setup.py build_ext --swig=/path/to/swig 
 >python setup.py build
  
  *NOTE*: This warning is expected on SLAC machines as the distributed
  swig version is less than required.  Please try running the  
  command first:

 >python setup.py build_ext --swig=/u/xo/mgmarino/software/bin/swig

  which should use the correct swig. 
  
  As always, be sure to test the installation with

 >python test.py

  after completion!
                  """ % swig_version)
        return build_ext.swig_sources(self, sources, ext)

class PyEXO_build(build):
    sub_commands = [('build_ext',     build.has_ext_modules),
                    ('build_py',      build.has_pure_modules),
                    ('build_clib',    build.has_c_libraries),
                    ('build_scripts', build.has_scripts),
                   ]

class PyEXO_clean(clean):
    def run( self ):
        clean.run( self )
        if self.all: 
            # also trash the swig wrappers
            for afile in ['src/' + base_name + '.py',
                          'src/' + base_name + '_interface_wrap.cpp',
                          'src/' + base_name + '_interface_wrap.h',]:
                if not os.path.exists(afile): continue
                os.remove(afile)
                log.info("removing '%s'", afile)


dist = setup(name         = base_name,
             version      = "0.1",
             description  = "Python bindings for the EXOAnalysis offline software package",
             author       = "Michael Marino",
             author_email = "michael.marino@ph.tum.de",
             url          = "https://github.com/mgmarino/PyEXOAnalysis",
             options      = {'build_ext':{'swig_opts': ' '.join(swig_flags)}},
             package_dir  = {'pyexo' : 'src'},
             packages     = ['pyexo'],
             cmdclass     = {'build_ext' : PyEXO_build_ext,
                             'clean'     : PyEXO_clean    , 
                             'build'     : PyEXO_build    }, 
             ext_modules  = [Extension('pyexo._' + base_name,
                                      ['src/%s_interface.i' % base_name],
                                      include_dirs  = include_dirs,
                                      swig_opts     = swig_flags, 
                                      define_macros = defines,
                                      library_dirs  = lib_dirs,
                                      libraries     = libs
                                      )])

