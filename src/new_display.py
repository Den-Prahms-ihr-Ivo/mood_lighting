from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander="PCF8574", address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()


def set_state(state):
    if state:
        lcd.backlight_enabled = True
    else:
        lcd.backlight_enabled = False
        lcd.clear()


def show(text):
    lcd.clear()
    lcd.write_string(text)
