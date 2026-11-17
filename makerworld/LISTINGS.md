# MakerWorld listings: ready-to-paste texts

Seven listings. Each one gets:

- **Model file:** the `.scad` (enables *Customize*).
- **Cover:** the render in `images/`. Add photos of your prints when you have them.
- **Print profile:** the 3MF in `print_profiles/`, made from the Bambu project: A1, 0.6 mm nozzle, 0.30 mm Strength, PLA Basic, one colour per plate. `single_thin` has none, because no Root box uses it; its customizer output is the profile.

Shared fields:

- **Category:** Toys & Games › Board Games (or the closest board-game accessory category).
- **License:** CC BY-NC-SA 4.0. It is non-commercial, which suits a fan-made accessory for a commercial game.
- **Common tags:** `root`, `board game`, `organizer`, `insert`, `box`, `sliding lid`, `customizable`, `openscad`, `leder games`.

The **Common part** below goes at the end of every description.

---

## Common part (append to every description)

```
WHAT IT IS
Part of an unofficial, fan-made organizer for the board game Root (Leder Games). The boxes stand upright side by side in the game box: 100 mm tall, 71.5 mm wide (three fit across 214.5 mm), and only as deep as their contents.

FEATURES
• Sliding lid in a 60° dovetail, 0.2 mm clearance per side (0.25 mm on two-compartment boxes); small stop feet keep it flush with the base.
• Click detent: a 0.4 mm bump on each dovetail edge of the lid snaps into a dip in the groove over the last 5 mm, so the lid stays shut.
• Labels engraved on both ends, the top and the lid (one name per end, readable with the box lying on its back).
• 1 mm 45° chamfers on the outer edges.

CUSTOMIZE
Open "Customize" to pick a preset or set your own depth, width, labels (| starts a new line), font and text size, sliding clearance and click strength. "Part" generates the whole set or a single piece.

PRINTING
• Designed for a 0.6 mm nozzle (walls are 1.5 mm, text is bold); a 0.4 mm nozzle works too.
• PLA, 0.2–0.3 mm layers, 4 walls, 15–25 % infill, no supports.
• Box lies on its back, lids stand upright: give the lids a brim (outer brim, ~5 mm); boxes need none.
• Lid too tight or too loose? Change "Sliding clearance" (0.15–0.3 mm). Click too stiff or too soft? Change "Click bump height" (0 = no click).

Root is a trademark of Leder Games. This is an unofficial fan creation, not affiliated with or endorsed by Leder Games.
```

---

## 1. `root_organizer_single.scad` (faction box with card lid)

- **Title:** Root Organizer – Faction Box with Card Lid (Customizable)
- **Summary:** A box for each Root faction's wooden pieces, with a sliding lid that holds the faction's cards and clicks shut. Presets for all 12 factions and Landmarks.
- **Extra tags:** `faction`, `card box`, `card holder`, `sleeved cards`
- **Cover:** `images/single.png`
- **Print profile:** `print_profiles/root_organizer_single.3mf` (Marquise de Cat)
- **Description (before the common part):**

```
One box per faction: the wooden pieces go in the box, the faction's cards go in a pocket inside the sliding lid, with a U thumb cutout to pull them out.

PRESETS (inside depth / card stack)
Marquise de Cat 23 / 0.7 · Eyrie Dynasties 16.5 / 3.5 · Woodland Alliance 14 / 0.7 · Riverfolk Company 11.5 / 0.7 · Lizard Cult 20.5 / 0.7 · Underground Duchy 19.5 / 5.2 · Corvid Conspiracy 14 / 0.7 · Lord of the Hundreds 23 / 4.5 · Keepers in Iron 18.5 / 2 · Lilypad Diaspora 19 / 9.2 · Twilight Council 20 / 0.7 · Knaves of the Deepwood 14 / 8.5 · Landmarks 20 / 5.5 (mm)

The card pocket is 67 × 91.5 mm for standard cards (63.5 × 88 mm) in hard sleeves; card stack thicknesses were measured sleeved. Change them for your own sleeves.

The top label is the faction's animal (Cats, Eagles, Alliance, Otters…). The Vagabond has its own listing (two boxes sharing one lid).
```

## 2. `root_organizer_single_thin.scad` (thin card box)

- **Title:** Root Organizer – Thin Card Box (Customizable)
- **Summary:** A shallow version of the faction box: card lid, click-shut sliding lid, and a smaller one-line top label that fits a thin box.
- **Extra tags:** `thin`, `card box`, `card holder`
- **Cover:** `images/single_thin.png`
- **Print profile:** none, use Customize.
- **Description:**

```
The faction box with card lid, for contents only a few millimetres thick (8 mm inside by default). A shallow box has a narrow top, so the top label is one line at an adjustable, smaller height (4.3 mm by default; the other labels stay 6 mm).

No Root box needs it today; it's here for expansions, promos and custom content. For deeper boxes use the regular faction box.
```

