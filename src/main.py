import generateValues
import time
from batteryChargeManager import Battery


if __name__ == "__main__":
    capacity, charge, discharge_rate = 10000, 1000, 10
    max_value, angular_frequency, prediction_length = 100, 1/100, 100
    update_rate_buffer = 0.2
    lower_limit, upper_limit = capacity*0.1, capacity*0.9

    default_battery = Battery(capacity, charge, discharge_rate)
    while True:
        time.sleep(1)
        prediction_interval = generateValues.generate_prediction_interval(max_value, angular_frequency, prediction_length)
        immediate_prediction = generateValues.generate_current_value(max_value, angular_frequency)
        new_discharge_rate = sum(prediction_interval[:10])/10
        print(new_discharge_rate)
        if default_battery.charge < lower_limit:
            new_discharge_rate = new_discharge_rate * 0.8
        elif default_battery.charge > upper_limit:
            new_discharge_rate = new_discharge_rate * 1.2
        difference = new_discharge_rate - default_battery.discharge_rate
        print(difference)
        new_discharge_rate = difference * update_rate_buffer + default_battery.discharge_rate

        default_battery.set_discharge_rate(new_discharge_rate)
        print("Battery charge: {}, input power: {}, discharge rate: {}".format(default_battery.get_charge(), immediate_prediction, new_discharge_rate))
        default_battery.update(immediate_prediction)


