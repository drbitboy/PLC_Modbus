"""
Usage:

  python test16.py   ip.ad.dr.ess   port    [--debug]

E.g.

  python test16.py  192.168.1.10  502

Cf. https://github.com/drbitboy/PLC_Modbus

"""
import os
import sys
import time
from easymodbus.modbusClient import *  

### Process command-line arguments

do_debug = '--debug' in sys.argv
argv2 = [arg for arg in sys.argv[1:] if not arg.startswith('--')][:2]

if len(argv2) == 2:

  ### Get IP address and port string
  ip_address,sport = argv2

  try:

    m = None

    ### Instantiate Modbus client, optionally set debug logging level,
    ### connect to Modbus server, write -1 to sixteenth holding register
    m=ModbusClient(ip_address,int(sport))

    if do_debug: m.logging_level = logging.DEBUG

    m.connect()
    m.write_single_register(15,-1)

    i64,hr16s = 0,[]

    ### Loop reads of first 16 hodling registers, pause 900ms
    while True:
      if not (i64 & 63):
        sys.stdout.flush()
        sys.stderr.write('Hit Control-C to exit\n')
        sys.stderr.flush()
      i64 += 1

      newhr16s = m.read_holdingregisters(0,16)
      if newhr16s != hr16s:
        hr16s = newhr16s
        print(hr16s)
      time.sleep(0.9)

  except KeyboardInterrupt: pass

  if isinstance(m,ModbusClient): m.close()
