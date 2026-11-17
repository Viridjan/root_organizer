
// ---- Vagabond double box ----
cw = box_width - 2 * wall;
lid_w = box_width - 2 * lid_gap;
T1 = wood_depth1 + wall + lid_t;
T2 = wood_depth2 + wall + lid_t;
flangeA = 2 * wall + card_stack_thickness;
XA = T1 + flangeA;                       // where lid 2's tongue starts (assembled, box 1 at x 0)
xc = T1 + wall + card_stack_thickness / 2;  // card pocket centre

module half(depth, wood) box(depth, box_width, wood, [[wall, wall + cw]], side_label, side_label, top_label, "", text_height, 0, slide_clearance);

module shared_lid() difference() {
    intersection() {
        union() {
            translate([T1 - lid_t, 0, 0])
                lid(cw, lid_w, flangeA, slide_clearance, [card_stack_thickness, card_pocket_width, card_pocket_height], chamfered = false);
            translate([XA + lid_t, box_width, 0]) rotate([0, 0, 180]) lid(cw, lid_w, wall, slide_clearance, chamfered = false);
        }
        translate([-1, lid_gap, 0]) extrude_x(XA + lid_t + 2) polygon(oct(lid_w, lid_h, mid_chamfer));
    }
    translate([0, -1, 0]) rotate([-90, 0, 0]) linear_extrude(box_width + 2) {  // (x, -z) -> finger notches through y
        zc = box_height - notch_d + notch_w / 2;
        translate([xc - notch_w / 2, -box_height - 1]) square([notch_w, notch_d - notch_w / 2 + 1]);
        translate([xc, -zc]) circle(notch_w / 2, $fn = 48);
    }
    engrave([0, lid_gap, 0], [0, 0, -1], [1, 0, 0], [-box_height / 2, xc], 0, side_label, text_height);
    engrave([0, box_width - lid_gap, 0], [0, 0, -1], [-1, 0, 0], [-box_height / 2, -xc], 180, side_label, text_height);
}

if (part == "all" || part == "box1") on_back(T1) half(T1, wood_depth1);
if (part == "all" || part == "box2") translate([0, part == "all" ? box_width + 10 : 0, 0]) on_back(T2) half(T2, wood_depth2);
if (part == "all" || part == "lid") translate([-(T1 - lid_t) + 1, part == "all" ? 2 * (box_width + 10) : 0, 0]) shared_lid();
