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


class Client(threading.Thread):
    def __init__(self):
        self.chan = lab_channel.Channel()
        threading.Thread.__init__(self)
        self.client = self.chan.join('client')
        self.server = None

    def run(self):
        base_list = DBList({'foo'})
        result_list = self.append('bar', base_list)
        print("Result: {}".format(result_list.value))

    def begin(self):
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')
        self.chan.send_to(self.server, "10")
        self.chan.receive_from(self.server)  # wait for response
        self.start()
        

    def stop(self):
        self.chan.leave('client')

    def append(self, data, db_list):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        msgrcv = self.chan.receive_from(self.server)  # wait for response
        return msgrcv[1]  # pass it to caller


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
                    time.sleep(10)
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass
