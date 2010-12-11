import sys
import re
import types
            
type_dict = { 'unsigned short' : 'NPY_USHORT',
              'int'            : 'NPY_INT',
              'unsigned int'   : 'NPY_UINT', 
              'double'         : 'NPY_DOUBLE', 
              'bool'           : 'NPY_BOOL', 
            }

def run_test(verbose = False):
   
    print 
    print "Looing for pyexo ...",
    try:
        import pyexo
    except ImportError, e:
        print """

pyexo installation not found.  Be sure that your python path 
(e.g. using PYTHONPATH) is appropriately set."""

        print "Actual output: ", e
        sys.exit(1)

    print "found in the path: ", pyexo.__path__[0]

    class EXOTest(pyexo.EXOAnalysisModule):
       def GetName(self): return "EXOTest"
       def test(self):
           print "  Checking if we can access protected members in EXOAnalysisModule ...",
           try: 
               event_data = self.analysisManager
               print "yes"
           except AttributeError: 
               print "no"
               print """
Problem accessing protected members.  This will reduce
the functionality of the python bindings since you will
be unable to access things like EXOAnalysisModule::analysisManager
in your derived python classes.  In most cases, though, this
functionality will not be necessary.

This problem is almost certainly due to using an older version of SWIG.
Please try updating the SWIG version and then reinstalling
pyexo.
               """ 
               pass
   
    print "Testing basic instantiation..."
    print

    try:
        analysis_mgr = pyexo.PyEXOOfflineManager()
        
        mgr = analysis_mgr.get_analysis_mgr()
        
        test = EXOTest( mgr)
        analysis_mgr.register_module(test, "test")
        mgr.ShowRegisteredModules()
    except Exception, e:
        print e
        raise
    print "Testing Module access"
    print                
    test.test()          

    print "Testing EXOEventData access"
    print                
    if not verbose: print "  Testing with low verbosity, pass --verbose to increase"
    event_data = pyexo.EXOEventData()
    list_of_gets = dict([ (aget,'') for aget in dir(event_data) if re.match("get_(.*)_as_ndarray", aget) ]) 
    list_of_arrays = []
    list_of_additions_to_interface = []
    for member_name in dir(event_data):
        if member_name in ["this", "clear"]: continue
        if re.match("__*", member_name): continue
        if re.match("get_(.*)_as_ndarray", member_name): continue
        var = getattr(event_data, member_name)
        if type(var) not in [ types.IntType, 
                              types.StringType, 
                              types.FloatType,
                              types.BooleanType ]:
            try: 
                func_name = "get_%s_as_ndarray" % member_name
                access_array = getattr(event_data, func_name)
                list_of_arrays.append("   Access function: {0:23} to access   {1:10} returns numpy array of type {2:8} {3}".format( func_name,
                                                                                                              member_name, str(access_array().dtype),
                                                                                                              repr(var)))
                del list_of_gets[func_name] 
            except AttributeError:
                if not re.match("<bound method .*", repr(var)):
                    list_of_arrays.append( "   NDArray access not yet implemented for %s, type: %s" % (member_name, repr(var)))
                    atype = re.match("<Swig Object of type '(.*) \*' at.*", repr(var)) 
                    if not atype: continue
                    atype = atype.group(1)
                    if not atype in type_dict:
                        list_of_additions_to_interface.append("ERROR with %s" % atype)
                    else:
                        list_of_additions_to_interface.append("%%exo_array_as_numpy_array( EXOEventData, %s, ?, %s )" % (member_name, type_dict[atype]))
                    
        else:
            if verbose: print "   Basic type, {0:15}: {1:30}".format(member_name, type(var))
    if verbose: 
        for val in list_of_arrays: print val
    if len( list_of_gets ) != 0 and verbose:
        print "   Depracated accesses need to be removed:"
        for aget in list_of_gets.keys(): print "     %s" % aget
    if verbose: 
        for val in list_of_additions_to_interface: print val
    print
                         
if __name__ == '__main__':
    verbose = False
    if len(sys.argv) > 1 and sys.argv[1] == '--verbose': verbose = True 
    run_test(verbose)           
    print sys.argv[0], "test ended.  If no horrible error output was seen, you should be all set."
