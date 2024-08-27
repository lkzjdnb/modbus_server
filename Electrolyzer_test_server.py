from pyModbusTCP.server import ModbusServer

import json
import argparse
import threading

from dataHandler import MyDataHandler

input_register = {}
with open("input_regs_dump.csv") as f:
    for i, l in enumerate(f.readlines()):
         if l != "None\n":
            input_register[i] = int(l)
holding_register = {}
with open("holding_regs_dump.csv") as f:
    for i, l in enumerate(f.readlines()):
         if l != "None\n":
            holding_register[i] = int(l)


def main():
    parser = argparse.ArgumentParser(prog='ModbusTestServer', description='A test server for the Modbus protocol')
    parser.add_argument("-n", "--number", default=1, type=int, help="The number of server instances to start (They will be assigned to incrementing port numbers)")
    parser.add_argument("-w", "--wait", default=0, type=int, help="Time to wait before each response")
    parser.add_argument("-d", "--disconnect", action='store_true', help="This will disconnect the server after responding to one request")

    args = parser.parse_args()

    read_event = threading.Event()

    servers = []
    for i in range(args.number):
        port = 4502 + i
        s = ModbusServer(data_hdl = MyDataHandler(input_register, holding_register, args.wait, read_event), port = port, no_block=True, host = "0.0.0.0")
        s.start()
        servers.append(s)
        print(f"Started on port {port}", flush=True)

    # Wait until a read as been performed
    if(args.disconnect):
        read_event.wait()
    # Wait forever
    else:
        threading.Event().wait()

    for s in servers:
        s.stop()

if __name__ == "__main__":
    main()
