# For future use this script keeps receiving bluetooth advertising
# packets from another process through FIFO file

import telegram_send

import chatListen
from AppConfig import telegram_config
import time

import os

fifo_file = '/tmp/myfifo'



while True:
    # Open the FIFO file for reading
    fifo = open(fifo_file, 'r')

    # Read data from the FIFO file
    data = fifo.read()

    # Close the FIFO file
    fifo.close()

    # Print the data
    print(data)

    telegram_send.send(messages=[data])   
