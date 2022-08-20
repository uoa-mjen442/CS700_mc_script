import os
import matplotlib.pyplot as plt
from PyLTSpice.LTSpiceBatch import SimCommander
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead
import time

def processing_data(raw_file, log_file):
    print("Handling the simulation data of %s, log file %s" % (raw_file, log_file))

LTC = SimCommander("battery_circuit_scripts/trial_circuit.asc")
for voltage in (0.6,0):
    LTC.set_component_value('V3', voltage) #Set V3 to 0.6V, then next iteration V3 to 0.6V
    #read = LTSpiceRawRead("trial_circuit.raw") #Not necessary, needs ltspice file to be run first.
    run_netlist_file = "{}_{}.net" .format(LTC.circuit_radic, voltage)
    LTC.run(run_netlist_file, callback=processing_data)



raw, log = LTC.run(run_filename="no_callback.net").wait_results()
processing_data(raw, log)

LTC.wait_completion()