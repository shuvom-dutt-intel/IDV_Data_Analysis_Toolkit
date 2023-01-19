from tkinter import *
from functions_call_ICC import *
from tkinter import ttk
from IDV_data_analysis_toolkit import *

### For matplot lib not to crash in the exe file:
import ctypes
import sys

if getattr(sys, 'frozen', False):
  # Override dll search path.
  ctypes.windll.kernel32.SetDllDirectoryW('C:/Users/RMENCHON/AppData/Local/Continuum/Anaconda3/envs/p34/Library/bin/')
  # Init code to load external dll
  ctypes.CDLL('mkl_avx2.dll')
  ctypes.CDLL('mkl_def.dll')
  ctypes.CDLL('mkl_vml_avx2.dll')
  ctypes.CDLL('mkl_vml_def.dll')

  # Restore dll search path.
  ctypes.windll.kernel32.SetDllDirectoryW(sys._MEIPASS)
  


### Main Root
root = Tk()
root.title('Data analysis toolkit')

mainframe = ttk.Frame(root, padding="100 100 100 100")
mainframe.grid(column=0, row=0, sticky=('news'))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

image = PhotoImage(file = "IDV_Tool_Kit.png")
background_label = Label(mainframe, image=image)
background_label.place(relx=0.5, rely=0.5, anchor=CENTER)

#### Main buttons
# button_dicc = Button(mainframe, text="DICC data analysis", height = 1, width = 20, command = dicc, borderwidth = 4, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
# button_dicc.grid(row = 0, column = 2, rowspan = 1 )

button_vcc = Button(mainframe, text="VCC data analysis", height = 1, width = 20, command = vcc, borderwidth = 4, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
button_vcc.grid(row = 1, column = 2, rowspan = 1 )

button_sicc = Button(mainframe, text="SICC data analysis", height = 1, width = 20, command = sicc, borderwidth = 4, bg = 'green', fg = 'orange', font = '-family "SF Espresso Shack" -size 12')
button_sicc.grid(row = 2, column = 2, rowspan = 1 )


button_fublet = Button(mainframe, text="Fublet data analysis", height = 1, width = 20, command = fublets, borderwidth = 4, bg = 'white', fg = 'black', font = '-family "SF Espresso Shack" -size 12')
button_fublet.grid(row = 3, column = 2, rowspan = 1 )


button_rollup = Button(mainframe, text="Rollup data analysis", height = 1, width = 20, command = rollups, borderwidth = 4, bg = 'orange', fg = 'green', font = '-family "SF Espresso Shack" -size 12')
button_rollup.grid(row = 4, column = 2, rowspan = 1 )



### Main loop
root.mainloop()