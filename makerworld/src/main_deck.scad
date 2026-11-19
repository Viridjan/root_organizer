
// ---- deck box (deck.sc): one piece, open top, same from front and back, label on all four sides ----
sel = [for (r = presets) if (r[0] == preset) r];
pr = len(sel) > 0 ? sel[0] : ["", side_label, card_stack_thickness];
W = box_width;
D = pr[2] + 2 * wall;
H = box_height;
c = chamfer;
sy = (W - slot_w) / 4;   // label centred in the strip beside the U
difference() {
    hull() {   // 45 deg chamfer on the 4 vertical and the 4 bottom edges
        linear_extrude(eps) offset(delta = -c) polygon(oct(D, W, c));
        extrude_z(c, H) polygon(oct(D, W, c));
    }
    translate([wall, (W - card_pocket_width) / 2, H - card_pocket_height]) cube([pr[2], card_pocket_width, card_pocket_height + 1]);
    translate([-1, 0, 0]) extrude_x(D + 2) {   // U thumb cutout through both faces
        zc = H - slot_d + slot_w / 2;
        translate([W / 2 - slot_w / 2, zc]) square([slot_w, slot_d]);
        translate([W / 2, zc]) circle(slot_w / 2, $fn = 64);
    }
    engrave([D, 0, 0], [0, 1, 0], [0, 0, 1], [sy, H / 2], -90, pr[1], text_height);    // front
    engrave([0, W, 0], [0, -1, 0], [0, 0, 1], [sy, H / 2], -90, pr[1], text_height);   // back
    engrave([0, 0, 0], [1, 0, 0], [0, 0, 1], [D / 2, H / 2], -90, pr[1], text_height);  // end y = 0
    engrave([D, W, 0], [-1, 0, 0], [0, 0, 1], [D / 2, H / 2], -90, pr[1], text_height); // end y = W
}
