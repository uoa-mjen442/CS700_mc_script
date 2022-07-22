import os
import matplotlib.pyplot as plt
from PyLTSpice.LTSpiceBatch import SimCommander
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead
import time

initial_read = LTSpiceRawRead("trial_circuit.raw")
print(initial_read.get_trace_names())
print(initial_read.get_raw_property())

switch_node = initial_read.get_trace("V(n008)")
x = initial_read.get_trace("time")
steps = initial_read.get_steps()

plt.figure("1")
for step in range(len(steps)):
   # print(steps[step])
   plt.plot(x.get_time_axis(step), switch_node.get_wave(step), label=steps[step])


plt.legend()  # order a legend
plt.show()
################

LTC = SimCommander("trial_circuit.asc")
LTC.set_component_value('V3', 2)

LTC.run()
LTC.wait_completion()

###############
LTR = LTSpiceRawRead("trial_circuit.raw")
print(LTR.get_trace_names())
print(LTR.get_raw_property())

switch_node_2 = LTR.get_trace("V(n008)")
x2 = LTR.get_trace("time")

plt.figure("2")

for step in range(len(steps)):
   # print(steps[step])
   plt.plot(x2.get_time_axis(step), switch_node_2.get_wave(step), label=steps[step])

plt.figure("2")
plt.legend()  # order a legend
plt.show()