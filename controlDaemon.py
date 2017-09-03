import os
import errno

FIFO = 'gaerbox_control'

try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

while True:
    print("Opening gaerbox_control FIFO ...")
    with open(FIFO) as fifo:
        print("   opened")
        while True:
            data = fifo.read()
            if len(data) == 0:
                print("Writer closed")
                break
            print('Read: "{0}"'.format(data))