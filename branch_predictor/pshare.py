from math import log2
from BTBPHT import BranchTargetBuffer

class Pshare:

    def __init__(self, history_bits = 10, btb_size = 1024, pht_size = 1024, initial_state = 3):

        self.__state = initial_state
        self.__next_state = initial_state

        bht_size = pht_size
        self.__pht_size = pht_size
        self.__bht_size = bht_size

        self.__history_bits = history_bits

        self.__bht = [initial_state] * bht_size
        self.__pht = [0] * pht_size
        self.__btb = BranchTargetBuffer(btb_size)

        self.__ST = 0
        self.__SN = 1
        self.__WT = 2
        self.__WN = 3
    
    @property
    def bht(self):
        return self.__bht
    @property
    def pht_table(self):
        return self.__pht
    @property
    def btb(self):
        return self.__btb

    def __get_pht(self, pc_addr):
        return self.__pht[self.__address(pc_addr)]
    
    def __shift_pht(self, pc_addr, outcome):
        mask = int("1"*self.__history_bits,2)
        pht = self.__get_pht(pc_addr) << 1 | outcome
        self.__pht[self.__address(pc_addr)] = pht & mask
        
    def __get_bht(self, pc_addr):
        return self.__bht[self.__get_bht_addr(pc_addr)]
    
    def __set_bht(self,pc_addr, value):
        self.__bht[self.__get_bht_addr(pc_addr)] = value

    def __get_bht_addr(self, pc_addr):
        mask = int("1"*int(log2(self.__bht_size)),2)
        addr = (self.__get_pht(pc_addr) ^ self.__address(pc_addr)) & mask # Calcula indice para la tabla BHT
        return addr
    
    def __address(self, pc_addr):
        # Asegurarse de que pc_addr es un entero antes de usarlo
        if isinstance(pc_addr, str):
            pc_addr = int(pc_addr, 16)  # Convertir de hexadecimal a entero si es una cadena

        return pc_addr % self.__pht_size # Elige los bits LSB para indexar PHT (si es 1024 elige 10bits)

    def predict(self, pc_addr):
        prediction = self.__get_bht(pc_addr)
        if(prediction == self.__ST or prediction == self.__WT):
            return True
        return False

    def update(self, pc_addr, outcome):
       self.__FSM(outcome)
       self.__set_bht(pc_addr, self.__state) # Actualizar BHT segun la FSM
       self.__shift_pht(pc_addr,outcome) # Shift el nuevo outcome al PHT
       
    def update_btb(self, pc_addr, target,outcome):
            if outcome:
                self.__btb.update(pc_addr, target)

    def __FSM(self, taken):
        self.__next_state = self.__state
        match self.__state:
            case self.__ST:
                if not taken: self.__next_state = self.__WT
            case self.__SN:
                if taken: self.__next_state = self.__WN
            case self.__WT:
                if taken: self.__next_state = self.__ST
                else: self.__next_state = self.__SN
            case self.__WN:
                if taken: self.__next_state = self.__ST
                else: self.__next_state = self.__SN
            case _:
                self.__next_state = self.__state
        self.__state = self.__next_state
    