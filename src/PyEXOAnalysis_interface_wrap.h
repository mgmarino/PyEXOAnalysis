/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 1.3.36
 * 
 * This file is not intended to be easily readable and contains a number of 
 * coding conventions designed to improve portability and efficiency. Do not make
 * changes to this file unless you know what you are doing--modify the SWIG 
 * interface file instead. 
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_PyEXOAnalysis_WRAP_H_
#define SWIG_PyEXOAnalysis_WRAP_H_

#include <map>
#include <string>


class SwigDirector_EXOAnalysisModule : public EXOAnalysisModule, public Swig::Director {

public:
    SwigDirector_EXOAnalysisModule(PyObject *self, char const *NAME, EXOAnalysisManager *MANAGER);
    virtual ~SwigDirector_EXOAnalysisModule();
    virtual int Initialize();
    virtual int BeginOfRun();
    virtual int BeginOfEvent();
    virtual int EndOfEvent();
    virtual int EndOfRun();
    virtual int BeginOfRunSegment();
    virtual int EndOfRunSegment();
    virtual int TalkTo();
    virtual int ShutDown();
    using EXOAnalysisModule::name;
    using EXOAnalysisModule::analysisManager;
    using EXOAnalysisModule::errorLogger;
    using EXOAnalysisModule::talktoManager;
    using EXOAnalysisModule::ED;
    using EXOAnalysisModule::channelMap;
    using EXOAnalysisModule::input_module;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class EXOAnalysisModule doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[9];
#endif

};


class SwigDirector_EXOInputModule : public EXOInputModule, public Swig::Director {

public:
    SwigDirector_EXOInputModule(PyObject *self, char const *NAME, EXOAnalysisManager *MANAGER);
    virtual ~SwigDirector_EXOInputModule();
    virtual int Initialize();
    virtual int BeginOfRun();
    virtual int BeginOfEvent();
    virtual int EndOfEvent();
    virtual int EndOfRun();
    virtual int BeginOfRunSegment();
    virtual int EndOfRunSegment();
    virtual int TalkTo();
    virtual int ShutDown();
    virtual bool continue_analysis();
    virtual int get_run_number();
    virtual int get_event_number();
    virtual bool file_type_recognized();
    virtual bool is_new_run_segment();
    using EXOInputModule::filename;
    using EXOInputModule::last_filename;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class EXOInputModule doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[14];
#endif

};


#endif