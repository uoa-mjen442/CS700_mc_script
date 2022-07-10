#!/usr/bin/env python

import time
import matplotlib.pyplot as plt
from pid_body import PID


class WaterBoiler:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """

    def __init__(self):
        self.water_temp = 20

    def update(self, boiler_power, dt):
        if boiler_power > 0:
            # Boiler can only produce heat, not cold
            self.water_temp += 1 * boiler_power * dt

        # Some heat dissipation
        self.water_temp -= 0.02 * dt
        return self.water_temp


if __name__ == '__main__':
    count = 0
    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    pid = PID(0.75, 0.0001, 0.01, setpoint=water_temp)
    pid.output_limits = (0, 100)

    start_tick = count
    last_tick = start_tick

    # Keep track of values for plotting
    setpoint, y, x = [], [], []

    while count - start_tick < 10:
        count = count + 1
        current_time = count
        dt = current_time - last_tick

        power = pid(water_temp, current_time)
        water_temp = boiler.update(power, dt)

        x += [count - start_tick]
        y += [water_temp]
        setpoint += [pid.setpoint]

        if count - start_tick > 1:
            pid.setpoint = 100

        last_tick = count

    plt.plot(x, y, label='measured')
    plt.plot(x, setpoint, label='target')
    plt.xlabel('ticks')
    plt.ylabel('temperature')
    plt.legend()
    plt.show()