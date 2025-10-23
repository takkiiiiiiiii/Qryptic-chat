from app.main.generate_siftedkey import Generate_Siftedkey
from app.main.kr_Hamming import key_reconciliation_Hamming
import threading
from threading import Thread
from qiskit_aer import AerSimulator



num_qubit = 12

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
        ka = ''
        kb = ''
        while (True):
            part_ka, part_kb = Generate_Siftedkey(self.user0, self.user1, num_qubit, 0, backend=AerSimulator())
            ka += part_ka
            kb += part_kb
            print(len(ka))
        # key reconciliation
            if(len(ka) > self.key_len and len(kb) > self.key_len):
                mod = len(ka) % 7
                ka = ka[:len(ka)-mod]
                kb = kb[:len(kb)-mod] 
                break

        reconciled_key_array = key_reconciliation_Hamming(ka, kb)
        reconciled_key = ''.join(map(str, map(int, reconciled_key_array)))
        self.lock.acquire()
        self.sender_key = reconciled_key
        self.receiver_key = reconciled_key
        self.lock.release()

    def run(self):
        while True:
            self.gen_key()
            # time.sleep(30)


# ユーザーが部屋に入った直後に実行するクラス
class Generate_Key_Join():
    def __init__(self, user0, user1, key_len):
        self.user0 = user0
        self.user1 = user1
        self.key_len = key_len
    def gen_key_joined(self):
        ka = ''
        kb = ''
        while (True):
            part_ka, part_kb = Generate_Siftedkey(self.user0, self.user1, num_qubit, 0, backend=AerSimulator())
            ka += part_ka
            kb += part_kb
            print(len(ka))
        # key reconciliation
            if(len(ka) > self.key_len and len(kb) > self.key_len):
                mod = len(ka) % 7
                ka = ka[:len(ka)-mod]
                kb = kb[:len(kb)-mod] 
                break

        reconciled_key_array = key_reconciliation_Hamming(ka, kb)
        reconciled_key = ''.join(map(str, map(int, reconciled_key_array)))
        return reconciled_key