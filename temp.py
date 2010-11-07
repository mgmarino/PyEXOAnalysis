import EXOofflineMgr
import EXOoffline
import sys
import ROOT
import numpy
import ctypes
from EXOSimpleWaveformAnalysis import EXOSimpleWaveformAnalysis


class SubClass(EXOoffline.EXOAnalysisModule):
    def __init__(self, name, mgr):
        EXOoffline.EXOAnalysisModule.__init__(self, name, mgr)
        self.number_of_times = 0
        self.c1 = ROOT.TCanvas()

    def BeginOfEvent(self):
        if self.ED.nsig == 0: return 0
        num_per_event = self.ED.nele/self.ED.nsig
        narray = numpy.arange(num_per_event, dtype=numpy.int32)
        anarray = self.ED.get_data_as_ndarray()
        print anarray, len(anarray)
        for i in range(self.ED.nsig):
            print i, self.ED.get_chan_array_as_ndarray()[i]
            graph = ROOT.TGraph(num_per_event, narray, anarray[i*num_per_event:]) 
            graph.Draw("APL")
            self.c1.Update()
            raw_input("e")
            
        self.number_of_times += 1
        return 0

    def EndOfRun(self):
        print "EndOfRun"
        print self.number_of_times
        return 0

    def Shutdown (self):
        print "Shutdown"
        print self.number_of_times
        return 0

analysis_mgr = EXOofflineMgr.EXOofflineMgr()
mgr = analysis_mgr.get_analysis_mgr()

temp = EXOSimpleWaveformAnalysis("wf_anal", mgr)
input = EXOoffline.EXOTreeInputModule("EXOTreeInputModule", mgr)
#tree = EXOoffline.EXOTreeInputModule("EXOTreeInputModule", mgr)
analysis_mgr.register_module(input, "tinput")
analysis_mgr.register_module(temp, "wf_anal")

mgr.ShowRegisteredModules()

analysis_mgr.set_filename(sys.argv[1])
analysis_mgr.run_analysis()
