
"""
  Class that basically performs the same function as Analysis Manager
  but allows simple loading from a python script.
  Performs all the necessary initializations, etc.

  An important difference is that the function 'register_module' 
  registers the module *and* puts it in the analysis.  This means
  that if a module is not to be used, than don't call this function.
  This avoids unnecessary loading of unused modules, etc.

"""
class PyEXOOfflineManager:

    def __init__ (self):

        import PyEXOAnalysis as EXOoffline
        self.channel_map  = EXOoffline.EXOChannelMap()
        self.error_logger = EXOoffline.EXOErrorLogger()
        self.exo_data     = EXOoffline.EXOEventData()
        
        self.talk_to      = EXOoffline.EXOTalkToManager(self.error_logger)
        self.calib_mgr    = EXOoffline.EXOCalibManager(self.error_logger)
        
        self.analysis_mgr = EXOoffline.EXOAnalysisManager(
                              self.error_logger,
                              self.talk_to, 
                              self.exo_data,
                              self.channel_map,
                              self.calib_mgr)
        self.modules = []
        self.filename = ""

    """
    The following access functions are for completeness, but 
    won't normally need to be called.
    """
    def get_channel_map(self):  return self.channel_map
    def get_error_logger(self): return self.error_logger
    def get_exo_data(self):     return self.exo_data
    def get_talkto_mgr(self):   return self.talk_to
    def get_calib_mgr(self):    return self.calib_mgr
    def get_analysis_mgr(self): return self.analysis_mgr

    def set_filename(self, aname): self.filename = aname 

    """
    The following registers a module and sets it up to be called.
    Therefore, the ordering of calls to this function is important!
    """

    def register_module(self, module, nickname): 
        # Be careful of memory management,
        # EXOAnalysisManager now owns this object
        # Don't let python delete it
        self.modules.append((nickname,module))
        self.analysis_mgr.UseModule(module, nickname)
   
    def run_analysis(self):
        
        if len(self.modules) == 0: return
        use_string = "use"

        file_str = "/input/file " + self.filename + "\0"
        self.talk_to.InterpretCommand(file_str)
        self.talk_to.InterpretCommand("show")
        self.talk_to.InterpretCommand("begin")
        self.analysis_mgr.RunAnalysis()
        self.analysis_mgr.FinishAnalysis()
    
        

