
// ---- card box ----
sel = [for (r = presets) if (r[0] == preset) r];
pr = len(sel) > 0 ? sel[0] : ["", side_label, top_label, card_stack_thickness, wood_depth];
depth = pr[4] + wall + lid_t;
cw = box_width - 2 * wall;
lid_w = box_width - 2 * lid_gap;
if (part != "lid") on_back(depth)
    box(depth, box_width, pr[4], [[wall, wall + cw]], pr[1], pr[1], pr[2], "", text_height, 0, slide_clearance);
if (part != "box") translate([1, part == "all" ? box_width + 10 : 0, 0])
    lid(cw, lid_w, 2 * wall + pr[3], slide_clearance, [pr[3], card_pocket_width, card_pocket_height], true,
        pr[1], lid_gap + (lid_w - slot_w) / 4);
