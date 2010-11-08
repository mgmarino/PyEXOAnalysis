import PyEXOAnalysis as EXOoffline
import ROOT
import array
import numpy
import fftw3
import cPickle as pick
import ctypes


class EXOFFTWAnalysis(EXOoffline.EXOAnalysisModule):
    def __init__(self, name, mgr):
        EXOoffline.EXOAnalysisModule.__init__(self, name, mgr)
        self.output_filename = "outputWF_FFT"
        self.plan = None

    def BeginOfRun(self):
        print "Beginning Run"
        self.output_dict = {}
        self.open_file = open(self.output_filename, 'wb')
        self.defined_run_size = None
        print "Initialization done"
        return 0

    def set_name_of_output_file(self, name): self.output_filename = name 

    def BeginOfEvent(self):
        if self.ED.nsig == 0: return 0
        num_per_event        = self.ED.nele/self.ED.nsig
        if not self.defined_run_size: self.defined_run_size = num_per_event 
        if self.defined_run_size != num_per_event: return 0

        anarray              = self.ED.get_data_as_ndarray()
        chan_array           = self.ED.get_chan_array_as_ndarray()
        work_with            = anarray.reshape(-1, num_per_event)
             
        complex_array        = numpy.zeros(num_per_event/2 + 1, dtype=numpy.complex)
        the_event_f          = numpy.zeros(num_per_event)
        plan = fftw3.Plan(the_event_f, complex_array, direction='forward') 
        # Now event-by-event 
        abs = numpy.abs
        square = numpy.square
        for the_event, chan in zip(work_with, chan_array):
            the_event_f_tmp = the_event.astype(float)
            # Have to copy data into the planned array
            # the overhead to create new plans is very
            # high.
            ctypes.memmove(the_event_f.ctypes._data,
                           the_event_f_tmp.ctypes._data, 
                           8*num_per_event) 
            plan.execute()
            if chan not in self.output_dict: 
                self.output_dict[chan] = [square(abs(complex_array)), 1]
            else:
                self.output_dict[chan][0] += square(abs(complex_array))
                self.output_dict[chan][1] += 1 

        return 0

    def EndOfRun(self):
        # Here we can serialize everything
        print "Dumping out FFTs"
        try:
            pick.dump(self.output_dict, self.open_file)
            self.open_file.close()
        except Exception, e:
            print e
            raise 
        return 0
