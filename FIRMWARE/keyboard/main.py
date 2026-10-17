# Doomsday Deck Keyboard Firmware
# CircuitPython for Raspberry Pi Pico 2 / RP2350
#
# Features:
# - 5x10 matrix keyboard over USB HID
# - joystick mouse movement
# - left/right/middle mouse buttons
# - M5Stack Scroll Unit I2C wheel + button
# - optional SSD1306 OLED status display
#
# Install the CircuitPython build for Raspberry Pi Pico 2 first.
# Copy config.py and this file to CIRCUITPY as main.py/config.py.
# Install the libraries listed in README.md into CIRCUITPY/lib.

import time
import math
import board
import busio
import analogio
import digitalio
import keypad
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

import config

# -------------------------- USB HID --------------------------

keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# -------------------------- Keyboard matrix -----------------
# Row-major map: 5 rows x 10 columns = 50 positions.
# Change this tuple to match the physical keycap arrangement.
# Modifier keys are ordinary HID keycodes.
KEYMAP = (
    # Row 1: number row
    Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE,
    Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO,
    # Row 2: QWERTY row
    Keycode.Q, Keycode.W, Keycode.E, Keycode.R, Keycode.T,
    Keycode.Y, Keycode.U, Keycode.I, Keycode.O, Keycode.P,
    # Row 3: home row
    Keycode.A, Keycode.S, Keycode.D, Keycode.F, Keycode.G,
    Keycode.H, Keycode.J, Keycode.K, Keycode.L, Keycode.ENTER,
    # Row 4: lower row
    Keycode.LEFT_SHIFT, Keycode.Z, Keycode.X, Keycode.C, Keycode.V,
    Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA, Keycode.PERIOD,
    # Row 5: bottom row / controls. Each position has a unique keycode.
    Keycode.LEFT_CONTROL, Keycode.LEFT_ALT, Keycode.LEFT_GUI,
    Keycode.SPACE, Keycode.SLASH, Keycode.BACKSPACE,
    Keycode.LEFT_ARROW, Keycode.DOWN_ARROW, Keycode.UP_ARROW, Keycode.RIGHT_ARROW,
)

if len(KEYMAP) != 50:
    raise ValueError("KEYMAP must contain exactly 50 keycodes")

matrix = keypad.KeyMatrix(
    row_pins=config.ROW_PINS,
    column_pins=config.COL_PINS,
    columns_to_anodes=config.COLUMNS_TO_ANODES,
    interval=config.KEY_SCAN_INTERVAL,
    max_events=64,
)

# Track the HID keycode currently held for each physical matrix position.
held_keys = {}

# -------------------------- Mouse buttons --------------------

def make_input(pin):
    obj = digitalio.DigitalInOut(pin)
    obj.direction = digitalio.Direction.INPUT
    obj.pull = digitalio.Pull.UP
    return obj

left_button = make_input(config.LEFT_CLICK_PIN)
right_button = make_input(config.RIGHT_CLICK_PIN)
joy_button = make_input(config.JOY_SWITCH_PIN)

# M5 Scroll Unit's own button becomes middle click by default.
scroll_button_was_down = False

# -------------------------- Joystick -------------------------

joy_x = analogio.AnalogIn(config.JOY_X_PIN)
joy_y = analogio.AnalogIn(config.JOY_Y_PIN)

# Center calibration: average readings at boot while joystick is untouched.
def calibrate_axis(axis, samples=40):
    total = 0
    for _ in range(samples):
        total += axis.value
        time.sleep(0.005)
    return total / samples

time.sleep(0.25)
joy_x_center = calibrate_axis(joy_x)
joy_y_center = calibrate_axis(joy_y)

def axis_to_motion(value, center, invert=False):
    # AnalogIn.value ranges from 0 to 65535.
    delta = (value - center) / 32768.0
    if invert:
        delta = -delta
    if abs(delta) < config.JOYSTICK_DEADZONE:
        return 0
    # Scale after deadzone, with gentle acceleration.
    normalized = (abs(delta) - config.JOYSTICK_DEADZONE) / (1.0 - config.JOYSTICK_DEADZONE)
    magnitude = 1 + int((normalized ** 1.5) * (config.JOYSTICK_SPEED - 1))
    return magnitude if delta > 0 else -magnitude

# -------------------------- I2C / Scroll Unit ----------------

i2c = busio.I2C(config.I2C_SCL, config.I2C_SDA, frequency=100000)

def wait_for_i2c():
    while not i2c.try_lock():
        time.sleep(0.001)

def i2c_read_register(address, register, length):
    wait_for_i2c()
    try:
        i2c.writeto(address, bytes([register]), stop=False)
        result = bytearray(length)
        i2c.readfrom_into(address, result)
        return result
    finally:
        i2c.unlock()

def i2c_write_registers(address, register, payload):
    wait_for_i2c()
    try:
        i2c.writeto(address, bytes([register]) + bytes(payload))
    finally:
        i2c.unlock()

scroll_present = False
scroll_last_count = None
scroll_button_was_down = False

