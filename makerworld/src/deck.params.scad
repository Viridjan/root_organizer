// Root organizer: deck box
// A one-piece box for a deck of cards, open at the top, with a U thumb cutout in both faces and
// the label engraved on all four sides. Boxes stand upright side by side in the game box.

/* [Preset] */
// A Root deck, or Custom to use the values below
preset = "Custom"; // [Custom, Standard_Deck, Exiles_and_Partisans, Squires_and_Disciples]

/* [Box] */
// Box width (mm)
box_width = 71.5; // [50:0.5:160]

/* [Cards] */
// Thickness of the card stack (sleeved), mm
card_stack_thickness = 34; // [5:0.5:80]
// Card pocket width (card width + clearance), mm
card_pocket_width = 67; // [40:0.5:150]
// Card pocket depth from the top (card length + clearance), mm
card_pocket_height = 91.5; // [40:0.5:97]

/* [Labels] */
// Label on all four sides; | starts a new line
side_label = "Standard Deck";

/* [Text] */
// Any font from the MakerWorld font list; bold keeps strokes printable with a 0.6 mm nozzle
font = "Noto Sans:style=Bold"; // font
// Capital-letter height of the labels (mm)
text_height = 6; // [3:0.1:10]

/* [Hidden] */
// name, side label, card stack
presets = [
    ["Standard_Deck", "Standard Deck", 34],
    ["Exiles_and_Partisans", "Exiles and|Partisans", 26.5],
    ["Squires_and_Disciples", "Squires and|Disciples", 30.5],
];
detent_height = 0;   // lib.scad's lid needs it; the deck box has no lid
