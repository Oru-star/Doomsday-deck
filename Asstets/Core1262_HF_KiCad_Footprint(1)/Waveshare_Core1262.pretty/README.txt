# Waveshare Core1262-HF / Core1262-LF — KiCad 10 footprint

## What is in this package

`Waveshare_Core1262.pretty/Core1262_HF.kicad_mod`

This footprint is intended for the Waveshare Core1262-HF/LF SX1262 module.

## Verified mechanical basis

- Module body: 22.00 × 19.00 mm
- 16 castellated edge pads
- Pad pitch: 2.54 mm
- 8 pads per edge
- Outer pad-center span: 17.78 mm
- Pad geometry used: 1.60 × 2.80 mm
- Module outline is on F.Fab/F.SilkS/F.CrtYd — it is NOT an Edge.Cuts rectangle.
- All 16 solder pads are on F.Cu because the module is mounted on the top side of the carrier PCB.

## Pad numbering used

The footprint preserves the physical side ordering shown by Waveshare's pinout:

Top edge, left → right:
1 ANT
2 GND
3 CS
4 CLK
5 MOSI
6 MISO
7 RESET
8 BUSY

Opposite edge, physically top → bottom:
9 GND
10 GND
11 RXEN
12 TXEN
13 DIO2
14 DIO1
15 GND
16 3V3

Because the opposite edge is represented as the bottom edge in this footprint, its left → right footprint order is:

16, 15, 14, 13, 12, 11, 10, 9

This reversal is intentional.

## IMPORTANT — pin-number verification

Waveshare's public pinout clearly specifies the signal order, but the published documentation does not unambiguously print the physical 1–16 numbering next to the castellated pads. Therefore, the signal order above is verified, while the numerical 1–16 convention must be checked against your actual Core1262-HF module/silkscreen before fabrication.

Do not send the PCB to fabrication until your J2 symbol pin numbers match this numbering.

## Installation

1. Copy `Waveshare_Core1262.pretty` into your project's `Assets` directory.
2. In KiCad: Preferences → Manage Footprint Libraries → Project Specific Libraries.
3. Add the folder as:
   `Waveshare_Core1262.pretty`
4. Assign:
   `Waveshare_Core1262:Core1262_HF`
5. Update the PCB from the schematic.

## Important

Do NOT draw the 22 × 19 mm module outline on Edge.Cuts. Edge.Cuts is the carrier PCB outline. The module outline belongs on F.Fab / F.SilkS / F.CrtYd.
