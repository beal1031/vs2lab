import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.begin()

for i in range(10):
    time.sleep(1)
    print("s")
