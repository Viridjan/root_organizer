// Root organizer: faction box with card lid
// A box for a faction's wooden pieces, with a sliding dovetail lid that holds the faction's
// cards in a pocket (thumb cutout to pull them out) and clicks shut. Engraved labels on both
// ends, the top and the lid. Boxes stand upright side by side in the game box.

/* [Preset] */
// A Root faction, or Custom to use the values below
preset = "Custom"; // [Custom, Marquise de Cat, Eyrie Dynasties, Woodland Alliance, Riverfolk Company, Lizard Cult, Underground Duchy, Corvid Conspiracy, Lord of the Hundreds, Keepers in Iron, Lilypad Diaspora, Twilight Council, Knaves of the Deepwood, Landmarks]

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
    ["Marquise de Cat", "Marquise de Cat", "Cats", 0.7, 23],
    ["Eyrie Dynasties", "Eyrie Dynasties", "Eagles", 3.5, 16.5],
    ["Woodland Alliance", "Woodland Alliance", "Alliance", 0.7, 14],
    ["Riverfolk Company", "Riverfolk Company", "Otters", 0.7, 11.5],
    ["Lizard Cult", "Lizard Cult", "Lizards", 0.7, 20.5],
    ["Underground Duchy", "Underground Duchy", "Moles", 5.2, 19.5],
    ["Corvid Conspiracy", "Corvid Conspiracy", "Corvids", 0.7, 14],
    ["Lord of the Hundreds", "Lord of the|Hundreds", "Rats", 4.5, 23],
    ["Keepers in Iron", "Keepers in Iron", "Badgers", 2, 18.5],
    ["Lilypad Diaspora", "Lilypad Diaspora", "Frogs", 9.2, 19],
    ["Twilight Council", "Twilight Council", "Bats", 0.7, 20],
    ["Knaves of the Deepwood", "Knaves of the|Deepwood", "Skunks", 8.5, 14],
    ["Landmarks", "Landmarks", "Landmarks", 5.5, 20],
];
top_text_height = text_height;
