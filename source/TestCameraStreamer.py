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
    while True:
        CameraStreamer.Start()
        print(CameraStreamer.GetUrl())
        time.sleep(5)
        CameraStreamer.Stop()
        time.sleep(4)

if __name__ == '__main__':
    main()

