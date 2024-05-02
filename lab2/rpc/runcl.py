import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, lambda out :  print("Result: {}".format(out)))

for i in range(10):
    time.sleep(1)
    print("s")
