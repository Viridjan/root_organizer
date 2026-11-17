
// ---- two-compartment box ----
sel = [for (r = presets) if (r[0] == preset) r];
pr = len(sel) > 0 ? sel[0] : ["", near_label, far_label, lid2_label, top_line1, top_line2, top_text_height, wood_depth, compartment_split];
depth = pr[7] + wall + lid_t;
inner = box_width - 3 * wall;
cw1 = inner * pr[8];
cw2 = inner - cw1;
if (part == "all" || part == "box") on_back(depth)
    box(depth, box_width, pr[7], [[wall, wall + cw1], [2 * wall + cw1, box_width - wall]], pr[1], pr[2], pr[4], pr[5],
        pr[6], pr[6] * 0.8, slide_clearance);
if (part == "all" || part == "lid1") translate([1, part == "all" ? box_width + 10 : 0, 0])
    lid(cw1, cw1 + wall - 2 * lid_gap, wall, slide_clearance, label = pr[1], label_y = wall + cw1 / 2);
if (part == "all" || part == "lid2") translate([part == "all" ? 15 : 1, part == "all" ? box_width + 10 : 0, 0])
    lid(cw2, cw2 + wall - 2 * lid_gap, wall, slide_clearance, label = pr[3] == "" ? pr[2] : pr[3], label_y = wall + cw2 / 2);
