import ltspice
import matplotlib.pyplot as plt
from PyLTSpice.LTSpice_RawRead import LTSpiceRawRead

import numpy as np
import os

LTR = LTSpiceRawRead("simple_voltage_divider.raw")



print(LTR.get_trace_names())
print(LTR.get_raw_property())

Vout = LTR.get_trace("V(Vout)")
x = LTR.get_trace('time')  # Gets the time axis
steps = LTR.get_steps()
for step in range(len(steps)):
   # print(steps[step])
   plt.plot(x.get_time_axis(step), Vout.get_wave(step), label=steps[step])

plt.legend()  # order a legend
plt.show()
