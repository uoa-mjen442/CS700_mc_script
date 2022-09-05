import time
import matlab.engine
import numpy
initial_time = time.time()
eng = matlab.engine.start_matlab()
voltage = numpy.array
print("line 1 took {} seconds".format(time.time() - initial_time))
for i in range(10):
    voltage = eng.test_script(i, nargout=1)
    k = i
    print("completed {} loops".format(i))
    print(voltage)

print("line 2 took {} seconds".format(time.time() - initial_time))
print(voltage)
print("line 3 took {} seconds".format(time.time() - initial_time))
eng.quit()
print("line 4 took {} seconds".format(time.time() - initial_time))

