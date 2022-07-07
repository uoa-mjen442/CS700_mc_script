import math


def generate_prediction_interval(max_value, angular_frequency, prediction_length, time):
    result = []
    for i in range(prediction_length):
        value = round(max_value * math.sin(angular_frequency * 2*math.pi * (time + i)-math.pi/2), 4)
        if value < 0:
            value = 0
        result.append(value)

    return result


def generate_current_value(max_value, angular_frequency, time):
    result = round(max_value * math.sin(angular_frequency * 2*math.pi * time-math.pi/2), 4)
    if result < 0:
        result = 0
    return result


# immediate_prediction = generate_current_value(100, 1/100)
# print(immediate_prediction)
# results = generate_prediction_interval(100, 1/100, 100)
# print(results)
