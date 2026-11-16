# Root organizer

A 3D-printable insert for the board game **Root** (base game and expansions). There is one box per faction, hireling set or component group. Each box has a sliding lid, and engraved labels on both ends, the top and the lid. The boxes stand upright side by side in the **base game box**; the maps and player boards go in an expansion box.

Printed on a Bambu Lab A1 with a 0.6 mm nozzle in PLA.

## What is in the box

Every box is 100 mm tall. The standard box is 70 mm wide; its depth depends on its contents.

Faction and hireling boxes have the animal on top (species from [The Root Database](https://www.therootdatabase.com/)).

### Factions (13 boxes, in the faction's colour)

Each box has a pocket for the wooden pieces, plus a card slot in the lid for the faction's cards.

| Box | Top label | Depth (mm) |
|---|---|---|
| Marquise de Cat | Cats | 27 |
| Eyrie Dynasties | Eagles | 20.5 |
| Woodland Alliance | Alliance | 18 |
| Vagabond (two boxes sharing one lid) | Vagabond | 27.5 + 17.5 |
| Riverfolk Company | Otters | 15.5 |
| Lizard Cult | Lizards | 24.5 |
| Underground Duchy | Moles | 23.5 |
| Corvid Conspiracy | Corvids | 18 |
| Lord of the Hundreds | Rats | 27 |
| Keepers in Iron | Badgers | 22.5 |
| Lilypad Diaspora | Frogs | 23 |
| Twilight Council | Bats | 24 |
| Knaves of the Deepwood | Skunks | 18 |

### Hirelings (8 boxes, white; each lid in the hireling's colour)

Six boxes hold two hirelings each, one per compartment, and each compartment has its own lid. The top label names both hirelings' animals.

| Box | Top label |
|---|---|
| Corvid Spies + Warm Sun Prophets | Corvids / Lizards |
| Last Dynasty + Forest Patrol | Eagles / Cats |
| Flame Bearers + River Roamers | Rats / Frogs |
| Spring Uprising + Sunward Expedition | Rabbits / Moles |
| Highway Bandits + Sunny Advocates | Porcupines / Bats |
| Popular Band + Vault Keepers | Weasels / Badgers |
| Singletons (14 mm deep) | Singletons |
| Prosperous Farmers (2/3 width, 46.7 mm) | Ducks |

### General (4 boxes, black)

| Box | Holds |
|---|---|
| Clearings | 3D-printed clearing pieces |
| Landmarks | landmark pieces and cards |
| Map Tokens & Dice | two compartments: dice (Dice lid) and map tokens (Tokens lid) |
| Hirelings Cards | hireling cards (140 mm wide, double width) |

## Why these sizes

- **70 × 100 mm footprint.** Three standard boxes side by side make 210 mm. That width and the 100 mm height are inherited from the original FreeCAD design. Hirelings Cards is double width (140 mm), and Prosperous Farmers is 2/3 width.
- **Depth per box.** The wood pocket depth (`wood_depth`) is the depth of the faction's pieces lying flat. A box with a card pocket adds the card stack thickness, a 1.5 mm wall and the 2.5 mm lid, so each box is only as deep as its contents need.
- **Card pockets.** Faction card pockets are 67 × 91.5 mm, for standard Root cards (63.5 × 88 mm) in Popcorn Games hard sleeves (63.5 × 88 size); card stack thicknesses (`card_stack_thickness`) were measured with the sleeves on. The hireling card pocket is 124 × 73 mm, for the large hireling cards (unsleeved). A U-shaped thumb cutout in the lid lets you pull the cards out.
- **Walls 1.5 mm** (two and a half 0.6 mm extrusion lines), so the walls stay stiff.
- **Sliding lid.** The lid slides in a 60° dovetail groove. It has 0.25 mm clearance per side, so it slides on a 0.6 mm nozzle print without being loose. Small "wings" at the bottom of the groove stop the lid and keep it flush with the base.
- **Text.** DejaVu Sans Bold, 5.5 mm capital height, engraved 0.5 mm deep. Regular-weight strokes would be thinner than the 0.6 mm nozzle. Every label is the same 5.5 mm height; long names are split over two lines (Lord of the / Hundreds, Knaves of the / Deepwood).
- **1 mm 45° chamfers** on the outer edges, including the full bottom edge, so the edges are not sharp and the lid groove ends cleanly.

## Files

| File | What it is |
|---|---|
| `cards.sc`, `plain.sc`, `divided.sc` | Parametric [SolidCraft](https://getartcraft.com) designs, one configuration row per box: faction and card boxes; plain boxes; two-compartment boxes |
| `vagabond_double.sc` | The two Vagabond boxes joined by one shared lid |
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
