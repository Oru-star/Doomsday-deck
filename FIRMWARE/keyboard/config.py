# Doomsday Deck keyboard firmware configuration
# Edit this file to match your physical keyboard and modules.

import board

# Raspberry Pi Pico 2 pin map based on the provided KiCad schematic.
ROW_PINS = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4)
COL_PINS = (
    board.GP5, board.GP6, board.GP7, board.GP8, board.GP9,
    board.GP10, board.GP11, board.GP12, board.GP13, board.GP14,
)

I2C_SDA = board.GP16
I2C_SCL = board.GP17

# Buttons from the schematic.
RIGHT_CLICK_PIN = board.GP20
LEFT_CLICK_PIN = board.GP21
JOY_SWITCH_PIN = board.GP22

# Joystick axes (ADC-capable pins).
JOY_X_PIN = board.GP26
JOY_Y_PIN = board.GP27

# IMPORTANT: Set this to match the physical diode orientation.
# False means columns are not the anode side. If keys scan incorrectly,
# test True after confirming the diode stripe/cathode direction.
COLUMNS_TO_ANODES = False

# Key debounce interval in seconds.
KEY_SCAN_INTERVAL = 0.02

# Joystick tuning. Increase DEADZONE if the mouse drifts at rest.
JOYSTICK_DEADZONE = 0.10
JOYSTICK_SPEED = 12.0
JOYSTICK_INVERT_X = False
JOYSTICK_INVERT_Y = True

# M5Stack Scroll Unit.
SCROLL_I2C_ADDRESS = 0x40
SCROLL_REVERSE = False
SCROLL_LINES_PER_STEP = 1

# OLED is optional. Set False if no display is fitted or its driver differs.
OLED_ENABLED = True
OLED_WIDTH = 128
OLED_HEIGHT = 64
OLED_I2C_ADDRESS = 0x3C
