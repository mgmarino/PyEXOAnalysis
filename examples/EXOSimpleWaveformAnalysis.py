import pyexo as EXOoffline
import ROOT
import array
import numpy
from ctypes import c_ulonglong

class EXOSimpleWaveformAnalysis(EXOoffline.EXOAnalysisModule):
    def __init__(self, name, mgr):
        EXOoffline.EXOAnalysisModule.__init__(self, name, mgr)
        self.baseline        = array.array('d', [0])
        self.maximum         = array.array('i', [0])
        self.minimum         = array.array('i', [0])
        self.channel         = array.array('i', [0])
        self.event_number    = array.array('i', [0])
        self.output_filename = "outputWF"
        self.time            = (c_ulonglong*1)()
        self.time_since_last = (c_ulonglong*1)()
        self.last_time       = 0

    def set_name_of_output_file(self, name): self.output_filename = name 

    def BeginOfRun(self, ED):
        print "Beginning Run"
        self.output_file = ROOT.TFile(self.output_filename, "recreate")
        self.tree = ROOT.TTree("WaveformInfo", "WaveformInfo")
        self.tree.Branch("eventNumber", self.event_number   , "eventNumber/I")
        self.tree.Branch("baseline"   , self.baseline       , "baseline/D")
        self.tree.Branch("maximum"    , self.maximum        , "maximum/I")
        self.tree.Branch("minimum"    , self.minimum        , "minimum/I")
        self.tree.Branch("channel"    , self.channel        , "channel/I")
        self.tree.Branch("time"       , self.time           , "time/l")
        self.tree.Branch("time_diff"  , self.time_since_last, "time_diff/l")
        self.last_time = 0
        print "Initialization done"
        return 0


    def BeginOfEvent(self, ED):
        if ED.nsig == 0: return 0
        num_per_event        = ED.nele/ED.nsig
        if num_per_event == 0: return 0
        
        # Dealing with time information
        self.time[0] = ED.trigsec*1000000 + ED.trigsub
        if self.last_time == 0:
            self.time_since_last[0] = 0
        else:
            self.time_since_last[0] = self.time[0] - self.last_time
        self.last_time = self.time[0]
        
        self.event_number[0] = ED.ne
        anarray              = ED.get_data_as_ndarray()
        chan_array           = ED.get_chan_as_ndarray()
        work_with            = anarray.reshape(-1, num_per_event)
        
        # Now event-by-event 
        for the_event, chan in zip(work_with, chan_array):
            self.maximum[0]  = the_event.max() 
            self.minimum[0]  = the_event.min() 
            self.baseline[0] = the_event.mean() 
            self.channel[0]  = chan
            self.tree.Fill()
        return 0

    def ShutDown(self):
        print "  Finishing Up, writing out:", self.output_file.GetName()
        self.output_file.cd()
        self.tree.Write()
        self.output_file.Close()
        return 0


