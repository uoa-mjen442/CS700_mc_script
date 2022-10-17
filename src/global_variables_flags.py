stop_flag = 0  # set in the gui to tell the main function to terminate
battery_charge_percent = 0  # passed from the main function to the gui to be displayed
control_scheme = None  # passed from the gui to the main function to control which controller it calls

"""
Python global variables are a little weird. They still have to be declared within the namespace of a local function.
By contrast, referencing a variable which exists in a specific namespace (in this example a separate file) is relatively easy.
Any function can access these variables provided they import or have a dependency which imports this file.
This does have issues with shared variable access though, so need to be careful with how these are used.
"""