"""Simple Wii Remote test script for Windows.

Install:
    py -m pip install mote

Run:
    py wii_test.py

Press 1 + 2 on the Wiimote to connect.
"""

import time

try:
    from mote import Mote
except ImportError:
    raise SystemExit("Please install the library: py -m pip install mote")


def main():
    print("Searching for a Wii Remote...")
    print("Press buttons 1 and 2 on the Wiimote now.")

    wii = Mote()
    if not wii.connect():
        print("Failed to connect to the Wii Remote.")
        return

    print("Connected! Press buttons to test them.")
    print("Press Home to quit.")

    last = set()
    try:
        while True:
            buttons = wii.get_buttons()
            current = {name for name, pressed in buttons.items() if pressed}
            new = current - last

            if new:
                print("Pressed:", sorted(new))

            if buttons.get("HOME"):
                print("Home pressed, exiting.")
                break

            last = current
            time.sleep(0.05)
    finally:
        wii.disconnect()
        print("Disconnected.")


if __name__ == "__main__":
    main()
