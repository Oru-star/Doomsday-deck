# Troubleshooting

## Pico does not appear as a keyboard
- Confirm `adafruit_hid/` is present in `CIRCUITPY/lib/`.
- Open `CIRCUITPY` `code.py`/`main.py` output using Mu or a serial console to see exceptions.
- Confirm the board is running the Pico 2 CircuitPython build, not a Pico/Pico W build.

## Keys are wrong or no keys register
- Confirm row/column GPIO assignments against the final schematic.
- Verify diode direction physically; change `COLUMNS_TO_ANODES` only after checking the diode cathode stripe.
- Change `KEYMAP` order to match the physical key layout.

## Scroll Unit not detected
- Scan I²C and confirm address `0x40`.
- Connect black=GND, red=5V, yellow=SDA, white=SCL.
- Do not assume the OLED's address is also `0x40`; two devices cannot share the same address on the same bus.

## OLED fails
- Set `OLED_ENABLED = False` to test keyboard functionality separately.
- Confirm controller, dimensions, and address before enabling it.
