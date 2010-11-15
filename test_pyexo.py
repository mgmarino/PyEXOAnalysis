import sys
            
def run_test():
   
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
       def test(self):
           print "  Checking if we can access protected members in EXOAnalysisModule ...",
           try: 
               event_data = self.ED
               print "yes"
               try: 
                   print "  Checking if we can get arrays back from EXOEventData ...",
                   dat = event_data.get_data_as_ndarray()
                   print "yes"
               except Exception, e:
                   print "no"
                   print "Failed with exception: ", e
                   pass
           except AttributeError: 
               print "no"
               print """

Problem accessing protected members
This problem is likely due to using an older version of SWIG
Please try updating the SWIG version and then reinstalling
pyexo.
               """ 
               pass
   
    print "Testing basic instantiation..."
    print

    analysis_mgr = pyexo.PyEXOOfflineManager()

    mgr = analysis_mgr.get_analysis_mgr()
    
    test = EXOTest("test", mgr)
    analysis_mgr.register_module(test, "test")
    mgr.ShowRegisteredModules()
    print "Testing Module access"
    print
    test.test()

if __name__ == '__main__':
    run_test()
    print sys.argv[0], "test ended.  If no horrible error output was seen, you should be all set."
