"""
Aufg1 unit test
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test Aufg1"""
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test

    def test_srv_get_Patric(self):  
        """Test simple call"""
        msg = self.client.call("Patric")
        self.assertEqual(msg, '123123556')
    
    def test_srv_get_Alex(self): 
        """Test simple call"""
        msg = self.client.call("Alex")
        self.assertEqual(msg, '2353453')

    def test_srv_getAll(self): 
        """Test simple call"""
        msg = self.client.call("GETALL")
        self.assertEqual(msg, '{"Mika": "123123", "Alex": "2353453", "Niklas": "345353", "Maya": "123123123", "Patric": "123123556"}')
    
    def test_srv_get_Maya(self): 
        """Test simple call"""
        msg = self.client.call("Maya")
        self.assertEqual(msg, '123123123')

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
