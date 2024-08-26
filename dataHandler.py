from pyModbusTCP.server import EXP_DATA_ADDRESS, ModbusServer, DataHandler
from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION, EXP_NONE

import time

class MyDataHandler(DataHandler):
    def __init__(self, input, holding, delay, read_event) -> None:
        super().__init__()
        self.input_register = input
        self.holding_register = holding
        self.delay = delay
        self.read_event = read_event
        
    def read_coils(self, address, count, srv_info):
        return super().read_coils(address, count, srv_info)

    def read_d_inputs(self, address, count, srv_info):
        return super().read_d_inputs(address, count, srv_info)

    def read_h_regs(self, address, count, srv_info):
        print(f"holding register read {address} x{count}")
        res = []
        for i in range(count):
            if not address + i in self.holding_register:
                print(f"address unset {address + i}")
                return DataHandler.Return(exp_code=EXP_DATA_ADDRESS)
            else:
                res.append(self.holding_register[address + i])
        return DataHandler.Return(exp_code=EXP_NONE, data=res)

    def read_i_regs(self, address, count, srv_info):
        print(f"input register read {address} x{count}")
        time.sleep(self.delay)
        self.read_event.set()
        res = []
        for i in range(count):
            if not address + i in self.input_register:
                print("address unset")
                return DataHandler.Return(exp_code=EXP_DATA_ADDRESS)
            else:
                res.append(self.input_register[address + i])
        return DataHandler.Return(exp_code=EXP_NONE, data=res)

    def write_coils(self, address, bits_l, srv_info):
        return super().write_coils(address, bits_l, srv_info)

    def write_h_regs(self, address, words_l, srv_info):
        print(f"Write to holding register {address}: {words_l}")
        for i, w in enumerate(words_l):
            self.holding_register[address + i] = w
        return super().write_h_regs(address, words_l, srv_info)
