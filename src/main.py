import generateValues
import time
from batteryChargeManager import Battery
import linear_controller


if __name__ == "__main__":
    capacity, charge, discharge_rate = 20, 10, 2 # capacity in KWH, discharge rate in KW,
    max_value, angular_frequency, prediction_length = 5, 1/86400, 10
    update_rate_buffer = 0.5
    lower_limit, upper_limit = capacity*0.3, capacity*0.7
    time_multiplier = 1800
    count = 0
    control_scheme = 'linear'

    default_battery = Battery(capacity, charge, discharge_rate)
    while True:
        time.sleep(1)
        prediction_interval = generateValues.generate_prediction_interval(max_value, angular_frequency,
                                                                          prediction_length, count*time_multiplier)
        immediate_prediction = generateValues.generate_current_value(max_value, angular_frequency, count*time_multiplier)
        new_discharge_rate = linear_controller.linear_control(default_battery.get_charge(),
                                                                    default_battery.get_max_discharge_rate(),
                                                                    immediate_prediction, prediction_interval,
                                                                    lower_limit, upper_limit, update_rate_buffer,
                                                                    default_battery.get_discharge_rate())

        default_battery.set_discharge_rate(new_discharge_rate)
        print("Tick: {} - {} hours elapsed - using {} control".format(count, count*time_multiplier/3600, 'linear'))
        print("Battery charge: {}KWH, input power: {}KW, discharge rate: {}KW".format(round(default_battery.get_charge(), 4),
                                                                                      immediate_prediction,
                                                                                      round(new_discharge_rate, 4)))
        default_battery.update(immediate_prediction)
        count = count + 1


