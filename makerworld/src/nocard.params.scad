// Root organizer: plain box
// A box for pieces or tokens with a sliding dovetail lid that clicks shut. Engraved labels on
// both ends, the top and the lid. Boxes stand upright side by side in the game box.

/* [Preset] */
// A Root component box, or Custom to use the values below
preset = "Custom"; // [Custom, Clearings, Singletons, River_Roamers]

/* [Box] */
// Inside depth of the pocket (mm)
wood_depth = 20; // [5:0.5:60]
// Box width (mm): 71.5 standard, 35.75 half
box_width = 71.5; // [30:0.25:160]

/* [Labels] */
// Label on both ends and on the lid; | starts a new line
side_label = "Clearings";
// Label on top; | starts a new line
top_label = "Clearings";

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
// name, side label, top label, width, depth
presets = [
    ["Clearings", "Clearings", "Clearings", 71.5, 28.2],
    ["Singletons", "Singletons", "Singletons", 71.5, 10],
    ["River_Roamers", "River Roamers", "Frogs", 35.75, 19.5],
];
