import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.start()
while True:
    time.sleep(1)
    print('1')
#cl.join()
#cl.stop()
