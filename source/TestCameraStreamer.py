#!/usr/bin/env python3

import telegram_send
import ChatListener
import AppConfig
import time
import CameraStreamer

def main() -> None:
    """
    Try starting and stopping video streaming server
    """

    cs = CameraStreamer.CameraStreamer()
    print(cs.get_url())

    while True:
        cs.start()
        time.sleep(4)
        cs.stop()
        time.sleep(4)

if __name__ == '__main__':
    main()

