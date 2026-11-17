"""Build the MakerWorld .scad files: each = its customizer parameters + shared geometry + its main part.
MakerWorld takes one self-contained .scad per listing.  Run: python3 makerworld/build.py"""
from pathlib import Path

src = Path(__file__).parent / "src"
lib = (src / "lib.scad").read_text()
for name, main in [("single", "cards"), ("single_thin", "cards"), ("wide", "cards"), ("nocard", "nocard"), ("split", "split"), ("split_thin", "split"), ("double", "double")]:
    out = (src / f"{name}.params.scad").read_text() + "\n" + lib + (src / f"main_{main}.scad").read_text()
    (src.parent / f"root_organizer_{name}.scad").write_text(out)
    print(f"root_organizer_{name}.scad")
