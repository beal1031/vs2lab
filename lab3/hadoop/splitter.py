import os
import const
import zmq
import time
import pickle

# end program if data.txt is not found
if not os.path.exists("data.txt"):
    print("ERROR: FILE 'data.txt' NOT FOUND")
    exit()

context = zmq.Context()

# create push socket
address = "tcp://" + const.SRC + ":" + const.PORT_SPLITTER
push_socket = context.socket(zmq.PUSH)
push_socket.bind(address)

# create 'results.txt' or empty it if already existent
open("results.txt", "w").close()

file = open("data.txt", "r")

time.sleep(1)

print("splitter started")

# read file line by line and send them away
for line in file:
    workload = line
    push_socket.send(pickle.dumps(workload))

# after loop send end of file string
print("end of file reached")
push_socket.send(pickle.dumps(const.EOF))

file.close()