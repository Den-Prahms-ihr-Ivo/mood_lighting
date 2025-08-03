from queue import Queue

from threading import Thread, Timer
import datetime
from enum import Enum
from src.config import CONFIG
import time

from rpi_ws281x import PixelStrip, ws, Color


class LED_Mode(Enum):
    (RUN, STOP) = range(2)


LED_COUNT = 12
LED_COM = 13  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1

current_state = False
led_queue = Queue()
led_thread = None
led_strip = PixelStrip(
    LED_COUNT,
    LED_COM,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
    ws.WS2811_STRIP_GRB,
)
led_strip.begin()
currently_running = False


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def animate(ls):
    s = datetime.datetime.now().second
    m = datetime.datetime.now().minute
    offset = int(s / 59 * LED_COUNT)
    minute_offset = m / 59 * 100

    R = int(CONFIG["DEFAULT"].get("COLOR_R", 255))
    G = int(CONFIG["DEFAULT"].get("COLOR_G", 255))
    B = int(CONFIG["DEFAULT"].get("COLOR_B", 255))

    for i in range(0, LED_COUNT):
        position = (i + offset) % LED_COUNT
        color_intensity = i / LED_COUNT
        r = int((R + minute_offset) * color_intensity % 255)
        g = int((G + minute_offset) * color_intensity % 255)
        b = int((B + minute_offset) * color_intensity % 255)
        ls.setPixelColor(position, Color(r, g, b))

    ls.show()

    time.sleep(50 / 1000.0)


def led_consumer(queue: Queue):
    print("LED Consumer läuft...")
    ls = None
    mode = None

    while True:
        if not queue.empty():
            item = queue.get(block=False)

            if item is not None:
                print("New item in quee")
                mode, ls = item

            if mode == LED_Mode.STOP:
                print("Stopping LED Consumer")
                for i in range(0, LED_COUNT):
                    ls.setPixelColor(i, Color(0, 0, 0))
                ls.show()
                break
        else:
            if ls is not None:
                animate(ls)


def set_state(state):
    global led_strip, led_thread, current_state

    if state:
        current_state = True
        led_thread.start()
        led_queue.put((LED_Mode.RUN, led_strip))
    else:
        current_state = False
        led_queue.put((LED_Mode.STOP, led_strip))
        led_thread = Thread(target=led_consumer, args=(led_queue,))


def toggle():
    global current_state
    set_state(not current_state)


def pop():
    global led_queue
    led_queue.get()


def shut_down():
    global led_queue, led_strip, led_thread
    led_queue.put((LED_Mode.STOP, led_strip))
    if led_thread.is_alive():
        led_thread.join()


led_thread = Thread(target=led_consumer, args=(led_queue,))
