import os
from PyLTSpice.LTSpiceBatch import SimCommander


LTC = SimCommander('simple_voltage_divider.asc')
LTC.set_component_value('R2', '4k')

LTC.run()
LTC.wait_completion()