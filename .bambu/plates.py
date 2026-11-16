"""Merge the per-box 3MFs into one Bambu Studio project with several A1 plates.

usage: python3 plates.py <dir with NN_name.3mf> <out.3mf>
"""
import glob, json, math, os, re, sys, uuid, zipfile
import xml.etree.ElementTree as ET

BED = 256.0          # Bambu Lab A1 bed, mm
MARGIN = 10.0        # keep off the bed edge (user: 1+ cm)
LIDS_ONE_PLATE = {"Black"}   # user: all black lids on one plate
MAX_PARTS = 5        # per plate, so plates stay balanced (a colour with more parts gets more plates)
MIN_GAP = 8.0        # between parts at least; layout() spreads them evenly over the plate
PLATE_GAP = 0.2      # BambuStudio LOGICAL_PART_PLATE_GAP: plate stride = BED * 1.2
LID_LABELS = {"dice_tokens": ["Dice", "Tokens"]}  # lid i+1 > 1 comes from NN_<key>_lid<i+1>.3mf
LIDS = {"dice_tokens": 2, "hirelings_2": 2, "hirelings_3": 3}  # one lid per compartment
# Plates are per colour (any container type); TYPES only lists what is printed (hirelings 2/3: leftovers).
# Hireling "a__b" keys: two half-width hirelings in one faction-width box (divided.sc rows "A + B"),
# lid 1 = a, lid 2 = b from NN_a__b_lid2.3mf; pairs chosen for contrasting, non-repeating lid colours.
TYPES = {
    "general": ["clearings", "landmarks", "dice_tokens", "hirelings_cards"],  # dice, tokens: not printed (dice_tokens holds both)
    "factions": ["corvid_conspiracy", "eyrie_dynasties", "keepers_in_iron", "knaves_of_the_deepwood", "lilypad_diaspora",
                 "lizard_cult", "lord_of_the_hundreds", "marquise_de_cat", "riverfolk_company", "twilight_council",
                 "underground_duchy", "vagabond_double", "woodland_alliance"],  # vagabond + vagabond_2: one double box (vagabond_double.sc)
    "hireling": ["singletons", "corvid_spies__warm_sun_prophets", "last_dynasty__forest_patrol",
                 "flame_bearers__river_roamers", "spring_uprising__sunward_expedition",
                 "highway_bandits__sunny_advocates", "popular_band__vault_keepers", "prosperous_farmers"],
}
NS = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"
# Bambu PLA Basic colours. White: hireling boxes and Singletons lid; Black: general boxes and lids.
FILAMENTS = {"White": "#FFFFFF", "Orange": "#FF6A13", "Blue": "#0A2989", "Cyan": "#0086D6", "Green": "#00AE42",
             "Bright Green": "#BECF00", "Purple": "#5E43B7", "Red": "#C12E1F", "Yellow": "#F4EE2A",
             "Gray": "#8E9089", "Silver": "#A6A9AA", "Brown": "#9D432C", "Black": "#000000",
             "Pink": "#F55A74", "Beige": "#F7E6DE"}
# Official colours (therootdatabase.com/color/...). Factions: box + lid; hirelings: lid only.
# Same-colour factions told apart: Riverfolk Cyan vs Eyrie Blue, Lilypad Bright Green vs Alliance Green,
# Keepers Silver vs Vagabond Gray.
COLOURS = {"marquise_de_cat": "Orange", "eyrie_dynasties": "Blue", "riverfolk_company": "Cyan",
           "woodland_alliance": "Green", "lilypad_diaspora": "Bright Green", "corvid_conspiracy": "Purple",
           "lord_of_the_hundreds": "Red", "lizard_cult": "Yellow", "keepers_in_iron": "Silver",
           "vagabond_double": "Gray", "twilight_council": "Brown", "knaves_of_the_deepwood": "Black",
           "underground_duchy": "Beige",
           "forest_patrol": "Orange", "last_dynasty": "Blue", "river_roamers": "Green", "spring_uprising": "Green",
           "corvid_spies": "Purple", "flame_bearers": "Red", "prosperous_farmers": "Yellow",
           "warm_sun_prophets": "Yellow", "vault_keepers": "Gray", "sunny_advocates": "Brown",
           "highway_bandits": "Pink", "popular_band": "Pink", "sunward_expedition": "Beige"}


