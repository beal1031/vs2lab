import constRPC
import threading
import time

from context import lab_channel


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client:
    def __init__(self):
        self.chan = lab_channel.Channel()
        threading.Thread.__init__(self)
        self.client = self.chan.join('client')
        self.server = None

    def waitForServer(self,callback):
        msgrcv = self.chan.receive_from(self.server)
        callback(msgrcv[1].value)  # wait for response  

    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list, callback):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server

        msgreq = self.chan.receive_from(self.server)
        if msgreq[1] == constRPC.OK:
            test_thread = threading.Thread(target=self.waitForServer,args=(callback,))
            test_thread.start()

class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    self.chan.send_to({client}, constRPC.OK)
                    time.sleep(5)
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass
