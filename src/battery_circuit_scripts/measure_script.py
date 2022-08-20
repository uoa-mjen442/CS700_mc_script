from PyLTSpice.LTSteps import LTSpiceLogReader

parsed_data = []

for voltage in (0.6,0):
    data = LTSpiceLogReader("battery_circuit_scripts/trial_circuit_{}.log" .format(voltage))

    print("Number of steps  :", data.step_count)
    step_names = data.get_step_vars()
    meas_names = data.get_measure_names()

# Printing Headers
#print(' '.join([f"{step:15s}" for step in step_names]), end='')  # Print steps names with no new line
#print(' '.join([f"{name:15s}" for name in meas_names]), end='\n')
# Printing data
#for i in range(data.step_count):
    #print(' '.join([f"{data[step][i]:15}" for step in step_names]), end='')  # Print steps names with no new line
    #print(' '.join([f"{data[name][i]:15}" for name in meas_names]), end='\n')  # Print Header
    #print([f"{data[name][i]:15}" for name in meas_names])

    
    raw_data = []
    raw_data.append([f"{data[name][1]:1}" for name in meas_names])
    parsed_data.append(raw_data[0][0])

print(parsed_data)





