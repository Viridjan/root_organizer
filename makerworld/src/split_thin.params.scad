// Root organizer: thin two-compartment box
// A shallow box split into two compartments, each with its own sliding dovetail lid that clicks
// shut. One compartment's name on each end and on its lid; a single smaller line on top, since a
// shallow box has no room for two (Highway Bandits + Warm Sun Prophets by default).

/* [Box] */
// Inside depth of both compartments (mm); two 6 mm top lines need >= 16.7 mm, use the regular two-compartment box then
wood_depth = 10; // [5:0.5:20]
// Box width (mm)
box_width = 71.5; // [40:0.5:160]
// Share of the inside width for compartment 1 (near end)
compartment_split = 0.5; // [0.2:0.01:0.8]

/* [Labels] */
// Compartment 1: near end and lid 1; | starts a new line
near_label = "Highway Bandits";
// Compartment 2: far end and lid 2; | starts a new line
far_label = "Warm Sun Prophets";
// Top label, one line
top_label = "Lizards / Porcupines";
// Capital height of the top label (mm): 4.3 fits a 71.5 mm top
top_text_height = 4.3; // [3:0.1:8]

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
preset = "Custom";
presets = [];
lid2_label = "";
top_line1 = top_label;
top_line2 = "";
