from src.config import CONFIG


CANDLE_PIN = int(CONFIG["DEFAULT"].get("CANDLE_PIN", 20))

# Imports, die vom Betriebssystem abängen und die
# im Test Fall gemockt werden.
# if os.environ.get("TESTING_ENV", None) is None:
#    import GPIO
import RPi.GPIO as GPIO

current_state = False


def toggle():
    global current_state
    set_state(not current_state)


def set_state(state):
    global current_state

    if state:
        current_state = True
        GPIO.output(CANDLE_PIN, GPIO.HIGH)
    else:
        current_state = False
        GPIO.output(CANDLE_PIN, GPIO.LOW)
