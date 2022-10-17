import generateValues
import time
from batteryChargeManager import Battery
import linear_controller
import logging
from queue import Queue
import global_variables_flags
import pid_body
import pid_controller

display_queue = Queue()


def run_through_gui():
    capacity, charge, discharge_rate = 20, 10, 2  # capacity in KWH, discharge rate in KW,
    max_value, angular_frequency, prediction_length = 5, 1 / 86400, 10
    update_rate_buffer = 0.5
    lower_limit, upper_limit = capacity * 0.3, capacity * 0.7
    time_multiplier = 3600
    count = 0

    default_battery = Battery(capacity, charge, discharge_rate)
    PID = pid_body.PID(0.5, 0, 0.5, setpoint=0)
    PID.output_limits = (-5, 0)  # just don't ask

    start_tick = count
    last_tick = start_tick

    while True:
        # wait 1 second so that results don't arrive all at once.
        # TODO: start timer here and stop after function execution + rest of 1s, for consistent runtime
        time.sleep(1)

        # Generates input power data
        prediction_interval = generateValues.generate_prediction_interval(max_value, angular_frequency,
                                                                          prediction_length, count * time_multiplier)
        immediate_prediction = generateValues.generate_current_value(max_value, angular_frequency,
                                                                     count * time_multiplier)
        if global_variables_flags.control_scheme == 'linear':
            # function call to linear controller
            new_discharge_rate = linear_controller.linear_control(default_battery.get_charge(),
                                                              default_battery.get_max_discharge_rate(),
                                                              immediate_prediction, prediction_interval,
                                                              lower_limit, upper_limit, update_rate_buffer,
                                                              default_battery.get_discharge_rate())
        elif global_variables_flags.control_scheme == 'pid':
            # function call to pid controller
            count, last_tick, new_discharge_rate = pid_controller.pid_control(count, last_tick,
                                                                              default_battery.get_charge(), PID)
        else:
            # no controller selected, just charges the battery
            new_discharge_rate = 0

        default_battery.set_discharge_rate(new_discharge_rate)
        # send results to GUI terminal
        # this is running in a separate thread so is sent through a queue to be printed in the other thread.
        display_queue.put("Tick: {} - {} hours elapsed - using {} control".format(count,
                                                                                  count * time_multiplier / 3600,
                                                                                  global_variables_flags.control_scheme))
        display_queue.put("Battery charge: {}KWH, input power: {}KW, discharge rate: {}KW".format(
            round(default_battery.get_charge(), 4),
            immediate_prediction,
            round(new_discharge_rate, 4)))
        # update battery state
        default_battery.update(immediate_prediction)
        # post battery state to output
        global_variables_flags.battery_charge_percent = default_battery.get_charge_percent()
        # breaks the function call if the stop button is pressed
        if global_variables_flags.stop_flag == 1:
            global_variables_flags.stop_flag = 0
            break
        # tick increment
        count = count + 1


