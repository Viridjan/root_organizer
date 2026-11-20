# MakerWorld customizer versions

OpenSCAD ports of the SolidCraft designs, one file per MakerWorld listing. Each one opens in MakerWorld's **Parametric Model Maker** (Customize button) and runs on OpenSCAD 2021.01, the version MakerWorld uses.

| File | Listing | Ported from |
|---|---|---|
| `root_organizer_single.scad` | Faction box: wooden pieces in the box, the faction's cards in the lid (presets: the 12 factions + Landmarks) | `single.sc` |
| `root_organizer_single_thin.scad` | Shallow faction box, smaller one-line top label (template, no preset) | `single_thin.sc` |
| `root_organizer_wide.scad` | Double-width box: hireling cards in the lid, tokens in the box | `wide.sc` |
| `root_organizer_nocard.scad` | Box without cards, for pieces or tokens (presets: Clearings, Singletons, River Roamers) | `nocard.sc` |
| `root_organizer_split.scad` | Two-compartment box, one lid per compartment: two hirelings' pieces, or dice + map tokens (presets: Dice + Map Tokens, 5 hireling pairs) | `split.sc` |
| `root_organizer_split_thin.scad` | Shallow two-compartment box, smaller one-line top label (default: Highway Bandits + Warm Sun Prophets) | `split_thin.sc` |
| `root_organizer_double.scad` | Vagabond box: two boxes (Vagabond and Vagabond 2) sharing one lid that holds both card stacks | `double.sc` |
| `root_organizer_deck.scad` | Deck box for a card deck: one piece, open top, no lid (presets: Standard Deck, Exiles and Partisans, Squires and Disciples) | `deck.sc` |

The geometry matches the SolidCraft prints: volumes are within 0.2 % of `prints/`, and the only difference is the font.

## Editing

Don't edit the eight `.scad` files above: `python3 makerworld/build.py` writes them from `src/`.

- **`src/<name>.params.scad`**: the customizer parameters (and presets) of each listing.
- **`src/lib.scad`**: the shared geometry (box, lid, labels).
- **`src/main_*.scad`**: puts the parts together.

## Publishing

`LISTINGS.md` has the ready-to-paste text for each listing: title, summary, tags, description, category and license. `images/` holds a cover render for each listing, and `print_profiles/` a Bambu 3MF of each default box (see below to rebuild them).

## MakerWorld quirks (checked 2026-11-17)

- **Preset values:** dropdown values use underscores instead of spaces (`Marquise_de_Cat`). No source confirms that MakerWorld's parser handles spaces inside `// [...]` lists; underscores are safe and still readable. The labels themselves keep their spaces.
- **Font:** MakerWorld's fonts are Google Fonts, and Noto Sans is one, but no font list I could read names it. If it's missing, OpenSCAD silently falls back to its default font: check the preview after uploading, and pick another font if it looks wrong.
- **No `include`:** an `include` makes MakerWorld's parameters vanish. That's why `build.py` writes each file as one self-contained script.
- **Print profile:** every listing has one in `print_profiles/` (Bambu Studio project 3MFs; generic 3MF exports are rejected). No source says whether MakerWorld requires one.

## Upload

1. On MakerWorld, create a new model. Upload the `.scad` file instead of a 3MF; MakerWorld adds the Customize button.
2. Add a few printed photos and a 3MF of the default preset if you like. The customizer only generates the parts, not the print settings.

## Notes for the listing text

- **Printer:** designed for a 0.6 mm nozzle (also fine with 0.4 mm), PLA, no supports. Put a brim on the upright lids only.
- **Labels:** `|` starts a new line. Text height is the capital height. Labels use **Noto Sans Bold**, and any MakerWorld font works.
- **Lids:** they slide in a 60° dovetail with 0.2 mm clearance and click shut. To make the click stiffer or softer, change *Click bump height* (0 turns it off).
- **Cards:** the card pockets fit 63.5 × 88 mm cards in Popcorn Games hard sleeves. Card stack thicknesses were measured sleeved.
- **Root names:** Root and the faction names are Leder Games trademarks. Say the listing is an unofficial fan-made organizer "for Root".
