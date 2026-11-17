// Root organizer: faction box with card lid
// A box for a faction's wooden pieces, with a sliding dovetail lid that holds the faction's
// cards in a pocket (thumb cutout to pull them out) and clicks shut. Engraved labels on both
// ends, the top and the lid. Boxes stand upright side by side in the game box.

/* [Preset] */
// A Root faction, or Custom to use the values below
preset = "Custom"; // [Custom, Marquise_de_Cat, Eyrie_Dynasties, Woodland_Alliance, Riverfolk_Company, Lizard_Cult, Underground_Duchy, Corvid_Conspiracy, Lord_of_the_Hundreds, Keepers_in_Iron, Lilypad_Diaspora, Twilight_Council, Knaves_of_the_Deepwood, Landmarks]

/* [Box] */
// Inside depth of the pocket for the wooden pieces (mm)
wood_depth = 23; // [5:0.5:60]
// Box width (mm)
box_width = 71.5; // [50:0.5:160]

/* [Cards] */
// Thickness of the card stack (sleeved), mm
card_stack_thickness = 0.7; // [0.5:0.1:20]
// Card pocket width (card width + clearance), mm
card_pocket_width = 67; // [40:0.5:150]
// Card pocket height (card length + clearance), mm
card_pocket_height = 91.5; // [40:0.5:97]

/* [Labels] */
// Label on both ends and on the lid; | starts a new line
side_label = "Marquise de Cat";
// Label on top; | starts a new line
top_label = "Cats";

/* [Fit] */
// Sliding clearance per side between lid and groove (mm)
slide_clearance = 0.2; // [0:0.05:0.5]
// Click bump height on the lid (0 = no click)
detent_height = 0.4; // [0:0.05:0.8]
/* [Text] */
// Any font from the MakerWorld font list; bold keeps strokes printable with a 0.6 mm nozzle
font = "Noto Sans:style=Bold"; // font
// Capital-letter height of the labels (mm)
text_height = 6; // [3:0.1:10]

/* [Print] */
// What to generate
part = "all"; // [all, box, lid]

/* [Hidden] */
// name, side label, top label, card stack, wood depth
presets = [
    ["Marquise_de_Cat", "Marquise de Cat", "Cats", 0.7, 23],
    ["Eyrie_Dynasties", "Eyrie Dynasties", "Eagles", 3.5, 16.5],
    ["Woodland_Alliance", "Woodland Alliance", "Alliance", 0.7, 14],
    ["Riverfolk_Company", "Riverfolk Company", "Otters", 0.7, 11.5],
    ["Lizard_Cult", "Lizard Cult", "Lizards", 0.7, 20.5],
    ["Underground_Duchy", "Underground Duchy", "Moles", 5.2, 19.5],
    ["Corvid_Conspiracy", "Corvid Conspiracy", "Corvids", 0.7, 14],
    ["Lord_of_the_Hundreds", "Lord of the|Hundreds", "Rats", 4.5, 23],
    ["Keepers_in_Iron", "Keepers in Iron", "Badgers", 2, 18.5],
    ["Lilypad_Diaspora", "Lilypad Diaspora", "Frogs", 9.2, 19],
    ["Twilight_Council", "Twilight Council", "Bats", 0.7, 20],
    ["Knaves_of_the_Deepwood", "Knaves of the|Deepwood", "Skunks", 8.5, 14],
    ["Landmarks", "Landmarks", "Landmarks", 5.5, 20],
];
top_text_height = text_height;

// ---- Root organizer geometry (shared by every MakerWorld entry; build.py inlines it) ----
// Ported from the SolidCraft designs: x = box depth (back wall at x 0, lid at x = depth),
// y = width, z = height (box standing upright). Parts are laid out for printing at the end.

wall = 1.5;            // every wall and floor
box_height = 100;
lid_t = 2.5;           // lid plate (dovetail tongue) thickness
lid_gap = 0.15;        // gap on each side of the lid flange
lid_trim = 0.15;       // lid is this much shorter than the box
dovetail = 60;         // dovetail angle
stop_w = 5;            // lid stop feet at the bottom of the groove
chamfer = 1;           // 45 deg chamfer on outer edges
text_depth = 0.5;
line_pitch = 1.166;    // line spacing, in capital heights
cap_ratio = 0.992;     // capital height / OpenSCAD text size for Noto Sans Bold
slot_w = 30;           // U thumb cutout in card lids
slot_d = 38;
detent_r = 1;
detent_drop = 5;       // click bump centre below the lid top

lid_h = box_height - lid_trim;
dovo = lid_t / tan(dovetail);
stop_h = wall + stop_w * tan(dovetail);
eps = 0.01;
$fn = 24;

// ---- helpers ----
// 2D profile drawn in (y, z), extruded along +x from x 0 to h.
module extrude_x(h) multmatrix([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0]]) linear_extrude(h) children();
module extrude_z(z0, z1) translate([0, 0, z0]) linear_extrude(z1 - z0) children();

function oct(w, h, c) = [[c, 0], [w - c, 0], [w, c], [w, h - c], [w - c, h], [c, h], [0, h - c], [0, c]];

// Cuboid [l, w, h] chamfered on its 4 x-direction edges and the 4 edges of the x = 0 face.
module chamfer_block(l, w, h, c = chamfer) hull() {
    translate([c, 0, 0]) extrude_x(l - c) polygon(oct(w, h, c));
    extrude_x(eps) offset(delta = -c) polygon(oct(w, h, c));
}

// "A|B" -> ["A", "B"] (| = line break in labels)
function _join(l, i = 0) = i >= len(l) ? "" : str(l[i], _join(l, i + 1));
function _sub(s, a, b) = b > a ? _join([for (i = [a : b - 1]) s[i]]) : "";
function lines(s) = let(cut = [for (i = [0 : len(s) - 1]) if (s[i] == "|") i], ends = concat([-1], cut, [len(s)]))
    len(s) == 0 ? [] : [for (k = [0 : len(ends) - 2]) _sub(s, ends[k] + 1, ends[k + 1])];

// Lines centred: horizontally, and vertically halfway between the first cap top and the last baseline.
module label2d(s, h) {
    l = lines(s);
    n = len(l);
    y0 = ((n - 1) * line_pitch * h - h) / 2;
    for (i = [0 : n - 1]) translate([0, y0 - i * line_pitch * h])
        text(l[i], size = h / cap_ratio, font = font, halign = "center", valign = "baseline");
}

// Engrave a label into the plane through o with axes u, v (normal u x v points out of the material).
module engrave(o, u, v, at, angle, s, h) if (len(s) > 0) {
    n = cross(u, v);
    multmatrix([[u.x, v.x, n.x, o.x], [u.y, v.y, n.y, o.y], [u.z, v.z, n.z, o.z]])
        translate([at.x, at.y, -text_depth]) linear_extrude(text_depth + 1) rotate(angle) label2d(s, h);
}

// ---- box ----
// comps: [[y start, y end], ...] of each compartment's inside.
module box(depth, width, wood, comps, near, far, top1, top2 = "", top_h, top_offset = 0, clearance) {
    off = clearance + detent_r - detent_height;
    difference() {
        intersection() {
            chamfer_block(depth, width, box_height);
            union() {
                difference() {
                    cube([depth, width, box_height]);
                    for (c = comps) {
                        translate([wall, c[0], wall]) cube([wood + eps, c[1] - c[0], box_height - 2 * wall]);
                        extrude_z(-1, box_height + 1) polygon([[depth - lid_t, c[0]], [depth, c[0] + dovo], [depth + 1, c[0] + dovo],
                            [depth + 1, c[1] - dovo], [depth, c[1] - dovo], [depth - lid_t, c[1]]]);
                    }
                }
                for (c = comps) translate([depth - lid_t - eps, 0, 0]) extrude_x(lid_t + eps) {
                    polygon([[c[0] - wall, -1], [c[0] - wall, stop_h], [c[0], stop_h], [c[0] + stop_w, wall], [c[0] + stop_w, -1]]);
                    polygon([[c[1] + wall, -1], [c[1] + wall, stop_h], [c[1], stop_h], [c[1] - stop_w, wall], [c[1] - stop_w, -1]]);
                }
            }
        }
        if (detent_height > 0) for (c = comps, y = [c[0] + dovo / 2 + sin(dovetail) * off, c[1] - dovo / 2 - sin(dovetail) * off])
            translate([depth - lid_t / 2 - cos(dovetail) * off, y, lid_h - detent_drop]) sphere(detent_r);
        engrave([0, 0, 0], [0, 0, -1], [1, 0, 0], [-box_height / 2, depth / 2 + text_height * 0.12], 0, near, text_height);
        engrave([0, width, 0], [0, 0, -1], [-1, 0, 0], [-box_height / 2, -depth / 2 - text_height * 0.12], 180, far, text_height);
        tx = (depth - lid_t) / 2 + top_h * 0.12;
        engrave([0, 0, box_height], [1, 0, 0], [0, 1, 0], [tx + (top2 == "" ? 0 : top_offset), width / 2], -90, top1, top_h);
        engrave([0, 0, box_height], [1, 0, 0], [0, 1, 0], [tx - top_offset, width / 2], -90, top2, top_h);
    }
}

// ---- lid ----
// Tongue for a compartment of inside width cw (lid frame: tongue x 0..lid_t, flange beyond).
// card = [stack thickness, pocket width, pocket height] or undef; label_y: label position across the lid.
module lid(cw, lid_w, flange, clearance, card = undef, slot = false, label = "", label_y, chamfered = true) {
    a = wall; b = wall + cw; yc = a + cw / 2;
    scy = clearance / sin(dovetail);
    off = clearance + detent_r - detent_height;
    face = lid_t + flange;
    union() {
        difference() {
            union() {
                difference() {
                    extrude_z(0, lid_h) polygon([[0, a + scy], [lid_t + eps, a + dovo + scy], [lid_t + eps, b - dovo - scy], [0, b - scy]]);
                    translate([-1, 0, 0]) extrude_x(lid_t + 1) {
                        polygon([[a - wall - 1, -1], [a - wall - 1, stop_h], [a, stop_h], [a + stop_w, wall],
                            [a + stop_w + clearance, wall - clearance * tan(dovetail)], [a + stop_w + clearance, -1]]);
                        polygon([[b + wall + 1, -1], [b + wall + 1, stop_h], [b, stop_h], [b - stop_w, wall],
                            [b - stop_w - clearance, wall - clearance * tan(dovetail)], [b - stop_w - clearance, -1]]);
                    }
                }
                translate([face, yc - lid_w / 2, 0]) mirror([1, 0, 0])
                    if (chamfered) chamfer_block(flange, lid_w, lid_h); else cube([flange, lid_w, lid_h]);
            }
            if (card != undef) {
                translate([lid_t + wall, yc - card[1] / 2, box_height - card[2]]) cube([card[0], card[1], card[2] + 1]);
                if (slot) translate([face - wall - card[0] / 2, 0, 0]) extrude_x(wall + card[0] / 2 + 1) {
                    zc = box_height - slot_d + slot_w / 2;
                    translate([yc - slot_w / 2, zc]) square([slot_w, slot_d]);
                    translate([yc, zc]) circle(slot_w / 2, $fn = 64);
                }
            }
            engrave([face, 0, 0], [0, 1, 0], [0, 0, 1], [label_y, box_height / 2], -90, label, text_height);
        }
        if (detent_height > 0) for (y = [a + dovo / 2 + sin(dovetail) * off, b - dovo / 2 - sin(dovetail) * off])
            translate([lid_t / 2 - cos(dovetail) * off, y, lid_h - detent_drop]) sphere(detent_r);
    }
}

// ---- print layout ----
// Box on its back (x -> z), lids standing upright beside it.
module on_back(depth) translate([box_height, 0, 0]) rotate([0, -90, 0]) children();

// ---- card box ----
sel = [for (r = presets) if (r[0] == preset) r];
pr = len(sel) > 0 ? sel[0] : ["", side_label, top_label, card_stack_thickness, wood_depth];
depth = pr[4] + wall + lid_t;
cw = box_width - 2 * wall;
lid_w = box_width - 2 * lid_gap;
if (part != "lid") on_back(depth)
    box(depth, box_width, pr[4], [[wall, wall + cw]], pr[1], pr[1], pr[2], "", top_text_height, 0, slide_clearance);
if (part != "box") translate([1, part == "all" ? box_width + 10 : 0, 0])
    lid(cw, lid_w, 2 * wall + pr[3], slide_clearance, [pr[3], card_pocket_width, card_pocket_height], true,
        pr[1], lid_gap + (lid_w - slot_w) / 4);
