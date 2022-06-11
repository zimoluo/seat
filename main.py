from library.gui import GUI
import tkinter as tk

def test():
    seat = tk.Tk()
    gui = GUI(seat)

    seat.mainloop()

if __name__ == '__main__':
    test()