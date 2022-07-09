import tkinter as tk
import logging
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk
import sys
import main
import global_variables_flags


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
        b1 = tk.Button(self, text="print to stdout", command=self.print_stdout)
        b2 = tk.Button(self, text="print to stderr", command=self.print_stderr)
        b1.grid(row=1, column=0, columnspan=2)
        b2.grid(row=1, column=2, columnspan=2)
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
                start_button.configure(text='STOP')
                start_button.configure(state='normal')
                start_button_function()
            else:
                start_button.configure(text='START')
                self.stop_running = True
            start_button.configure(state='normal')
        start_button = tk.Button(self, text ="START", command=start_button_call)
        start_button.grid(row=7, column=1, rowspan=2)

        cs_label = tk.Label(self, text='Control Style')
        cs_label.grid(row=3, column=0, sticky='w')
        checkbutton_hess = tk.Checkbutton(self, text="HESS")
        checkbutton_hess.grid(row=4, column=0, sticky='w')
        checkbutton_linear = tk.Checkbutton(self, text="linear")
        checkbutton_linear.grid(row=5, column=0, sticky='w')
        checkbutton_pid = tk.Checkbutton(self, text="pid")
        checkbutton_pid.grid(row=6, column=0, sticky='w')
        checkbutton_fuzzy_power = tk.Checkbutton(self, text="fuzzy_power")
        checkbutton_fuzzy_power.grid(row=7, column=0, sticky='w')
        checkbutton_ai_prediction = tk.Checkbutton(self, text="ai_prediction")
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

    def print_stdout(self):
        '''Illustrate that using 'print' writes to stdout'''
        print("this is stdout")

    def print_stderr(self):
        '''Illustrate that we can write directly to stderr'''
        sys.stderr.write("this is stderr\n")


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
