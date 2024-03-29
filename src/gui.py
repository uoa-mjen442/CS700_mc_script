import tkinter as tk
import logging
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk
import sys
import main
import global_variables_flags
"""
simple TKinter-based gui to help the user interact with the program

The most interesting part of the gui is the console log. it uses a 'redirect' class to print stdout and stderr
to its own internal terminal. This terminal is an accurate copy of the real terminal, but doesn't receive commands.

most of the code here is creating buttons and checkboxes and placing them in various spots in the gui using the 'grid'
function. 

The GUI also has a use of multithreading where it calls the main function using a thread pool executor. This is to 
prevent the GUI from freezing while functions in main run, as they can take a lot of time. This way we can see status
updates in real time. With a few subtle code edits you can actually run multiple simulations at once.
"""


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        toolbar = tk.Frame(self)
        self.title('Battery management GUI')
        toolbar.grid(row=0, column=0, columnspan=3)
        s = ttk.Style()
        self.stop_running = False
        s.theme_use("default")
        s.configure("TProgressbar", thickness=100)
        # Add a Scrollbar(horizontal)
        title = tk.Label(self, text='Solar-battery management', font="Times 20 italic bold")
        title.grid(row=2, column=0, columnspan=2)
        v = tk.Scrollbar(self, orient='vertical')
        v.grid(row=2, column=5, rowspan=11)
        self.value_label = ttk.Label(self, text='Battery charge: 0%')
        self.value_label.grid(column=0, row=9, columnspan=2)
        self.text = tk.Text(self, wrap="word", yscrollcommand=v.set, padx=5, pady=5)
        self.text.grid(row=2, column=2, columnspan=3, rowspan=11, padx=5, pady=5)
        self.text.tag_configure("stderr", foreground="#b22222")
        self.text.insert('end', 'Console log\n')
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = Redirect(self.text, old_stdout, "stdout")
        sys.stderr = Redirect(self.text, old_stderr, "stderr")
        self.pb = ttk.Progressbar(self, orient='horizontal', mode='determinate',
                             length=280, style="TProgressbar")
        self.pb.grid(row=10, column=0, columnspan=2)
        self.pb['value'] = 50

        def start_button_call():
            start_button.configure(state='disabled')
            if start_button['text'] == 'START':
                self.stop_running = False
                start_button.configure(text='STOP')
                start_button.configure(state='normal')
                options_selected = [hess_selected.get(), linear_selected.get(), pid_selected.get(),
                                    fuzzy_power_selected.get(), ai_prediction_selected.get()]
                if sum(options_selected) > 1:
                    raise Exception("Multiple options selected. please try again")
                if hess_selected.get():
                    global_variables_flags.control_scheme = 'hess'
                    raise Exception("Unsupported control scheme: HESS. Please try again")
                elif linear_selected.get():
                    global_variables_flags.control_scheme = 'linear'
                elif pid_selected.get():
                    global_variables_flags.control_scheme = 'pid'
                elif fuzzy_power_selected.get():
                    global_variables_flags.control_scheme = 'fuzzy'
                    raise Exception("Unsupported control scheme: Fuzzy. Please try again")
                elif ai_prediction_selected.get():
                    global_variables_flags.control_scheme = 'ai prediction'
                    raise Exception("Unsupported control scheme: AI prediction. Please try again")
                start_button_function()
            else:
                start_button.configure(text='START')
                self.stop_running = True
            start_button.configure(state='normal')
        start_button = tk.Button(self, text ="START", command=start_button_call)
        start_button.grid(row=7, column=1, rowspan=2)

        # control style selection

        cs_label = tk.Label(self, text='Control Style')
        cs_label.grid(row=3, column=0, sticky='w')
        hess_selected = tk.IntVar()
        checkbutton_hess = tk.Checkbutton(self, text="HESS", variable=hess_selected)
        checkbutton_hess.grid(row=4, column=0, sticky='w')
        linear_selected = tk.IntVar()
        checkbutton_linear = tk.Checkbutton(self, text="linear", variable=linear_selected)
        checkbutton_linear.grid(row=5, column=0, sticky='w')
        pid_selected = tk.IntVar()
        checkbutton_pid = tk.Checkbutton(self, text="pid", variable=pid_selected)
        checkbutton_pid.grid(row=6, column=0, sticky='w')
        fuzzy_power_selected = tk.IntVar()
        checkbutton_fuzzy_power = tk.Checkbutton(self, text="fuzzy_power", variable=fuzzy_power_selected)
        checkbutton_fuzzy_power.grid(row=7, column=0, sticky='w')
        ai_prediction_selected = tk.IntVar()
        checkbutton_ai_prediction = tk.Checkbutton(self, text="ai_prediction", variable=ai_prediction_selected)
        checkbutton_ai_prediction.grid(row=8, column=0, sticky='w')

        label_time_multiplier = tk.Label(self, text="time multiplier: ")
        label_time_multiplier.grid(row=3, column=1, sticky='w')
        field_time_multiplier = tk.Entry(self)
        field_time_multiplier.grid(row=4, column=1, sticky='w')
        label_battery_capacity = tk.Label(self, text="battery capacity (KWH): ")
        label_battery_capacity.grid(row=5, column=1, sticky='w')
        field_battery_capacity = tk.Entry(self)
        field_battery_capacity.grid(row=6, column=1, sticky='w')
        self.update()

        def display_worker(queue):
            line = queue.get()
            print(line)

        def call_main():
            logging.info('running main')
            main.run_through_gui()
            return 'main loop terminated'

        def start_button_function():
            with ThreadPoolExecutor() as executor:
                t1 = executor.submit(call_main)
                while True:
                    self.update()
                    self.pb['value'] = global_variables_flags.battery_charge_percent
                    self.value_label.configure(text='Battery charge: {}%'.format(round(global_variables_flags.battery_charge_percent), 2))
                    display_worker(main.display_queue)
                    sleep(0.01)
                    if t1.done():
                        print(t1.result())
                        main.display_queue.queue.clear()
                        break
                    if self.stop_running:
                        print('stop')
                        global_variables_flags.stop_flag = True
                        sleep(1)
                        self.stop_running = False
        self.mainloop()


class Redirect(object):
    def __init__(self, widget, old_input, tag="stdout"):
        self.widget = widget
        self.old_input = old_input
        self.tag = tag

    def write(self, input_string):
        self.widget.insert("end", input_string, (self.tag,))
        self.old_input.write(input_string)
        self.widget.see('end')

    def flush(self):
        pass


if __name__ == '__main__':
    app = ExampleApp()
    app.mainloop()
