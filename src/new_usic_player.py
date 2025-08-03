from mpd import MPDClient

from threading import Timer

HOST = "localhost"
PORT = 6600

client = MPDClient()
client.timeout = 10
client.idletimeout = None
_connected = False


def set_state(flag):
    _connect()
    if flag:
        print("... Play music")
        client.play()
    else:
        print("... Pause music")
        client.pause()


def next_song():
    _connect()
    try:
        client.next()
    except Exception as e:
        print("NExt song ging wohl nicht...")
        print(e)


def set_playlist(idx):
    global client
    _connect()
    client.clear()
    client.load(idx)


def _connect():
    global _connected
    if not _connected:
        client.connect(HOST, PORT)
        _connected = True
        cnt_dwn_timer = Timer(5, disconnect)
        cnt_dwn_timer.start()


def disconnect():
    global _connected
    _connected = False
    client.disconnect()
