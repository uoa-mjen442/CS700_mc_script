import generateValues

"""
This is a variant on P controllers, but also has a bonus feature where it can see into the future a bit.
This is intended to be adapted later to a machine learning based solar input prediction program as found
in our literature review. However such a program would require access to a lot of global irradiance data
which isn't readily collected or available. 
"""


def linear_control(charge_numerical, max_discharge, current_input, prediction_interval,
                   lower_limit, upper_limit, update_rate_buffer, current_discharge_rate):
    new_discharge_rate = sum(prediction_interval[:5]) / 5
    if charge_numerical < lower_limit:
        new_discharge_rate = new_discharge_rate * 0.8
    elif charge_numerical > upper_limit:
        new_discharge_rate = new_discharge_rate * 1.2
    difference = new_discharge_rate - current_discharge_rate
    new_discharge_rate = difference * update_rate_buffer + current_discharge_rate
    return new_discharge_rate

