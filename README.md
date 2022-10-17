*** Software readme ***

**python version**
Part of this project uses the MATLAB to python API. In order for this to function it has to be with compatible versions, which can be found here
https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/support/sysreq/files/python-compatibility.pdf

Reccommended selection is python 3.9 and MATLAB 3.10. Other versions may work with the rest of the project, but your mileage may vary. 
https://www.python.org/downloads/release/python-390/


The version of python needs to be in your path variable, which can be selected as an option when you install, or added manually following the steps here
https://www.educative.io/answers/how-to-add-python-to-path-variable-in-windows

Finally, the matlab to python API needs to be installed as a package. I would reccommend doing it through the matlab terminal using the following commands:
```
import matlab.engine
eng = matlab.engine.start_matlab()
```
Documentation on the debugging process for this can be found here
https://au.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

**Packages**
Package               Version
--------------------- -------
matlabengineforpython R2022a 
numpy                 1.23.2 
Pillow                9.2.0  
pip                   22.2.2 
PyQt5                 5.15.7 
PyQt5-Qt5             5.15.2 
PyQt5-sip             12.11.0
scipy                 1.9.1  
setuptools            58.1.0 
torch                 1.12.1 
typing_extensions     4.3.0  

In order to keep the packages on the version in the PATH variable, I would reccommend installing the packages to pip directly. This can be done in either command prompt or in the internal terminal of an IDE which supports pip, such as PyCharm.

**running the project**

The main function of the project can be run through the following command, once in the correct folder:
python3 gui.py

Running main.py will do nothing; it contains the code which connects the code base together but itself is just a function.

the simulink feature demo can be run through the following command:
python3 trial_simulink.py
It will run more quickly if matlab and simulink are already open; in the range of 10s to initialise instead of 1 minute to initialise. Once running, the model is very simple and runs fast.
There are a few unrelated simulink and ltspice files in the project as well. They don't do anything, but they're part of our research process so I've left them in for completeness.