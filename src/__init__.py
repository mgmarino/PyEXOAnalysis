import pyexo.PyEXOAnalysis as exo
from pyexo.PyEXOOfflineManager import PyEXOOfflineManager 

# Flatten the name space to allow
# people to call e.g.
# pyexo.EXOAnalysisModule()
# etc. 
module_dict = globals()


for module in [exo]:
    for export_obj_name, export_obj in module.__dict__.items():
        if export_obj_name not in module_dict:
            module_dict[export_obj_name] = export_obj