def read_parts(path):
    root = ET.fromstring(zipfile.ZipFile(path).read("3D/3dmodel.model"))
    parts = {}
    for o in root.iter(f"{{{NS}}}object"):
        vs = [tuple(float(v.get(k)) for k in "xyz") for v in o.iter(f"{{{NS}}}vertex")]
        ts = [tuple(int(t.get(k)) for k in ("v1", "v2", "v3")) for t in o.iter(f"{{{NS}}}triangle")]
        lo = [min(v[i] for v in vs) for i in range(3)]
        vs = [tuple(v[i] - lo[i] for i in range(3)) for v in vs]  # min corner at origin
        size = [max(v[i] for v in vs) for i in range(3)]
        parts[o.get("name")] = (vs, ts, size)
    return parts


# Proper rotations putting -z, +z, -x, +x, -y, +y on the bed.
ROTATIONS = [((1, 0, 0), (0, 1, 0), (0, 0, 1)), ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
             ((0, 0, -1), (0, 1, 0), (1, 0, 0)), ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
             ((1, 0, 0), (0, 0, -1), (0, 1, 0)), ((1, 0, 0), (0, 0, 1), (0, -1, 0))]
OVERHANG = -math.cos(math.radians(45)) - 1e-3   # face normal z below this needs support (45 deg chamfers don't)


def overhang_area(vs, ts):
    """Area of downward faces steeper than 45 deg from vertical, not lying on the bed."""
    area = 0.0
    for a, b, c in ts:
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = vs[a], vs[b], vs[c]
        ux, uy, uz, wx, wy, wz = bx - ax, by - ay, bz - az, cx - ax, cy - ay, cz - az
        nx, ny, nz = uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx
        n = math.sqrt(nx * nx + ny * ny + nz * nz)
        if n and nz / n < OVERHANG and max(az, bz, cz) > 1e-3:
            area += n / 2
    return area


def orient(p):
    """Rotate the part onto the face that leaves the least overhang (ties: the lowest)."""
    best = None
    for r in ROTATIONS:
        vs = [tuple(sum(r[i][j] * v[j] for j in range(3)) for i in range(3)) for v in p["vs"]]
        lo = [min(v[i] for v in vs) for i in range(3)]
        vs = [tuple(v[i] - lo[i] for i in range(3)) for v in vs]
        size = [max(v[i] for v in vs) for i in range(3)]
        score = (round(overhang_area(vs, p["ts"])), size[2])
        if best is None or score < best[0]:
            best = (score, vs, size)
    p["overhang"], p["vs"], p["size"] = best[0][0], best[1], best[2]


def cols_for(n):  # BambuStudio compute_colum_count
    v = math.sqrt(n)
    r = round(v)
    return r + 1 if v > r else r


def spread(sizes):
    """Positions along one plate axis for parts of these sizes: equal spaces between them and at
    both ends (space-evenly), or MARGIN at the ends when that would leave less. Returns (positions,
    smallest gap between parts) or None when they do not fit MIN_GAP apart."""
    free = BED - sum(sizes)
    n = len(sizes)
    if free - 2 * MARGIN < MIN_GAP * (n - 1) - 1e-9:
        return None
    gap = free / (n + 1)
    edge = gap
    if gap < MARGIN:
        edge, gap = MARGIN, (free - 2 * MARGIN) / (n - 1)
    pos, x = [], edge
    for w in sizes:
        pos.append(x)
        x += w + gap
    return pos, (gap if n > 1 else edge)


