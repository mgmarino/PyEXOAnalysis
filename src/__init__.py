print "Welcome to pyexo"
import pyexo.PyEXOAnalysis as exo
import pyexo.PyEXOOfflineManager as mgr

# Flatten the name space to allow
# people to call e.g.
# pyexo.EXOAnalysisModule()
# etc. 
module_dict = globals()


for module in [exo, mgr]:
    for export_obj_name, export_obj in module.__dict__.items():
        if export_obj_name not in module_dict:
            module_dict[export_obj_name] = export_obj

