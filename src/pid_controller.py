

def pid_control(count, last_tick, pid_variable, pid_object):
    current_time = count
    # the -1 is because the battery charge ROC is inversely proportional to the desired discharge rate.
    pid_control_output = -1*pid_object(pid_variable, current_time+1)

    last_tick = count
    return count, last_tick, pid_control_output
