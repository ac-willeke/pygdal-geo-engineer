from osgeo import ogr


def import_gpkg(in_gpkg, layer_name, new_field_name):
    ds = ogr.Open(in_gpkg, 1)
    lyr = ds.GetLayerByName(layer_name)
    new_field_defn = ogr.FieldDefn(new_field_name, ogr.OFTInteger)
    if lyr.GetLayerDefn().GetFieldIndex(new_field_name) == -1:
        lyr.CreateField(new_field_defn)
    return ds, lyr


def print_layer_schema(lyr):
    print("Layer schema:")
    print("Name, Type, Width, Precision")
    for field in lyr.schema:
        print(field.name, field.type, field.width, field.precision)
