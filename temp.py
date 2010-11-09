import sys
import os.path

def run_analysis(list_of_input_files, output_directory):
    import EXOofflineMgr
    import PyEXOAnalysis as EXOoffline
    from EXOFFTWAnalysis import EXOFFTWAnalysis
   
    # now parse what we need    
   
    for input_file in list_of_input_files:
        analysis_mgr = EXOofflineMgr.EXOofflineMgr()
        mgr = analysis_mgr.get_analysis_mgr()
        
        wf_anal = EXOFFTWAnalysis("fftw", mgr)
        input = EXOoffline.EXOTreeInputModule("EXOTreeInputModule", mgr)
        analysis_mgr.register_module(input, "tinput")
        analysis_mgr.register_module(wf_anal, "fftw")
        mgr.ShowRegisteredModules()
 
        base_file_name = os.path.basename(input_file) 
        base_file_name, _ = os.path.splitext(base_file_name)
        base_file_name = output_directory + '/' \
                         + base_file_name + "wf_fftwanalysis.pkl"
        wf_anal.set_name_of_output_file(base_file_name)

        print "Reading from file: ", input_file
        print "  Outputting to: ", base_file_name
        analysis_mgr.set_filename(input_file)
        analysis_mgr.run_analysis()
        print "Done..."

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: [output_directory] [files_to_parse]"
        sys.exit(1)
    run_analysis(sys.argv[2:], sys.argv[1])
