// Root organizer: double-width card box (Hirelings cards)
// A double-width box with a sliding dovetail lid holding a stack of large cards in a pocket
// (thumb cutout to pull them out); the box behind holds tokens. Clicks shut; engraved labels.

/* [Box] */
// Inside depth of the pocket behind the cards (mm)
wood_depth = 13; // [5:0.5:60]
// Box width (mm): two standard 71.5 mm boxes
box_width = 143; // [50:0.5:200]

/* [Cards] */
// Thickness of the card stack, mm
card_stack_thickness = 9.5; // [0.5:0.1:30]
// Card pocket width (card width + clearance), mm
card_pocket_width = 124; // [40:0.5:190]
// Card pocket height (card length + clearance), mm
card_pocket_height = 73; // [40:0.5:97]

/* [Labels] */
// Label on both ends and on the lid; | starts a new line
side_label = "Hirelings";
// Label on top; | starts a new line
top_label = "Hirelings";

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
preset = "Custom";
presets = [];
