import arcpy

feature_class = r'D:\GZ\西藏入库\111类乌齐\111类乌齐\类乌齐草原确权数据库2023.gdb\ZDJBXXB'

output_class = feature_class + '_起点1'
# 检查要素类是否存在
if not arcpy.Exists(feature_class):
    print(f"要素类 {feature_class} 不存在。")
if arcpy.Exists(output_class):
    print(f"要素类 {output_class} 已存在，请改名或清除。")

# 检查要素类是否为面要素
desc = arcpy.Describe(feature_class)
if desc.shapeType != "Polygon":
    print("该函数仅支持 面 要素类。")

arcpy.management.CopyFeatures(feature_class, output_class)
number_rows = arcpy.management.GetCount(output_class)

with arcpy.da.UpdateCursor(output_class, ["OID@", "SHAPE@"]) as cursor:
    for row in cursor:
        geometry = row[1]
        x_min = geometry.extent.XMin
        y_max = geometry.extent.YMax
        # 获取外边界环
        exterior_ring = geometry.getPart(0)  # 假设面要素为单部分
        if exterior_ring is None:
            continue  # 如果没有外边界环，跳过
        # 将环转换为列表
        points = [pt for pt in exterior_ring]

        if not points:
            continue  # 如果没有顶点，跳过

        from math import sqrt
        def distance(pt1, pt2):
            return sqrt((pt1.X - pt2[0]) ** 2 + (pt1.Y - pt2[1]) ** 2)

        min_dist = float('inf')  # 表示正无穷大
        new_index = 0
        for i, pt in enumerate(points):
            dist = distance(pt, [x_min, y_max])
            if dist < min_dist:
                min_dist = dist
                new_index = i
        # 重新排列顶点顺序
        new_points = points[new_index:] + points[:new_index] + [points[new_index]]

        # 创建新的环
        new_exterior_ring = arcpy.Array([arcpy.Point(pt.X, pt.Y) for pt in new_points])
        # 创建新的面几何
        new_geometry = arcpy.Polygon(new_exterior_ring, spatial_reference=geometry.spatialReference)
        # 更新要素的几何
        row[1] = new_geometry
        cursor.updateRow(row)
        print('OID@ {:^5}|{:^5}'.format(str(row[0]), str(number_rows)))







