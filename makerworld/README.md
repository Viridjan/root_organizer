# MakerWorld customizer versions

OpenSCAD ports of the SolidCraft designs, one file per MakerWorld listing. Each one opens in MakerWorld's **Parametric Model Maker** (Customize button) and runs on OpenSCAD 2021.01, the version MakerWorld uses.

| File | Listing | Ported from |
|---|---|---|
| `root_organizer_single.scad` | Faction box with card lid (presets: the 12 factions + Landmarks) | `single.sc` |
| `root_organizer_wide.scad` | Double-width card box (Hirelings cards) | `wide.sc` |
| `root_organizer_nocard.scad` | Plain box (presets: Clearings, Singletons, River Roamers) | `nocard.sc` |
| `root_organizer_split.scad` | Two-compartment box, two lids (presets: Dice + Map Tokens, 5 hireling pairs) | `split.sc` |
| `root_organizer_split_thin.scad` | Shallow two-compartment box, one-line top label (default: Highway Bandits + Warm Sun Prophets) | `split_thin.sc` |
| `root_organizer_double.scad` | Vagabond double box (two boxes, one shared lid) | `double.sc` |

The geometry matches the SolidCraft prints: volumes are within 0.2 % of `prints/`, and the only difference is the font.

## Editing

Don't edit the six `.scad` files above: `python3 makerworld/build.py` writes them from `src/`.

- **`src/<name>.params.scad`**: the customizer parameters (and presets) of each listing.
- **`src/lib.scad`**: the shared geometry (box, lid, labels).
- **`src/main_*.scad`**: puts the parts together.

## Upload

1. On MakerWorld, create a new model. Upload the `.scad` file instead of a 3MF; MakerWorld adds the Customize button.
2. Add a few printed photos and a 3MF of the default preset if you like. The customizer only generates the parts, not the print settings.

## Notes for the listing text

- **Printer:** designed for a 0.6 mm nozzle (also fine with 0.4 mm), PLA, no supports. Put a brim on the upright lids only.
- **Labels:** `|` starts a new line. Text height is the capital height. Labels use **Noto Sans Bold**, and any MakerWorld font works.
- **Lids:** they slide in a 60° dovetail with 0.2 mm clearance and click shut. To make the click stiffer or softer, change *Click bump height* (0 turns it off).
- **Cards:** the card pockets fit 63.5 × 88 mm cards in Popcorn Games hard sleeves. Card stack thicknesses were measured sleeved.
- **Root names:** Root and the faction names are Leder Games trademarks. Say the listing is an unofficial fan-made organizer "for Root".
