import time
import math

start_time = time.time()


def generate_prediction_interval(max_value, angular_frequency, prediction_length):
    result = []
    for i in range(prediction_length):
        value = round(2*max_value * math.sin(angular_frequency * math.pi * (time.time() - start_time + i))) - max_value
        if value < 0:
            value = 0
        result.append(value)

    return result


def generate_current_value(max_value, angular_frequency):
    result = round(2*max_value * math.sin(angular_frequency * math.pi * (time.time() - start_time))) - max_value
    if result < 0:
        result = 0
    return result


# immediate_prediction = generate_current_value(100, 1/100)
# print(immediate_prediction)
# results = generate_prediction_interval(100, 1/100, 100)
# print(results)
