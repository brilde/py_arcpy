import arcpy

feature_class = r'D:\GZ\西藏入库\类乌齐草原确权数据库2023.gdb\ZDJBXXB'

def distance(pt1, pt2):
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5

if not arcpy.Exists(feature_class):
    print(f"要素类 {feature_class} 不存在。")

# 检查要素类是否为面要素
desc = arcpy.Describe(feature_class)
if desc.shapeType != "Polygon":
    print("该函数仅支持 面 要素类。")

output_class = feature_class + '_起点1'

arcpy.management.CopyFeatures(feature_class, output_class)

number_rows = arcpy.management.GetCount(feature_class)
with arcpy.da.UpdateCursor(output_class, ["OID@", "Shape@"]) as cursor:
    for row in cursor:
        xy_nw = [row[1].extent.XMin, row[1].extent.YMax]
        # print(xy_nw)
        result = []
        for part in row[1]:
            current = []
            for i, pt in enumerate(part):
                if pt:
                    current.append([pt.X, pt.Y])
                else:
                    result.append(current)
                    current = []
            if current:
                result.append(current)
        rings = []
        for resu in result:

            min_dist = float('inf')  # 表示正无穷大
            new_index = 0
            for i, pt in enumerate(resu):
                dist = distance(pt, xy_nw)
                if dist < min_dist:
                    min_dist = dist
                    new_index = i
            # 重新排列顶点顺序
            new_points = resu[new_index:] + resu[:new_index] + [resu[new_index]]
            ring = arcpy.Array([arcpy.Point(*p) for p in new_points])
            rings.append(ring)

        row[1] = arcpy.Polygon(arcpy.Array(rings))
        cursor.updateRow(row)
        print('OID@ {:^5}|{:^5}'.format(str(row[0]), str(number_rows)))



