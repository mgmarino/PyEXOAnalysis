#!/bin/env python
import os
import sys
import shutil

def run_analysis(list_of_input_files, temp_outputdir, final_output_directory):
    import EXOofflineMgr
    import PyEXOAnalysis as EXOoffline
    from EXOSimpleWaveformAnalysis import EXOSimpleWaveformAnalysis
   
    import shutil
    # now parse what we need    
    if temp_outputdir[-1] == '/':
        temp_outputdir = temp_outputdir[0:-1]
    
    for input_file in list_of_input_files:
        analysis_mgr = EXOofflineMgr.EXOofflineMgr()
        mgr = analysis_mgr.get_analysis_mgr()
        
        wf_anal = EXOSimpleWaveformAnalysis("wf_anal", mgr)
        input = EXOoffline.EXOTreeInputModule("EXOTreeInputModule", mgr)
        analysis_mgr.register_module(input, "tinput")
        analysis_mgr.register_module(wf_anal, "wf_anal")
        mgr.ShowRegisteredModules()
 
        base_file_name = os.path.basename(input_file) 
        base_file_name, _ = os.path.splitext(base_file_name)
        base_file_name = temp_outputdir + '/' \
                         + base_file_name + \
                         "wf_analysis.root"
        wf_anal.set_name_of_output_file(base_file_name)

        print "Reading from file: ", input_file
        print "  Outputting to: ", base_file_name
        analysis_mgr.set_filename(input_file)
        analysis_mgr.run_analysis()

        shutil.move(base_file_name, final_output_directory)
        print "Done..."

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: [final_output_dir] [files_to_parse]"
        sys.exit(1)
    
    import getpass
    temp_dir =  "/scratch/" + \
                getpass.getuser() + \
                "/" + os.environ['LSB_JOBID']
    final_dir = sys.argv[1]
    print "  Temp output is: ",  temp_dir
    print "  Final output is: ", final_dir
    if not os.path.isdir(temp_dir):
        os.makedirs(temp_dir)
    if not os.path.isdir(final_dir):
        print "  Final output dir is not a directory!"
        sys.exit(1)

    print "Input file(s) is/are:"
    for afile in sys.argv[2:]:
        print "  " + afile
    run_analysis(sys.argv[2:], temp_dir, final_dir) 
    shutil.rmtree(temp_dir)
