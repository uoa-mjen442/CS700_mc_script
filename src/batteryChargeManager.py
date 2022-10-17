class Battery: # this is a simplified model of a battery.
    # It has charge given in KWH, and updates each tick with the discharge rate it is passed.
    def __init__(self, capacity, charge, discharge_rate):
        self.capacity = capacity
        self.charge = charge
        self.discharge_rate = discharge_rate

    def update(self, input_power):
        if (self.charge + input_power) < self.capacity:
            self.charge = self.charge + input_power
        else:
            print('battery overflowed')
            self.charge = self.capacity
            # prevent the battery from overfilling

        if (self.charge - self.discharge_rate) > 0:
            self.charge = self.charge - self.discharge_rate
        else:
            print('battery drained')
            self.charge = 0
            # prevent the battery from having negative charge

    def get_charge(self):
        return self.charge

    def get_charge_percent(self):
        return round(self.charge/self.capacity, 4)*100

    def get_discharge_rate(self):
        return self.discharge_rate

    def get_max_discharge_rate(self):
        return self.capacity/3

    def set_discharge_rate(self, new_value):
        self.discharge_rate = new_value


