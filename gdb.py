import arcpy
import os
import sys


path = sys.path[0]
gdb_list = []
for d, ds, fs in os.walk(path):
    for dd in ds:
        if os.path.splitext(dd)[1].lower() == '.gdb':
            print(d + os.sep + dd)
            gdb_list.append(d + os.sep + dd)


# walk = arcpy.da.Walk(workspace)
# for dp, dn, fl in walk[0]:
