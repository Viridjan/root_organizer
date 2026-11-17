// Root organizer: two-compartment box
// A box split into two compartments, each with its own sliding dovetail lid that clicks shut.
// Engraved labels: one compartment's name on each end and on its lid, both on top.

/* [Preset] */
// A Root box (hireling pairs, dice + map tokens), or Custom to use the values below
preset = "Custom"; // [Custom, Dice + Map Tokens, Corvid Spies + Sunny Advocates, Last Dynasty + Prosperous Farmers, Flame Bearers + Forest Patrol, Spring Uprising + Sunward Expedition, Popular Band + Vault Keepers]

/* [Box] */
// Inside depth of both compartments (mm)
wood_depth = 18.5; // [5:0.5:60]
// Box width (mm)
box_width = 71.5; // [40:0.5:160]
// Share of the inside width for compartment 1 (near end)
compartment_split = 0.5; // [0.2:0.01:0.8]

/* [Labels] */
// Compartment 1: near end and lid 1; | starts a new line
near_label = "Corvid Spies";
// Compartment 2: far end; | starts a new line
far_label = "Sunny Advocates";
// Lid 2 label (empty = far end label)
lid2_label = "";
// Top, line 1 (toward the lids)
top_line1 = "Bats";
// Top, line 2 (empty = one centred line)
top_line2 = "Corvids";
// Capital height of the top label (mm)
top_text_height = 6; // [3:0.1:10]

/* [Fit] */
// Sliding clearance per side between lid and groove (mm)
slide_clearance = 0.25; // [0:0.05:0.5]
// Click bump height on the lids (0 = no click)
detent_height = 0.4; // [0:0.05:0.8]
/* [Text] */
// Any font from the MakerWorld font list; bold keeps strokes printable with a 0.6 mm nozzle
font = "Noto Sans:style=Bold"; // font
// Capital-letter height of the labels (mm)
text_height = 6; // [3:0.1:10]

/* [Print] */
// What to generate
part = "all"; // [all, box, lid1, lid2]

/* [Hidden] */
// name, near, far, lid 2, top 1, top 2, top height, depth, split
presets = [
    ["Dice + Map Tokens", "Dice", "Map Tokens", "Tokens", "Tokens", "Dice", 6, 22.5, 1/2],
    ["Corvid Spies + Sunny Advocates", "Corvid Spies", "Sunny Advocates", "", "Bats", "Corvids", 6, 18.5, 1/2],
    ["Last Dynasty + Prosperous Farmers", "Last Dynasty", "Prosperous Farmers", "", "Ducks", "Eagles", 6, 18.5, 1/3],
    ["Flame Bearers + Forest Patrol", "Flame Bearers", "Forest Patrol", "", "Cats", "Rats", 6, 18.5, 1/2],
    ["Spring Uprising + Sunward Expedition", "Spring Uprising", "Sunward Expedition", "", "Moles", "Rabbits", 6, 18.5, 1/2],
    ["Popular Band + Vault Keepers", "Popular Band", "Vault Keepers", "", "Badgers", "Weasels", 6, 18.5, 1/2],
];
