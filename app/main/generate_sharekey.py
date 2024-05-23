from app.main.qkd import bb84
import threading
from threading import Thread
import time

num_qubit = 20

class Generate_Key(Thread):
    def __init__(self, user0, user1, key_len):
        Thread.__init__(self)
        self.user0 = user0
        self.user1 = user1
        self.key_len = key_len
        self.sender_key = ''
        self.receiver_key = ''
        self.lock = threading.Lock()

    def gen_key(self):
        sender_key = ''
        receiver_key = ''
        self.lock.acquire()
        while (len(sender_key) < self.key_len and len(receiver_key) < self.key_len):
            ka, kb = bb84(self.user0, self.user1, num_qubit)
            sender_key += ka
            receiver_key += kb
        self.sender_key = sender_key
        self.receiver_key = receiver_key
        self.lock.release()

    def run(self):
        while True:
            self.gen_key()
            # time.sleep(30)

