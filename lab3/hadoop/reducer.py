import sys
import zmq
import const
import pickle
import json
import time

me = str(sys.argv[1])
context = zmq.Context()

# user port 1 if this is reducer 1, and 2 if 2
port = const.PORT_REDUCER1 if me == '1' else const.PORT_REDUCER2

reducer_address = "tcp://" + const.SRC + ":" + port
pull_socket = context.socket(zmq.PULL) # create pull socket for receiving words
pull_socket.bind(reducer_address)

file = open("results.txt", "a")

results = {}

time.sleep(1)

print("reducer {} started".format(me))

while True:

    work = pickle.loads(pull_socket.recv())

    # stop if end of file is reached
    if work == const.EOF:
        break

    word = work[1]

    # increase word count, add word to dict if not already in there
    if word in results:
        results[word] += 1
    else:
        results[word] = 1

    print("{} received word {} from {}".format(me, work[1], work[0]))

print("end of file reached")

time.sleep(1)

# write results to file
for word, count in results.items():
    file.write(word + ": " + str(count) + "\n")