# Probe address 0x40 once at boot.
wait_for_i2c()
try:
    scroll_present = config.SCROLL_I2C_ADDRESS in i2c.scan()
finally:
    i2c.unlock()

def read_scroll_count():
    # M5Stack Unit Scroll protocol: register 0x10, 16-bit little-endian count.
    raw = i2c_read_register(config.SCROLL_I2C_ADDRESS, 0x10, 2)
    unsigned = raw[0] | (raw[1] << 8)
    # Interpret as signed 16-bit so wraparound near +/-32768 behaves sensibly.
    return unsigned - 65536 if unsigned >= 32768 else unsigned

def read_scroll_button():
    # Register 0x20 returns button state (0/1).
    raw = i2c_read_register(config.SCROLL_I2C_ADDRESS, 0x20, 1)
    return bool(raw[0] & 0x01)

def set_scroll_rgb(red, green, blue):
    # Optional helper; RGB register is 0x30 followed by R, G, B.
    if scroll_present:
        i2c_write_registers(config.SCROLL_I2C_ADDRESS, 0x30, (red, green, blue))

# -------------------------- Optional OLED --------------------

display = None
oled_label = "OLED: off"

if config.OLED_ENABLED:
    try:
        import displayio
        import terminalio
        from adafruit_display_text import label
        import adafruit_ssd1306

        displayio.release_displays()
        oled = adafruit_ssd1306.SSD1306_I2C(
            config.OLED_WIDTH,
            config.OLED_HEIGHT,
            i2c,
            addr=config.OLED_I2C_ADDRESS,
        )
        oled.fill(0)
        oled.text("DOOMSDAY DECK", 0, 0, 1)
        oled.text("Keyboard booting", 0, 16, 1)
        oled.show()
        display = oled
        oled_label = "OLED: SSD1306"
    except Exception as exc:
        # The keyboard remains usable if the display is absent or unsupported.
        display = None
        oled_label = "OLED unavailable"

def update_oled():
    if display is None:
        return
    try:
        display.fill(0)
        display.text("DOOMSDAY DECK", 0, 0, 1)
        display.text("Keys: USB HID", 0, 14, 1)
        display.text("Scroll: " + ("OK" if scroll_present else "not found"), 0, 28, 1)
        display.text(oled_label, 0, 42, 1)
        display.show()
    except Exception:
        pass

update_oled()

# -------------------------- Main loop ------------------------

last_oled_update = 0
last_mouse_update = 0
mouse_button_state = 0
last_scroll_poll = 0

while True:
    # Matrix events: release only the exact keycode that was pressed.
    event = matrix.events.get()
    if event:
        index = event.key_number
        keycode = KEYMAP[index]
        if event.pressed:
            try:
                keyboard.press(keycode)
                held_keys[index] = keycode
            except ValueError:
                pass
        else:
            previous = held_keys.pop(index, None)
            if previous is not None:
                try:
                    keyboard.release(previous)
                except ValueError:
                    pass

    # Mouse buttons use pull-ups and are active-low.
    new_state = 0
    if not left_button.value:
        new_state |= Mouse.LEFT_BUTTON
    if not right_button.value:
        new_state |= Mouse.RIGHT_BUTTON
    if not joy_button.value or scroll_button_was_down:
        new_state |= Mouse.MIDDLE_BUTTON

    if new_state != mouse_button_state:
        changed = mouse_button_state ^ new_state
        for bit in (Mouse.LEFT_BUTTON, Mouse.RIGHT_BUTTON, Mouse.MIDDLE_BUTTON):
            if changed & bit:
                if new_state & bit:
                    mouse.press(bit)
                else:
                    mouse.release(bit)
        mouse_button_state = new_state

    # Joystick movement at a moderate polling rate.
    now = time.monotonic()
    if now - last_mouse_update >= 0.012:
        dx = axis_to_motion(joy_x.value, joy_x_center, config.JOYSTICK_INVERT_X)
        dy = axis_to_motion(joy_y.value, joy_y_center, config.JOYSTICK_INVERT_Y)
        if dx or dy:
            mouse.move(x=dx, y=dy)
        last_mouse_update = now

    # Scroll Unit polling. Encoder delta is translated to USB mouse wheel.
    if scroll_present and now - last_scroll_poll >= 0.025:
        try:
            count = read_scroll_count()
            if scroll_last_count is not None:
                delta = count - scroll_last_count
                # Compensate for signed 16-bit wrap.
                if delta > 32767:
                    delta -= 65536
                elif delta < -32768:
                    delta += 65536
                if config.SCROLL_REVERSE:
                    delta = -delta
                if delta:
                    wheel = max(-127, min(127, delta * config.SCROLL_LINES_PER_STEP))
                    mouse.move(wheel=wheel)
            scroll_last_count = count

            scroll_button_was_down = read_scroll_button()
        except (OSError, ValueError):
            # Recover if the cable is disconnected during operation.
            scroll_present = False
        last_scroll_poll = now

    if now - last_oled_update >= 1.0:
        update_oled()
        last_oled_update = now

    time.sleep(0.001)
