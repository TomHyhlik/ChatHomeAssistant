# For future use this script keeps receiving bluetooth advertising
# packets from another process through FIFO file


class BleHandler:
    def __init__(self, fifoFileName):
        self.fifoFileName = fifoFileName

    def start_scanner(self):
        while True:
            # Open the FIFO file for reading
            fifo = open(self.fifoFileName, 'r')

            # Read data from the FIFO file
            data = fifo.read()

            # Close the FIFO file
            fifo.close()

            # Print the data
            print(data)

