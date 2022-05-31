import tkinter as tk
import tkinter.ttk as ttk


def main_window():
    root = tk.Tk()
    root.title('Battery controller visualisation')
    root.resizable(True, True)

    label1 = ttk.Label(root, text="Hello World", compound="center", )
    label1.grid(row=1, column=0)

    root.mainloop()


main_window()
