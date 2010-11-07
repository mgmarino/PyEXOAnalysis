UNAME := $(shell uname)
PACKAGE_NAME = PyEXOAnalysis
SWIG = swig
SWIG_FLAGS = -python -dirprot
PYTHONCONF = /opt/TWWfsw/python25/bin/python-config 
PYTHON = $(shell $(PYTHONCONF) --exec-prefix)/bin/python

ifeq ($(UNAME), Darwin)
SONAME = dylib
else
SONAME = so
endif

EXOANALYSISLIBS = EXOAnalysisManager EXOUtilities EXOReconstruction EXOCalibUtilities EXODBUtilities EXOSim  EXOBinaryPackage
EXOANALYSISLIB_FLAGS = $(patsubst %, -l%, $(EXOANALYSISLIBS))

ROOT_INC_FLAGS = -I$(shell root-config --incdir)
ROOT_CC_FLAGS = $(shell root-config --auxcflags)
ROOT_LD_FLAGS = $(shell root-config --libs)


ifndef EXOLIB
INCFLAGS = -I../analysis/manager             \
            -I../utilities/misc               \
            -I../utilities/calib              \
            -I../include                      \
            -I../../EXOBinaryPackage          
EXOLIBFLAGS = -L/tmp/$(shell whoami)/exoout/lib
else
INCFLAGS = -I$(EXOLIB)/include -I.
EXOLIBFLAGS = -L$(EXOLIB)/lib
endif

INCFLAGS += $(shell $(PYTHONCONF) --includes) \
            $(ROOT_INC_FLAGS)                 \
            -I$(shell $(PYTHON) -c 'import numpy; print numpy.__path__[0]')

CCFLAGS = $(INCFLAGS) $(ROOT_CC_FLAGS) 
CXXFLAGS = -Wall -fPIC -O2
CXX = g++
LDFLAGS = -shared \
          $(shell $(PYTHONCONF) --ldflags) \
          $(EXOLIBFLAGS) \
          $(EXOANALYSISLIB_FLAGS) \
          $(ROOT_LD_FLAGS) 
          #$(shell python - --ldflags) \

INTERFACE_NAME = $(PACKAGE_NAME)_interface.i 
WRAPPER = $(INTERFACE_NAME:.i=_wrap.cxx)
OBJS = $(WRAPPER:.cxx=.o)
PYTHON_LIB = _$(PACKAGE_NAME).$(SONAME) 

all: $(PYTHON_LIB)

,depend: $(INTERFACE_NAME) 
	@$(SWIG) -M -c++ $(LANGUAGE_TYPE) $(CCFLAGS) $< > $@  

-include .depend

$(WRAPPER): $(INTERFACE_NAME)
	$(SWIG) -c++ $(SWIG_FLAGS) $(INCFLAGS) -o $@ $<

$(OBJS): $(WRAPPER)
	$(CXX) $(CXXFLAGS) -c $(CCFLAGS) -o $@ $< 

$(PYTHON_LIB): $(OBJS)
	$(CXX) $(LDFLAGS) $(OBJS) -o $@ 

clean:
	@rm -rf $(OBJS) $(PYTHON_LIB) $(WRAPPER) $(PACKAGE_NAME).py* _$(PACKAGE_NAME)*