## 3. `root_organizer_wide.scad` (double-width card box)

- **Title:** Root Organizer – Hirelings Card Box, Double Width (Customizable)
- **Summary:** A double-width box (143 mm) whose sliding lid holds the large hireling cards; the box holds tokens behind them.
- **Extra tags:** `hirelings`, `card box`, `large cards`
- **Cover:** `images/wide.png`
- **Print profile:** `print_profiles/root_organizer_wide.3mf`
- **Description:**

```
Two standard box widths (143 mm) wide, for the large Hireling cards (unsleeved): card pocket 124 × 73 mm, 9.5 mm stack, with a thumb cutout. The box behind the lid is 13 mm deep inside.

Card size, stack thickness, depth and width are all adjustable for other large-card decks.
```

## 4. `root_organizer_nocard.scad` (plain box)

- **Title:** Root Organizer – Plain Box with Sliding Lid (Customizable)
- **Summary:** A plain Root organizer box with a click-shut sliding lid, for pieces and tokens. Presets for Clearings, Singletons and River Roamers (half width).
- **Extra tags:** `token box`, `clearings`, `hirelings`
- **Cover:** `images/nocard.png`
- **Print profile:** `print_profiles/root_organizer_nocard.3mf` (Clearings)
- **Description:**

```
The simplest box of the set: one pocket, a thin sliding lid, labels on both ends, the top and the lid.

PRESETS (width / inside depth)
Clearings 71.5 / 28.2 · Singletons 71.5 / 10 · River Roamers 35.75 (half width) / 19.5 (mm)
```

## 5. `root_organizer_split.scad` (two-compartment box)

- **Title:** Root Organizer – Two-Compartment Box for Hireling Pairs (Customizable)
- **Summary:** One box, two compartments, two click-shut lids. Holds two Root hirelings (or dice + map tokens), with each name on its end and both animals on top.
- **Extra tags:** `hirelings`, `dice`, `tokens`, `two compartments`, `divided box`
- **Cover:** `images/split.png`
- **Print profile:** `print_profiles/root_organizer_split.3mf` (Corvid Spies + Sunny Advocates; lids in the hirelings' colours)
- **Description:**

```
Two compartments, each with its own sliding lid: one hireling per compartment, its name on that end of the box and on its lid, both animals on top (far-end animal first).

PRESETS (inside depth, compartment split)
Dice + Map Tokens 22.5 (fits 22 mm dice) · Corvid Spies + Sunny Advocates 18.5 · Last Dynasty + Prosperous Farmers 18.5 (1/3 + 2/3) · Flame Bearers + Forest Patrol 18.5 · Spring Uprising + Sunward Expedition 18.5 · Popular Band + Vault Keepers 18.5 (mm, halves unless noted)

The split is adjustable (compartment 1's share of the inside width). Two 6 mm top lines need at least ~16.7 mm inside depth; for shallower pairs use the thin two-compartment box.
```

## 6. `root_organizer_split_thin.scad` (thin two-compartment box)

- **Title:** Root Organizer – Thin Two-Compartment Box (Customizable)
- **Summary:** A shallow two-compartment box with two click-shut lids and a one-line top label. Default: Highway Bandits + Warm Sun Prophets (10 mm inside).
- **Extra tags:** `hirelings`, `thin`, `two compartments`
- **Cover:** `images/split_thin.png`
- **Print profile:** `print_profiles/root_organizer_split_thin.3mf` (Highway Bandits + Warm Sun Prophets)
- **Description:**

```
The two-compartment box for contents only ~10 mm thick. The top is too narrow for two lines, so both animals share one line ("Lizards / Porcupines") at an adjustable smaller height (4.3 mm fits a 71.5 mm box).

Default: Highway Bandits + Warm Sun Prophets, 10 mm inside, 14 mm outside.
```

## 7. `root_organizer_double.scad` (Vagabond double box)

- **Title:** Root Organizer – Vagabond Double Box with Shared Lid (Customizable)
- **Summary:** Two Vagabond boxes joined by one double-sided sliding lid that holds both Vagabonds' cards between them.
- **Extra tags:** `vagabond`, `double box`, `card box`
- **Cover:** `images/double.png`
- **Print profile:** `print_profiles/root_organizer_double.3mf`
- **Description:**

```
The two Vagabond boxes slide onto one shared lid: it has a dovetail tongue on each face and a card pocket between them for both Vagabonds' cards (15.7 mm stack), with finger notches at both ends. Each box clicks onto its side of the lid.

Box 1 is 23.5 mm deep inside, box 2 13.5 mm; together with the lid the set is 63.7 mm deep. All depths, the card stack and the labels are adjustable.
```
