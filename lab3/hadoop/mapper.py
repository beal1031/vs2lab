import const
import sys
import zmq
import time
import pickle

me = str(sys.argv[1])
context = zmq.Context()

splitter_address = "tcp://" + const.SRC + ":" + const.PORT_SPLITTER
pull_socket = context.socket(zmq.PULL) # create pull socket for receiving sentences from splitter
pull_socket.connect(splitter_address) # connect to splitter

push_socket1 = context.socket(zmq.PUSH) # create push socket for sending words to reducer
push_socket2 = context.socket(zmq.PUSH) # create push socket for sending words to reducer

# define reducer addresses
reducer1_address = "tcp://" + const.SRC + ":" + const.PORT_REDUCER1
reducer2_address = "tcp://" + const.SRC + ":" + const.PORT_REDUCER2

push_socket1.connect(reducer1_address)
push_socket2.connect(reducer2_address)

time.sleep(1)

print("mapper {} started".format(me))

while True:
    work = pickle.loads(pull_socket.recv())
    
    # short wait so you can kind of see what's going on in the terminal
    time.sleep(0.2)

    print("{} received workload {}".format(me, work))

    # stop if end of file is reached
    if work == const.EOF:
        break

    words = work.split()

    for word in words:
        # split words between reducers based on the Unicode code of the first character
        if (ord(word[0]) % 2 == 0):
            address = reducer1_address
            push_socket1.send(pickle.dumps((me, word)))
        else:
            address = reducer2_address
            push_socket2.send(pickle.dumps((me, word)))


print("end of file reached")

time.sleep(1)

# send end of file strings to reducers

print("shut down receiver 1")

push_socket1.send(pickle.dumps(const.EOF))
push_socket1.disconnect(reducer1_address)

time.sleep(1)

print("shut down receiver 2")

push_socket2.send(pickle.dumps(const.EOF))
push_socket2.disconnect(reducer2_address)