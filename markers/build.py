"""Bambu Studio project for the frog clearing marker: COUNT copies on one A1 plate, each one object
with two parts, Body in Bright Green and Details (bands + frog head) in White.

usage: python3 markers/build.py markers/frog_marker.3mf <out.3mf>   (then re-save it with the Bambu CLI, see CLAUDE.md)
"""
import json, os, sys, uuid, zipfile
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".bambu"))
from plates import BED, FILAMENTS, NS, mesh_xml, project_settings

COUNT = 4                                   # as the original marker files: 4 per plate
PARTS = {"Body": "Bright Green", "Details": "White"}
GAP = 8.0

root = ET.fromstring(zipfile.ZipFile(sys.argv[1]).read("3D/3dmodel.model"))
parts = {}
for o in root.iter(f"{{{NS}}}object"):
    if o.get("name") in PARTS:
        parts[o.get("name")] = ([tuple(float(v.get(k)) for k in "xyz") for v in o.iter(f"{{{NS}}}vertex")],
                                [tuple(int(t.get(k)) for k in ("v1", "v2", "v3")) for t in o.iter(f"{{{NS}}}triangle")])
assert set(parts) == set(PARTS), parts.keys()
allv = [v for vs, _ in parts.values() for v in vs]
lo = [min(v[i] for v in allv) for i in range(3)]
size = [max(v[i] for v in allv) - lo[i] for i in range(3)]
parts = {n: ([tuple(v[i] - lo[i] for i in range(3)) for v in vs], ts) for n, (vs, ts) in parts.items()}  # shared frame, min corner at 0

cols = 2
rows = -(-COUNT // cols)
x0 = (BED - (cols * size[0] + (cols - 1) * GAP)) / 2
y0 = (BED - (rows * size[1] + (rows - 1) * GAP)) / 2
files, objs, items, cfg, inst = {}, [], [], [], []
oid = 0
for k in range(COUNT):
    obj_id = oid = oid + 1
    comps, cparts = [], []
    for name, (vs, ts) in parts.items():
        oid += 1
        path = f"3D/Objects/object_{oid}.model"
        files[path] = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="{NS}" '
                       'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">'
                       f'<resources><object id="{oid}" p:UUID="{uuid.uuid4()}" type="model">{mesh_xml(vs, ts)}</object>'
                       '</resources><build/></model>')
        comps.append(f'<component p:path="/{path}" objectid="{oid}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>')
        cparts.append(f'<part id="{oid}" subtype="normal_part"><metadata key="name" value="{name}"/>'
                      '<metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>'
                      f'<metadata key="extruder" value="{list(FILAMENTS).index(PARTS[name]) + 1}"/></part>')
    objs.append(f'<object id="{obj_id}" p:UUID="{uuid.uuid4()}" type="model"><components>{"".join(comps)}</components></object>')
    x = x0 + (k % cols) * (size[0] + GAP)
    y = y0 + (k // cols) * (size[1] + GAP)
    items.append(f'<item objectid="{obj_id}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 {x:.4f} {y:.4f} 0" printable="1"/>')
    cfg.append(f'<object id="{obj_id}"><metadata key="name" value="Frog marker {k + 1}"/>'
               f'<metadata key="extruder" value="{list(FILAMENTS).index(PARTS["Body"]) + 1}"/>'
               f'<metadata key="brim_type" value="no_brim"/>{"".join(cparts)}</object>')
    inst.append(f'<model_instance><metadata key="object_id" value="{obj_id}"/><metadata key="instance_id" value="0"/>'
                f'<metadata key="identify_id" value="{obj_id}"/></model_instance>')
assert x0 >= 10 and y0 >= 10, "markers don't fit the plate"

model = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="{NS}" '
         'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
         'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">'
         '<metadata name="Application">BambuStudio-02.09.01.00</metadata><metadata name="BambuStudio:3mfVersion">1</metadata>'
         f'<metadata name="Title">Frog clearing marker</metadata><resources>{"".join(objs)}</resources>'
         f'<build p:UUID="{uuid.uuid4()}">{"".join(items)}</build></model>')
config = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>' + "".join(cfg)
          + '<plate><metadata key="plater_id" value="1"/><metadata key="plater_name" value="Frog markers"/>'
          + f'<metadata key="locked" value="false"/>{"".join(inst)}</plate></config>')
rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(f'<Relationship Target="/{p}" Id="rel-{i + 1}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
                  for i, p in enumerate(files)) + "</Relationships>")
with zipfile.ZipFile(sys.argv[2], "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
               '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
               '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
               '<Default Extension="png" ContentType="image/png"/></Types>')
    z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    z.writestr("3D/3dmodel.model", model)
    z.writestr("3D/_rels/3dmodel.model.rels", rels)
    for p, body in files.items():
        z.writestr(p, body)
    z.writestr("Metadata/model_settings.config", config)
    z.writestr("Metadata/project_settings.config", json.dumps(project_settings(), indent=4))
print(f"{COUNT} markers, {size[0]:.1f} x {size[1]:.1f} x {size[2]:.2f} mm each")