def layout(groups, per_row):
    """Rows of at most per_row parts (tallest first), spread evenly over the bed in x and y.
    Returns ([(part, x, y)], smallest gap) or None when it does not fit."""
    parts = sorted((p for g in groups for p in g), key=lambda p: -p["size"][1])
    rows, cur = [], []
    for p in parts:
        if cur and (len(cur) >= per_row or not spread([q["size"][0] for q in cur + [p]])):
            rows.append(cur); cur = []
        cur.append(p)
    rows.append(cur)
    heights = [max(p["size"][1] for p in r) for r in rows]
    ys = spread(heights)
    if not ys:
        return None
    out, gaps = [], [ys[1]]
    for r, h, y in zip(rows, heights, ys[0]):
        xs = spread([p["size"][0] for p in r])
        if not xs:
            return None
        gaps.append(xs[1])
        out += [(p, x, y + (h - p["size"][1]) / 2) for p, x in zip(r, xs[0])]
    return out, min(gaps)


def best_layout(groups):
    """The row length that leaves the widest smallest gap."""
    n = sum(map(len, groups))
    lays = [lay for k in range(1, n + 1) if (lay := layout(groups, k))]
    return max(lays, key=lambda l: l[1])[0] if lays else None


def deal(parts, cap):
    """The fewest plates (at most `cap` parts each) the parts fit on, dealt out so each plate gets
    the same number (and about the same area), each laid out with the widest gap that fits."""
    area = lambda q: q["size"][0] * q["size"][1]
    for n in range(-(-len(parts) // cap), len(parts) + 1):
        bins = [[] for _ in range(n)]
        for q in sorted(parts, key=area, reverse=True):   # largest part to the emptiest plate
            min(bins, key=lambda b: (len(b), sum(area(r[0]) for r in b))).append([q])
        placed = [best_layout(b) for b in bins]
        if all(placed):
            return placed
    raise SystemExit(f"{parts[0]['name']}: does not fit on a plate")


def pack(groups):
    """One colour per plate, parts dealt out evenly (deal). Colours in LIDS_ONE_PLATE: all lids on
    one plate, the boxes dealt out on their own.
    groups: [(colour, parts)]. Returns ([[(part, x, y)]], [colour per plate])."""
    by_colour = {}
    for c, parts in groups:
        by_colour.setdefault(c, []).extend(parts)
    plates, kinds = [], []
    for c, parts in by_colour.items():
        if c in LIDS_ONE_PLATE:
            lids = [p for p in parts if " - lid" in p["name"]]
            placed = deal([p for p in parts if p not in lids], MAX_PARTS) + deal(lids, len(lids))
            assert len(placed[-1]) == len(lids), f"{c}: lids do not fit on one plate"
        else:
            placed = deal(parts, MAX_PARTS)
        plates += placed
        kinds += [c] * len(placed)
    return plates, kinds


def project_settings():
    """Flattened A1 profiles (.bambu/*.json) with one PLA Basic filament per FILAMENTS entry."""
    here = os.path.dirname(os.path.abspath(__file__))
    cfg = {}
    for n in ("machine", "process", "filament"):
        cfg.update(json.load(open(os.path.join(here, f"{n}.json"))))
    fil = json.load(open(os.path.join(here, "filament.json")))
    for k, v in fil.items():   # per-filament settings: one entry per filament
        if isinstance(v, list) and len(v) == 1:
            cfg[k] = v * len(FILAMENTS)
    cfg["filament_colour"] = list(FILAMENTS.values())
    # Per-filament keys the Bambu CLI adds with a single entry; the GUI rejects the project
    # ("Invalid configuration file") unless every per-filament list has one entry per filament.
    n = len(FILAMENTS)
    for k, v in {"filament_change_length_nc": "10", "filament_idle_travel_cooling_enabled": "1",
                 "filament_is_mixed": "0", "filament_map": "1", "filament_map_2": "1",
                 "filament_mixed_components": "", "filament_mixed_gradient": "0",
                 "filament_mixed_gradient_curve": "", "filament_mixed_gradient_per_part": "0",
                 "filament_mixed_gradient_range": "", "filament_mixed_sublayer_ratios": "",
                 "filament_nozzle_map": "1", "filament_prime_tower_speed_factor_curve": "",
                 "filament_retract_length_toolchange": "nil", "filament_retract_restart_extra_toolchange": "nil",
                 "filament_volume_map": "0"}.items():
        cfg[k] = [v] * n
    cfg["filament_self_index"] = [str(i + 1) for i in range(n)]
    return cfg


def mesh_xml(vs, ts):
    v = "".join(f'<vertex x="{a:.5f}" y="{b:.5f}" z="{c:.5f}"/>' for a, b, c in vs)
    t = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in ts)
    return f"<mesh><vertices>{v}</vertices><triangles>{t}</triangles></mesh>"


def main(src, out):
    files_by_key = {re.sub(r"^\d+_", "", os.path.basename(f)[:-4]): f
                    for f in glob.glob(os.path.join(src, "*.3mf"))}
    groups = []
    for kind, keys in TYPES.items():
      for key in keys:
        f = files_by_key[key]
        title = key.replace("_", " ").title()
        parts = read_parts(f)
        pair = key.split("__")   # merged hireling box: one lid per hireling
        if len(pair) == 2:
            LIDS[key], LID_LABELS[key] = 2, [k.replace("_", " ").title() for k in pair]
            title = " + ".join(LID_LABELS[key])
        box_names = sorted(n for n in parts if n.startswith("Box"))  # vagabond_double has two: Box, Box (2)
        boxes = [{"name": f"{title} - box" + (f" {i + 1}" if len(box_names) > 1 else ""),
                  **dict(zip(("vs", "ts", "size"), parts[n]))} for i, n in enumerate(box_names)]
        n = LIDS.get(key, 1)
        lids = [{"name": f"{title} - lid" + (f" {i + 1}" if n > 1 else ""),
                 **dict(zip(("vs", "ts", "size"), parts["Lid"]))} for i in range(n)]
        for i, label in enumerate(LID_LABELS.get(key, [])):
            lids[i]["name"] = f"{title} - lid {label}"
            extra = files_by_key.get(f"{key}_lid{i + 1}")   # differently labelled lid, exported on its own
            if extra:
                lids[i].update(zip(("vs", "ts", "size"), read_parts(extra)["Lid"]))
        for p in boxes + lids:
            orient(p)
        plain = "Black" if kind == "general" else "White"   # colour of parts without an official one
        lid_colours = [COLOURS.get(k, plain) for k in pair] if len(pair) == 2 else [COLOURS.get(key, plain)] * n
        for p, c in zip(lids, lid_colours):
            p["colour"] = c
        for b in boxes:   # hirelings: colour on the lid only
            b["colour"] = "White" if kind == "hireling" else COLOURS.get(key, plain)
        for c in dict.fromkeys(p["colour"] for p in boxes + lids):   # a box stays with its same-colour lids
            groups.append((c, [p for p in boxes + lids if p["colour"] == c]))
    for _, parts in groups:
        for p in parts:
            p["filament"] = list(FILAMENTS).index(p["colour"]) + 1
    # one colour after another; within a colour, tallest footprint first (first-fit decreasing shelves)
    groups.sort(key=lambda g: (list(FILAMENTS).index(g[0]), -max(p["size"][1] for p in g[1])))
    plates, kinds = pack(groups)
    cols = cols_for(len(plates))

    files, items, objs, plate_cfg = {}, [], [], []
    oid = 0
    for pi, plate in enumerate(plates):
        ox = (pi % cols) * BED * (1 + PLATE_GAP)
        oy = -(pi // cols) * BED * (1 + PLATE_GAP)
        inst = []
        for p, x, y in plate:
            mesh_id, obj_id = oid + 1, oid + 2
            oid += 2
            path = f"3D/Objects/object_{mesh_id}.model"
            files[path] = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
                           f'xmlns="{NS}" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
                           f'requiredextensions="p"><resources><object id="{mesh_id}" p:UUID="{uuid.uuid4()}" type="model">'
                           f'{mesh_xml(p["vs"], p["ts"])}</object></resources><build/></model>')
            objs.append(f'<object id="{obj_id}" p:UUID="{uuid.uuid4()}" type="model"><components>'
                        f'<component p:path="/{path}" objectid="{mesh_id}" p:UUID="{uuid.uuid4()}" '
                        f'transform="1 0 0 0 1 0 0 0 1 0 0 0"/></components></object>')
            items.append(f'<item objectid="{obj_id}" p:UUID="{uuid.uuid4()}" '
                         f'transform="1 0 0 0 1 0 0 0 1 {ox + x:.4f} {oy + y:.4f} 0" printable="1"/>')
            name = p["name"].replace("&", "&amp;")
            plate_cfg.append(None)
            inst.append(f'<model_instance><metadata key="object_id" value="{obj_id}"/>'
                        f'<metadata key="instance_id" value="0"/><metadata key="identify_id" value="{obj_id}"/></model_instance>')
            objs[-1] = (objs[-1], obj_id, mesh_id, name, p["filament"])
        plate_cfg[-1] = (pi, inst)
    plate_cfg = [c for c in plate_cfg if c]

    model = (f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" xmlns="{NS}" '
             'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
             'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">'
             '<metadata name="Application">BambuStudio-02.09.01.00</metadata>'
             '<metadata name="BambuStudio:3mfVersion">1</metadata>'
             f'<metadata name="Title">Root organizer</metadata><resources>{"".join(o[0] for o in objs)}</resources>'
             f'<build p:UUID="{uuid.uuid4()}">{"".join(items)}</build></model>')
    cfg = ['<?xml version="1.0" encoding="UTF-8"?>\n<config>']
    for _, obj_id, mesh_id, name, fil in objs:
        cfg.append(f'<object id="{obj_id}"><metadata key="name" value="{name}"/><metadata key="extruder" value="{fil}"/>'
                   f'<part id="{mesh_id}" subtype="normal_part"><metadata key="name" value="{name}"/>'
                   '<metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/></part></object>')
    for pi, inst in plate_cfg:
        cfg.append(f'<plate><metadata key="plater_id" value="{pi + 1}"/><metadata key="plater_name" value="{kinds[pi]}"/>'
                   f'<metadata key="locked" value="false"/>{"".join(inst)}</plate>')
    cfg.append("</config>")

    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(f'<Relationship Target="/{p}" Id="rel-{i + 1}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>'
                      for i, p in enumerate(files)) + "</Relationships>")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
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
        z.writestr("Metadata/model_settings.config", "\n".join(cfg))
        z.writestr("Metadata/project_settings.config", json.dumps(project_settings(), indent=4))

    # self-check: every part inside its plate, none overlapping on a plate
    for pi, plate in enumerate(plates):
        rects = [(x, y, x + p["size"][0], y + p["size"][1]) for p, x, y in plate]
        assert all(MARGIN - 1e-6 <= a and c <= BED - MARGIN + 1e-6 and MARGIN - 1e-6 <= b and d <= BED - MARGIN + 1e-6
                   for a, b, c, d in rects), f"plate {pi + 1} overflow"
        sep = [max(s[0] - r[2], r[0] - s[2], s[1] - r[3], r[1] - s[3]) for i, r in enumerate(rects) for s in rects[i + 1:]]
        assert min(sep, default=MIN_GAP) >= MIN_GAP - 1e-6, f"plate {pi + 1} parts too close"
        edge = min(min(a, b, BED - c, BED - d) for a, b, c, d in rects)
        print(f"plate {pi + 1} [{kinds[pi]}]: {len(plate)} parts, gap {min(sep, default=0):.0f}, edge {edge:.0f} mm:",
              ", ".join(f'{p["name"]} (h {p["size"][2]:.0f}, overhang {p["overhang"]} mm2)' for p, _, _ in plate))


if __name__ == "__main__":
    main(*sys.argv[1:3])
