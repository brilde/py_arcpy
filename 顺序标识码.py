import arcpy

arcpy.env.workspace = r'D:\GZ\西藏入库\0224\类武器库.gdb'
# table_value = arcpy.ListFeatureClasses()
table_value = ['JZX', 'JZD']
rec = 0
for table in table_value:
    with arcpy.da.UpdateCursor(table, ["OID@", "BSM"]) as cursor:
        for row in cursor:
            rec += 1
            row[1] = rec
            cursor.updateRow(row)
            print(rec)
