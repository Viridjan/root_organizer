// Root organizer: thin card box
// A shallow box (one-line smaller top label) for pieces, with a sliding dovetail lid that holds the faction's
// cards in a pocket (thumb cutout to pull them out) and clicks shut. Engraved labels on both
// ends, the top and the lid. Boxes stand upright side by side in the game box.

/* [Box] */
// Inside depth of the pocket for the wooden pieces (mm)
wood_depth = 8; // [4:0.5:20]
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
side_label = "Thin Box";
// Label on top; | starts a new line
top_label = "Top label";
// Capital height of the top label (mm): smaller than the other labels so it fits a shallow box
top_text_height = 4.3; // [3:0.1:8]

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
