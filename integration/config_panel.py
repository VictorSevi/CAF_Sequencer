import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import CAFTestingFwk as fwk
import sign_in_menu


prt=fwk.protocol("","")

class config_pan():
    def __init__(self,running_app, config_json):
        self.app = running_app
        self.config_json = config_json

        

    

def main():
    #app = gui(root)
    #root.mainloop()
    root1 = tk.Tk()
    a=app()
    m=sign_in_menu.sign_in(root1,a)
    root1.mainloop()

    if(m.passed()):
        root2= tk.Tk()
        g=gui(root2,a)
        root2.mainloop()

if __name__ == "__main__":
    main()

