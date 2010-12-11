%module(docstring="python wrapping of EXOoffline software",
        directors="1", 
        allprotected="1") PyEXOAnalysis

/* Temporary hack to disable mysql and G4*/
%init %{
import_array();
%}
%{
#include "EXOAnalysisManager/EXOAnalysisManager.hh"
#include "EXOAnalysisManager/EXOAnalysisModule.hh"
#include "EXOAnalysisManager/EXOInputModule.hh"
#include "EXOUtilities/EXOChannelMap.hh"
#include "EXOUtilities/EXOErrorLogger.hh"
#include "EXOUtilities/EXOTalkToManager.hh"
#include "EXOUtilities/EXOEventData.hh"
#include "EXOCalibUtilities/EXOCalibManager.hh"
#include "EXOAnalysisManager/EXOTreeInputModule.hh"
#include "core/include/numpy/arrayobject.h"
%}
%include stl.i

// The following is actually a bit odd.  Is this function
// never instantiated?
%include "EXOAnalysisManager/EXOAnalysisManager.hh"
%include "EXOAnalysisManager/EXOAnalysisModuleFactory.hh"

/* The following allows us to subclass Analysis 
   and Input modules in python. This is especially
   powerful to be able to access all the functionality
   built in to python or available in python. */
%exception EXOAnalysisModule::GetName {
    try {
        $action
    } 
    catch(Swig::DirectorPureVirtualException) { 
        printf("\npyexo ERROR:                                                                    \n"
               "Calling EXOAnalysisModule::GetName as a pure virtual.                             \n"
               "This function (returning a string) needs to be defined in the python class, e.g.: \n"
               "  class MyClass(pyexo.EXOAnalysisModule):                                         \n"
               "    def GetName(self): return \"MyClass\"                                         \n"
               "    ...                                                                         \n\n");
        Swig::DirectorPureVirtualException::raise("EXOAnalysisModule::GetName");
    }
}


%feature("director") EXOAnalysisModule;
%feature("director") EXOInputModule;
%include "EXOAnalysisManager/EXOAnalysisModule.hh"
%include "EXOAnalysisManager/EXOInputModule.hh"

/* Ensuring that we get some information about 
   exceptions.  FixME: throw an EXO Exception? */
%include "EXOUtilities/EXOChannelMap.hh"
%ignore EXOErrorLogger::LogError(char const *,char const *,char const *,int);
%include "EXOUtilities/EXOErrorLogger.hh"
%include "EXOUtilities/EXOTalkToManager.hh"

/* MYSQL causes some problems with SWIG.  
   In particular, we need to be careful
   since this functions are defined in the
   header dependent upon whether or
   not NOMYSQL is set.  Therefore, we
   shut off the interface and assume
   that the user has appropriately set
   up the env variables in his/her setup.*/
/* If the environment variables are not consistent
   with the build of EXOAnalysis, you will 
   get a hard-to-understand malloc error 
   which indicates that the memory footprint
   of the object is different in the library
   that pyexo is expecting. */
%ignore EXOCalibManager::m_mysqlConn;
%ignore EXOCalibManager::getMysqlBest;
%ignore EXOCalibManager::makeMysqlConnection();
%ignore EXOCalibManager::setMysqlOptions;
%ignore EXOCalibManager::borrowConnection();
%include "EXOCalibUtilities/EXOCalibManager.hh"
%include "EXOAnalysisManager/EXOTreeInputModule.hh"

/* Following deals with event data. */
%rename ("_in") EXOEventData::in;
%rename ("EXOEventData_scintillation_site") EXOEventData::scintillation_site;
%ignore EXOEventData::add_scintillation_site;
%ignore EXOEventData::get_scintillation_site;
%include "EXOUtilities/EXOEventData.hh"

/* We extend EXOEventData, templatized to deal with 
   the many arrays in EXOEventData. adding get_data_as_ndarray. 
   In general, we need to be careful when dealing with
   memory sharing between python and C.  In this case
   EXOEventData::data is a buffer of a defined size and
   is allocated in the scope of the EXOEventData so it
   is always guaranteed to be available during the run-
   ning program.  PyArray_SimpleNewFromData does *not*
   copy memory, everything happens in-place. 

   Eventually, this will need to be templatized to
   allow access to all the buffers in EXOEventData,
   but for now, we just access the data and channel
   info of the raw waveforms. */
%define %exo_array_as_numpy_array(EXOCLASS, EXOVARIABLE, EXOBOUND, THETYPE)
%extend EXOCLASS {
    PyObject* get_##EXOVARIABLE##_as_ndarray() {
        npy_intp dim = $self->EXOBOUND;
        PyObject* return_obj = PyArray_SimpleNewFromData(1, &dim, THETYPE, $self->EXOVARIABLE); 
        return return_obj;
    }
}
%enddef

/* MC info for EXOEventData */
%exo_array_as_numpy_array( EXOEventData, idpart, npart, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, epart,  npart, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, qpart,  npart, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, apart,  npart, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, expart, npart, NPY_DOUBLE )

%exo_array_as_numpy_array( EXOEventData, ixq, nq, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, iyq, nq, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, izq, nq, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, etq, nq, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, eiq, nq, NPY_DOUBLE )

%exo_array_as_numpy_array( EXOEventData, apd_hits, napd, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, eapd,     napd, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, qapd,     napd, NPY_DOUBLE )

%exo_array_as_numpy_array( EXOEventData, ercl,    ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, eccl,    ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, eerrcl,  ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, xcl,     ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, ycl,     ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, ucl,     ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, vcl,     ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, zcl,     ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, tcl,     ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, ncscl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, iu1cl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, iu2cl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, iu3cl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, iu4cl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, nvchcl,  ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, iv1cl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, iv2cl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, dhalfcl, ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, evcl,    ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, dtcl,    ncl, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, isccl,   ncl, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, fidcl,   ncl, NPY_BOOL )
%exo_array_as_numpy_array( EXOEventData, ghcl,    ncl, NPY_BOOL )
%exo_array_as_numpy_array( EXOEventData, tdcl,    ncl, NPY_BOOL )
/* Can't handle BOOLs just yet */

%exo_array_as_numpy_array( EXOEventData, c1sc,    nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, c1errsc, nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, c2sc,    nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, c2errsc, nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, rsc,     nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, ssc,     nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, sssc,    nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, thsc,    nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, xsc,     nsc, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, ysc,     nsc, NPY_DOUBLE )

%exo_array_as_numpy_array( EXOEventData, csc,    nphe, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, cerrsc, nphe, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, esc,    nphe, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, tsc,    nphe, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, zsc,    nphe, NPY_DOUBLE )
%exo_array_as_numpy_array( EXOEventData, algsc,  nphe, NPY_INT )

%exo_array_as_numpy_array( EXOEventData, data, nele, NPY_INT )
%exo_array_as_numpy_array( EXOEventData, chan, nsig, NPY_INT )

%exo_array_as_numpy_array( EXOEventData, qdata, nqele, NPY_USHORT )
