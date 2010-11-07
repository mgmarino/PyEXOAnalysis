import PyEXOAnalysis as EXOoffline
import ROOT
import array
import numpy

class EXOSimpleWaveformAnalysis(EXOoffline.EXOAnalysisModule):
    def __init__(self, name, mgr):
        EXOoffline.EXOAnalysisModule.__init__(self, name, mgr)
        self.baseline = array.array('d', [0])
        self.maximum = array.array('i', [0])
        self.minimum = array.array('i', [0])
        self.channel = array.array('i', [0])
        self.event_number = array.array('i', [0])

    def BeginOfRun(self):
        self.output_file = ROOT.TFile("outputWF" + str(self.ED.nr) + ".root", "recreate")
        self.tree = ROOT.TTree("WaveformInfo", "WaveformInfo")
        self.tree.Branch("eventNumber", self.event_number, "eventNumber/I")
        self.tree.Branch("baseline"   , self.baseline    , "baseline/D")
        self.tree.Branch("maximum"    , self.maximum     , "maximum/I")
        self.tree.Branch("minimum"    , self.minimum     , "minimum/I")
        self.tree.Branch("channel"    , self.channel     , "channel/I")
        return 0


    def BeginOfEvent(self):
        if self.ED.nsig == 0: return 0
        self.event_number[0] = self.ED.ne
        num_per_event = self.ED.nele/self.ED.nsig
        anarray = self.ED.get_data_as_ndarray()
        chan_array = self.ED.get_chan_array_as_ndarray()
        work_with = anarray.reshape(-1, num_per_event)

        for the_event, chan in zip(work_with, chan_array):
            self.maximum[0] = the_event.max() 
            self.minimum[0] = the_event.min() 
            self.baseline[0] = the_event.mean() 
            self.channel[0] = chan
            self.tree.Fill()
        return 0

    def ShutDown(self):
        print "Finishing Up"
        self.output_file.cd()
        self.tree.Write()
        self.output_file.Close()
        return 0


