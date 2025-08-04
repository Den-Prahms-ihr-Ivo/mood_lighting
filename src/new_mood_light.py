from queue import Queue

from threading import Thread, Timer
import datetime
from enum import Enum
from src.config import CONFIG
import time
import random

from rpi_ws281x import PixelStrip, ws, Color

colors = [
    {"R": 255, "G": 255, "B": 255},
    {"R": 255, "G": 255, "B": 255},
    {"R": 255, "G": 255, "B": 255},
    {"R": 255, "G": 255, "B": 255},
    {"R": 255, "G": 255, "B": 255},
]


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

current_color_1 = random.choice(colors)
current_color_2 = random.choice(colors)
fade_color_1 = random.choice(colors)
fade_color_2 = random.choice(colors)
current_color_step = 0
N = 255


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


def cs(c):
    return min(int(c), 255)


def animate(ls):
    global current_color_step, current_color_1, current_color_2, fade_color_1, fade_color_2, N, colors
    s = int(datetime.datetime.now().microsecond / 10000)
    if s % 10 != 0:
        return
    r = 0
    g = 0
    b = 0

    for i in range(0, LED_COUNT):
        if i % 2 == 0:
            r = (
                current_color_1["R"]
                + current_color_step * (fade_color_1["R"] - current_color_1["R"]) / N
            )

            g = (
                current_color_1["G"]
                + current_color_step * (fade_color_1["G"] - current_color_1["R"]) / N
            )
            b = (
                current_color_1["B"]
                + current_color_step * (fade_color_1["B"] - current_color_1["R"]) / N
            )

        else:
            r = (
                current_color_2["R"]
                + current_color_step * (fade_color_2["R"] - current_color_2["R"]) / N
            )
            g = (
                current_color_2["G"]
                + current_color_step * (fade_color_2["G"] - current_color_2["R"]) / N
            )
            b = (
                current_color_2["B"]
                + current_color_step * (fade_color_2["B"] - current_color_2["R"]) / N
            )

        ls.setPixelColor(i, Color(cs(r), cs(g), cs(b)))
        current_color_step += 1
        if current_color_step >= N:
            current_color_step = 0
            fade_color_1 = random.choice(colors)
            fade_color_2 = random.choice(colors)

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
