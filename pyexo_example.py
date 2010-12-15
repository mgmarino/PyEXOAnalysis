import sys
import os.path
import pyexo
import cPickle as pickle

class EXOExample(pyexo.EXOAnalysisModule):
    """
    An example of how one might subclass an EXOAnalysisModule in python
    You absolutely don't have to use anything you won't need, and
    of course you can add additional functions as necessary.
    This class is defined here, but normally you would define the class
    in a separate module (i.e. a separate .py file) and import it. 
    """

    # class variable 
    output_filename = "example.tmp"
    last_array = None
    def set_name_of_output_file(self, name): self.output_filename = name 

    def BeginOfRun(self, ED):
        print "Beginning Run"
        print "Initialization done"
        return 0


    def BeginOfEvent(self, ED):
        # We can directly access the protected data of EXOAnalysisModule, for example
        # below is accessing self.ED (self is like 'this') which is
        # the EXOEventData
        if ED.nsig == 0: return 0

        num_per_event        = ED.nele/ED.nsig
        if num_per_event == 0: return 0
        
        # pyexo automatically returns the data array as
        # a numpy array.  No additional data copying, this
        # is fast.
        anarray              = ED.get_data_as_ndarray()
        chan_array           = ED.get_chan_as_ndarray()
        
        print num_per_event
        # numpy ndarrays are rad, just reshape to get a 2-d
        # array.  Again, no data copying. 
        work_with            = anarray.reshape(-1, num_per_event)

        print "Printing out the waveform array for channel: ", chan_array[0]
        self.last_array = work_with[0].copy()
        print self.last_array
        
        return 0

    def ShutDown(self):
        # Just to be cute, we can pickle to the output file
        print "  Finishing Up, pickling a waveform to:", self.output_filename
        try:
            pickle.dump(self.last_array, open(self.output_filename, 'wb'))
        except Exception, e:
            print e
        
        return 0


def run_analysis(list_of_input_files, output_directory):
    """ 
    This is an example analysis script that one might write.
    It essentially replaces EXOAnalysis.cc, the idea here for
    this example is to be as simple as possible.  In particular,
    registration of modules is streamlined. 
    """
   
    # Loop over the input files"
    for input_file in list_of_input_files:
        #############################################
        # The analysis manager handles all the basic 
        # instantiations that must happen for initialization.        
        # In general for quick, one-off analyses, the
        # internals will not be important.
        analysis_mgr = pyexo.PyEXOOfflineManager()

        # mgr is an EXOAnalysisManager instance
        mgr = analysis_mgr.get_analysis_mgr()
        #############################################
        
        #############################################
        # Now instantiate our modules:
        #
        # First a compiled module distributed by
        # EXOAnalysis:
        # Then a module we defined above:
        wf_analysis = EXOExample(mgr)
        #############################################


        #############################################
        # Now we register the modules.  Note, that
        # the order of registration is important
        # as the modules will be called in this
        # order in the analysis loop.
        # The name given is just a nickname, 
        mgr.UseModule("input")
        analysis_mgr.register_module(wf_analysis, "example")
        mgr.ShowRegisteredModules()
        #############################################
 
        #############################################
        # Setting the base file name from the input
        # (presumably ROOt) file:
        base_file_name    = os.path.basename(input_file)
        base_file_name, _ = os.path.splitext(base_file_name)
        base_file_name    = os.path.join(output_directory,  
                                         base_file_name + "example.pkl")  
        wf_analysis.set_name_of_output_file(base_file_name)
        #############################################

        print "Reading from file: ", input_file
        print "  Outputting to: ", base_file_name
        #############################################

        #############################################
        # Setting the input filename
        # Since we selected the EXOTreeInputModule above,
        # this should be a ROOT file
        analysis_mgr.set_filename(input_file)
        #############################################


        #############################################
        # Go, actually do the analysis
        analysis_mgr.run_analysis()
        print "Done..."
        #############################################

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: [output_directory] [files_to_parse]"
        sys.exit(1)
    run_analysis(sys.argv[2:], sys.argv[1])
