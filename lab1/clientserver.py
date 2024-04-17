"""
Client and server using classes
"""

import logging
import socket
import json

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True
    phoneDB = {
        "Mika": "123123",
        "Alex": "2353453",
        "Niklas": "345353",
        "Maya": "123123123",
        "Patric": "123123556"
        }

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, adress) = self.sock.accept() #adress # returns new socket and address of client
                while True:  # forever
                    self._logger.info("Server waiting for request")
                    data = connection.recv(1024)  # receive data from client
                    decodedData = data.decode('ascii')
                    self._logger.info("Server received "+ decodedData)
                    if decodedData == "GETALL":
                        self.getAll(decodedData, connection)
                    elif decodedData in self.phoneDB:
                        self.get(decodedData, connection)
                    else:
                        connection.send((decodedData + " not in phoneDB").encode('ascii'))
                    if not data:
                        break  # stop if client stopped
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")

    def get(self, decodedData, connection):
        self._logger.info("Server found " + decodedData + " in phoneDB")
        connection.send(self.phoneDB[decodedData].encode('ascii'))
        self._logger.info("Server send " + self.phoneDB[decodedData])

    def getAll(self, decodedData, connection):
        self._logger.info("Server sent " + decodedData)
        json_str = json.dumps(self.phoneDB)
        connection.send(json_str.encode('ascii'))

class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Mika"):
        """ Call server """
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        self.logger.info("Client sent " + msg_in)
        data = self.sock.recv(1024)  # receive the response
        self.logger.info("Client received decoded: " + data.decode('ascii'))
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def close(self):
        """ Close socket """
        self.sock.close()
