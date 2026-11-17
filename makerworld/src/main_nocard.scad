
// ---- plain box ----
sel = [for (r = presets) if (r[0] == preset) r];
pr = len(sel) > 0 ? sel[0] : ["", side_label, top_label, box_width, wood_depth];
W = pr[3];
depth = pr[4] + wall + lid_t;
cw = W - 2 * wall;
if (part != "lid") on_back(depth)
    box(depth, W, pr[4], [[wall, wall + cw]], pr[1], pr[1], pr[2], "", text_height, 0, slide_clearance);
if (part != "box") translate([1, part == "all" ? W + 10 : 0, 0])
    lid(cw, W - 2 * lid_gap, wall, slide_clearance, label = pr[1], label_y = wall + cw / 2);
