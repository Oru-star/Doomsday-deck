# Doomsday Deck Keyboard Firmware — CircuitPython

Target: Raspberry Pi Pico 2 (RP2350), based on the KiCad pin assignments provided.

## What this firmware does

- 5×10 key matrix → USB HID keyboard
- Joystick on GP26/GP27 → USB mouse movement
- GP21 left click, GP20 right click, GP22 joystick switch/middle click
- M5Stack Unit Scroll at I²C address `0x40` → mouse wheel and middle click
- Optional SSD1306 128×64 OLED at I²C address `0x3C`

## 1. Install CircuitPython

1. Download the **Raspberry Pi Pico 2** CircuitPython UF2 from the official CircuitPython downloads page.
2. Hold BOOTSEL while connecting the Pico 2 over USB and copy the UF2 to the `RPI-RP2` drive.
3. After reboot, a `CIRCUITPY` drive should appear.

Official downloads: https://circuitpython.org/board/raspberry_pi_pico2/

## 2. Install libraries

Download the matching **Adafruit CircuitPython Library Bundle** for the CircuitPython version installed on the Pico 2:
https://circuitpython.org/libraries

Copy these into `CIRCUITPY/lib/`:
- `adafruit_hid/`
- `adafruit_ssd1306.mpy`
- `adafruit_display_text/`
- Any dependencies required by the bundle version for `adafruit_display_text`

The firmware will continue without an OLED if the OLED driver or display is unavailable. `adafruit_hid` is required.

## 3. Copy the firmware

Copy `main.py` and `config.py` to the root of `CIRCUITPY`.

The Pico will restart and enumerate as a USB keyboard/mouse.

## 4. Current pin map

| Function | Pico 2 GPIO |
|---|---|
| Matrix rows 1–5 | GP0, GP1, GP2, GP3, GP4 |
| Matrix columns 1–10 | GP5–GP14 |
| I²C SDA | GP16 |
| I²C SCL | GP17 |
| Right click | GP20 |
| Left click | GP21 |
| Joystick switch | GP22 |
| Joystick X ADC | GP26 |
| Joystick Y ADC | GP27 |

I²C is shared by the OLED and Scroll Unit. The Scroll Unit uses 5V power, GND, SDA, and SCL; its I²C logic is 3.3V-compatible according to its design. Confirm your board's power path before wiring 5V.

## 5. Before first power-on

- Verify the key matrix diode orientation. `COLUMNS_TO_ANODES` in `config.py` is currently `False` and may need to be changed after checking the actual diode direction.
- Confirm the physical key order. `KEYMAP` in `main.py` is a starting QWERTY layout; it is not inferred from the PCB.
- Confirm the OLED controller/address. The default is SSD1306, 128×64, address `0x3C`. Set `OLED_ENABLED = False` if you have not confirmed the display.
- The joystick is calibrated at startup. Leave it centered and untouched during the first 0.5 seconds after power-up.
- If mouse movement drifts, increase `JOYSTICK_DEADZONE`; if axes are reversed, toggle `JOYSTICK_INVERT_X` / `JOYSTICK_INVERT_Y`.
- The M5Stack Scroll Unit button is assigned to middle click. The joystick switch is also middle click.
- Do not connect an external 5V supply to Pico VBUS while the Pico is USB-powered unless the power design explicitly prevents backfeeding.

## Known first-version limitations

- This is a bring-up firmware, not yet a polished production keyboard.
- The OLED shows basic status only; no custom graphics or key animation yet.
- Scroll Unit protocol follows the official register map: encoder count at `0x10`, button at `0x20`, RGB at `0x30`.
- If the unit does not appear at I²C address `0x40`, check SDA/SCL, GND, power, and the shared I²C bus.
- CircuitPython HID library behavior and supported board firmware should be checked against the installed library bundle version.
