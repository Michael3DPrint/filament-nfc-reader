# Case

The case is five rigid parts printed in PLA and eight washers printed in TPU 95A. Both sets are Bambu Studio projects set up for a Bambu Lab X2D, and each prints on its own plate.

| File | Contents |
|---|---|
| `filament-selector-case_rigid-parts.3mf` | All five rigid parts on one plate (see the table below) |
| `filament-selector-case_tpu-washers.3mf` | Eight TPU 95A washers |

| Rigid part | Purpose |
|---|---|
| Case_Body | Main housing for the display board |
| Faceplate | Front plate around the screen |
| NFC_Arm | Arm that holds the PN532 reader |
| NFC_Top_Lid | Lid over the reader |
| Spine_Cover | Cover for the back or spine |

## Print settings in the projects

Both projects use a 0.4 mm nozzle, the 0.20 mm Standard process, 2 walls, 15% sparse infill, no supports and an auto brim. They differ in material and plate:

| | Rigid parts | TPU washers |
|---|---|---|
| Filament profile | Bambu PLA Metal | Bambu TPU 95A |
| Plate | Supertack | Textured PEI |

The projects open in Bambu Studio 2.x. Slice them again for a different printer.

## Fastening

The case needs 10 M3 x 8 mm screws, which go straight into the plastic, so no inserts are needed. One length works in all three places:

| Joint | Screws | What the screw passes through | Pilot hole depth | Thread in the plastic with M3 x 8 |
|---|---|---|---|---|
| NFC lid to arm | 4 | 0.7 mm of lid, below a 6.0 mm wide, 1.3 mm deep head recess | 10.0 mm, in the arm posts | 7.3 mm |
| Arm to case body | 2 | 2.0 mm of arm floor, below a 6.4 mm wide, 3.0 mm deep head recess | 14.0 mm, in the body | 6.0 mm |
| Display board to standoffs | 4 | 1.6 mm board plus two 0.4 mm TPU washers | 6.0 mm, in the standoffs | 5.6 mm |

Screws longer than 10.7 mm at the lid, 16 mm at the arm or 8.4 mm at the board would reach the bottom of their pilot holes. The board joint leaves only 0.4 mm to spare, so put a TPU washer under each screw head as well as under the board, which also accounts for the 8 washers for 4 screws. The build script confirms the washer under the board, and the one under each head is inferred from the count.

The pilot holes and recesses were measured in the v10 mesh, and the washers are 6.4 mm across with a 3.2 mm bore and 0.4 mm thick. The screw lengths are calculated from those measurements and nothing was test-fitted.

Superglue could replace the two arm-to-body screws, because the spine cover still opens the cavity behind the arm. Keep the lid and board screws if you may need to service the NFC module or the display. This is a suggestion that has not been tested.

## Feet recesses

The underside of the case body has four round recesses, each 9.0 mm across and 1.2 mm deep, which the build script calls feet dimples. They do not join parts, and the unit is too heavy for magnets in them to hold it, so use them for stick-on feet. The dimensions were measured from the mesh in the rigid-parts file.
