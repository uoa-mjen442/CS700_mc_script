import generateValues


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

