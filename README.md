# Root organizer

A 3D-printable insert for the board game **Root** (base game and expansions). There is one box per faction, hireling set or component group. Each box has a sliding lid, and engraved labels on both ends, the top and the lid. The boxes stand upright side by side in the **base game box**; the maps and player boards go in an expansion box.

Printed on a Bambu Lab A1 with a 0.6 mm nozzle in PLA.

## What is in the box

Every box is 100 mm tall. The standard box is 71.5 mm wide; its depth depends on its contents. Depths below are the **inside** depth of the wood pocket (the space for the pieces); the box is 4 mm deeper outside (1.5 mm back wall + 2.5 mm lid).

Faction and hireling boxes have the animal on top (species from [The Root Database](https://www.therootdatabase.com/)).

### Factions (13 boxes, in the faction's colour)

Each box has a pocket for the wooden pieces, plus a card slot in the lid for the faction's cards.

| Box | Top label | Inside depth (mm) |
|---|---|---|
| Marquise de Cat | Cats | 23 |
| Eyrie Dynasties | Eagles | 16.5 |
| Woodland Alliance | Alliance | 14 |
| Vagabond (two boxes sharing one lid) | Vagabond | 23.5 + 13.5 |
| Riverfolk Company | Otters | 11.5 |
| Lizard Cult | Lizards | 20.5 |
| Underground Duchy | Moles | 19.5 |
| Corvid Conspiracy | Corvids | 14 |
| Lord of the Hundreds | Rats | 23 |
| Keepers in Iron | Badgers | 18.5 |
| Lilypad Diaspora | Frogs | 19 |
| Twilight Council | Bats | 20 |
| Knaves of the Deepwood | Skunks | 14 |

### Hirelings (8 boxes, white; each lid in the hireling's colour)

Six boxes hold two hirelings each, one per compartment, and each compartment has its own lid. The top label names both hirelings' animals: the first line is the hireling at the far end, the second the one at the near end (as on Map Tokens & Dice). Compartments are half the box each, except Last Dynasty (1/3) + Prosperous Farmers (2/3), the widths of the original design.

| Box | Top label | Inside depth (mm) |
|---|---|---|
| Corvid Spies + Sunny Advocates | Bats / Corvids | 18.5 |
| Last Dynasty + Prosperous Farmers | Ducks / Eagles | 18.5 |
| Flame Bearers + Forest Patrol | Cats / Rats | 18.5 |
| Spring Uprising + Sunward Expedition | Moles / Rabbits | 18.5 |
| Highway Bandits + Warm Sun Prophets | Lizards / Porcupines (one line, 4.3 mm) | 10 |
| Popular Band + Vault Keepers | Badgers / Weasels | 18.5 |
| Singletons | Singletons | 10 |
| River Roamers (half width, 35.75 mm) | Frogs | 19.5 |

### General (4 boxes, black)

| Box | Holds |
|---|---|
| Clearings | 3D-printed clearing pieces (28.2 mm inside) |
| Landmarks | landmark pieces (20 mm inside) and cards |
| Map Tokens & Dice | two compartments, 22.5 mm inside (fits the 22 mm dice): dice (Dice lid) and map tokens (Tokens lid) |
| Hirelings Cards | hireling cards (143 mm wide, double width) |

## Why these sizes

- **71.5 × 100 mm footprint.** Three standard boxes side by side make 214.5 mm. The 100 mm height is inherited from the original FreeCAD design (which had 70 mm wide boxes). Hirelings Cards is double width (143 mm), and River Roamers is half width.
- **Depth per box.** The wood pocket depth (`wood_depth`) is the depth of the faction's pieces lying flat. The box adds a 1.5 mm back wall and the 2.5 mm lid, plus the card stack and its walls on boxes with a card pocket, so each box is only as deep as its contents need.
- **Card pockets.** Faction card pockets are 67 × 91.5 mm, for standard Root cards (63.5 × 88 mm) in Popcorn Games hard sleeves (63.5 × 88 size); card stack thicknesses (`card_stack_thickness`) were measured with the sleeves on. The hireling card pocket is 124 × 73 mm, for the large hireling cards (unsleeved). A U-shaped thumb cutout in the lid lets you pull the cards out.
- **Walls 1.5 mm** (two and a half 0.6 mm extrusion lines), so the walls stay stiff.
- **Sliding lid.** The lid slides in a 60° dovetail groove. It has 0.2 mm clearance per side (0.25 mm on the two-compartment boxes), so it slides on a 0.6 mm nozzle print without being loose. A small click detent holds it shut: a 0.4 mm bump on each dovetail edge of the lid, 5 mm below its top, snaps into a matching dip in the groove, and only rubs over the last 5 mm of travel. Small "wings" at the bottom of the groove stop the lid and keep it flush with the base.
- **Text.** DejaVu Sans Bold, 6 mm capital height, engraved 0.5 mm deep. Regular-weight strokes would be thinner than the 0.6 mm nozzle. Every label is the same 6 mm height (except the one-line 4.3 mm top label of the shallow Highway Bandits + Warm Sun Prophets box), the largest that fits on every box (the limit is the two-line Knaves label on its 18 mm end); long names are split over two lines (Lord of the / Hundreds, Knaves of the / Deepwood).
- **1 mm 45° chamfers** on the outer edges, including the full bottom edge, so the edges are not sharp and the lid groove ends cleanly.

## Files

| File | What it is |
|---|---|
| `single.sc`, `nocard.sc`, `split.sc` | Parametric [SolidCraft](https://getartcraft.com) designs, one configuration row per box: faction and card boxes; plain boxes; two-compartment boxes |
| `wide.sc` | The double-width Hirelings Cards box (one box, no configuration table) |
| `double.sc` | The two Vagabond boxes joined by one shared lid |
| `supersketch.FCStd` | The original FreeCAD design |
| `prints/` | One 3MF per box (box + lid), exported from the SolidCraft designs |
| `.bambu/plates.py` | Builds the Bambu Studio project from `prints/`: one plate per filament colour, with parts spread evenly |
| `root_organizer_A1.3mf` | Ready-to-print Bambu Studio project (A1, 0.6 mm nozzle, 0.30 mm layers, PLA Basic): 18 plates |

To rebuild the Bambu project after re-exporting boxes:

```sh
python3 .bambu/plates.py prints out.3mf
flatpak run --command=bambu-studio com.bambulab.BambuStudio --arrange 0 --orient 0 --export-3mf root_organizer_A1.3mf out.3mf
```

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) (full text in `LICENSE`). You may use, remix and share these files for non-commercial purposes, as long as you credit **Viridjan** (https://github.com/Viridjan/root_organizer) and say what you changed.

Root is a game by Leder Games; this is an unofficial fan-made organizer.
