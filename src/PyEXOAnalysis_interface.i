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
#include "core/include/numpy/ndarrayobject.h"
%}

// The following is actually a bit odd.  Is this function
// never instantiated?
%ignore EXOAnalysisManager::ParseListOfNames();
%include "EXOAnalysisManager/EXOAnalysisManager.hh"

/* The following allows us to subclass Analysis 
   and Input modules in python. This is especially
   powerful to be able to access all the functionality
   built in to python or available in python. */
%feature("director") EXOAnalysisModule;
%feature("director") EXOInputModule;
%include "EXOAnalysisManager/EXOAnalysisModule.hh"
%include "EXOAnalysisManager/EXOInputModule.hh"

/* Ensuring that we get some information about 
   exceptions.  FixME: throw an EXO Exception? */

%include "EXOUtilities/EXOChannelMap.hh"
%include "EXOUtilities/EXOErrorLogger.hh"
%include "EXOUtilities/EXOTalkToManager.hh"

%ignore EXOCalibManager::m_mysqlConn;
%ignore EXOCalibManager::getMysqlBest();
%ignore EXOCalibManager::makeMysqlConnection();
%include "EXOCalibUtilities/EXOCalibManager.hh"
%include "EXOAnalysisManager/EXOTreeInputModule.hh"

/* Following deals with event data. */
%rename ("_in") EXOEventData::in;
%include "EXOUtilities/EXOEventData.hh"
/* We extend EXOEventData, adding get_data_as_ndarray. 
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
%extend EXOEventData {
    /* Return EXOEventData::data as an numpy.ndarray */
    PyObject* get_data_as_ndarray() {
        npy_intp dim = $self->nele;
        PyObject* return_obj = PyArray_SimpleNewFromData(1, &dim, NPY_INT, $self->data); 
        return return_obj;
    }
    /* Return EXOEventData::chan as an numpy.ndarray */
    PyObject* get_chan_array_as_ndarray() {
        npy_intp dim = $self->nsig;
        PyObject* return_obj = PyArray_SimpleNewFromData(1, &dim, NPY_INT, $self->chan); 
        return return_obj;
    }
}
