// Root organizer: Vagabond double box
// Two boxes joined by one shared lid: the lid has a dovetail tongue on each face and holds both
// Vagabonds' card stacks between them (finger notches at the ends). Clicks shut on both boxes.

/* [Boxes] */
// Inside depth of box 1 (mm)
wood_depth1 = 23.5; // [5:0.5:60]
// Inside depth of box 2 (mm)
wood_depth2 = 13.5; // [5:0.5:60]
// Box width (mm)
box_width = 71.5; // [50:0.5:160]

/* [Cards] */
// Thickness of the card stack in the shared lid (both Vagabonds), mm
card_stack_thickness = 15.7; // [0.5:0.1:30]
// Card pocket width (card width + clearance), mm
card_pocket_width = 67; // [40:0.5:150]
// Card pocket height (card length + clearance), mm
card_pocket_height = 91.5; // [40:0.5:97]

/* [Labels] */
// Label on the box ends and the lid ends; | starts a new line
side_label = "Vagabond";
// Label on top of both boxes
top_label = "Vagabond";

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
part = "all"; // [all, box1, box2, lid]

/* [Hidden] */
mid_chamfer = 0.85;    // lid end edges between the boxes
notch_w = 14;          // finger notches through the pocket's end walls
notch_d = 25;
