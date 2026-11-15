# Case

The case is five rigid parts printed in PLA. They are one Bambu Studio project, `filament-selector-case_rigid-parts.3mf`, set up for a Bambu Lab X2D, with the parts split over two plates so each plate prints more reliably.

| Rigid part | Plate | Purpose |
|---|---|---|
| Case_Body | 2 | Main housing for the display board |
| Faceplate | 1 | Front plate around the screen |
| NFC_Arm | 1 | Arm that holds the PN532 reader |
| NFC_Top_Lid | 1 | Lid over the reader |
| Spine_Cover | 1 | Cover for the back or spine |

## Print settings in the project

The project uses a 0.4 mm nozzle, the 0.20 mm Standard process, 2 walls, 15% gyroid infill, no supports, an auto brim and the Textured PEI plate. It does not set a material for the parts: filament slot 1 is PLA, so choose your own PLA before slicing. The project opens in Bambu Studio 2.x. Slice it again for a different printer.

## How the parts hold together

The case needs 5 screws, which go straight into the plastic, so no inserts or washers are needed. The lid and the NFC arm need almost none, because they are held by their shape:

| Joint | Held by |
|---|---|
| NFC lid to arm | No screws. Four hooks on the lid's underside, two per side, each 10 mm long with a 0.6 mm barb, snap into a groove in the inner side walls of the arm. The lid drops straight down into a pocket in the top of the arm, and you pry it up to remove it. |
| PN532 in the arm | Two 2.5 mm stops on the arm floor, 0.4 mm in front of the board's front edge, keep the board from sliding forward out of its holder. They are not locating pins and need no sockets. |
| Arm to case body | The arm slides on from the back along two dovetail rails on top of the pillar, which carry its weight and hold it down. One M3 x 6 mm screw goes through the arm floor into the pillar wall and only stops the arm sliding back off. |
| Display board to standoffs | Four M3 x 8 mm screws. |

The screws, with the depths measured in the mesh:

| Joint | Screws | What the screw passes through | Pilot hole depth | Thread in the plastic |
|---|---|---|---|---|
| Arm to case body | 1 x M3 x 6 | 2.1 mm of arm floor, below a 6.4 mm wide, 3.2 mm deep head recess | 9.0 mm, in the pillar | 3.9 mm |
| Display board to standoffs | 4 x M3 x 8 | 1.6 mm of board | 7.0 mm, in the standoffs | 6.4 mm |

A screw longer than 11.1 mm at the arm or 8.6 mm at the board would reach the bottom of its pilot hole. The pilot holes and recesses were measured in the v20 mesh by fitting cylinders to its walls. The screw lengths are calculated from those measurements and nothing was test-fitted. The hooks, grooves, rails and stops come from the owner's description and were not measured.

Superglue could replace the arm screw, because the spine cover still opens the cavity behind the arm. Keep the board screws if you may need to service the display. This is a suggestion that has not been tested.

## Feet recesses

The underside of the case body has four round recesses, each 9.0 mm across and 1.2 mm deep, which the build script calls feet dimples. They do not join parts, and the unit is too heavy for magnets in them to hold it, so use them for stick-on feet. The dimensions were measured from the mesh in the rigid-parts file.
