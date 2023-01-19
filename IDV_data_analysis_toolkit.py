from tkinter import *
from fublet_lib import *
from general_lib import *
from IDV_fublet_comparison import *
from rollup_data import rollup_data
from os.path import isfile,dirname, abspath
from re import sub
from os import remove

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


def fublets():

    ###Root fublets
    root1 = Tk()
    root1.title('IDV fublets data analysis')
    root1.configure(background='black')
    ### Globals
    fields = [
        'Path of results: ',
        'Corner: ',
        'Oscillators: ',
        'Reference IDV xml: ',
        'Output pdf name: '
    ]


    step_fields = [
        'Name in plot: ',
        'Lots wafers / ituffs: ',
        'Site / ituff IDV name: ',
        'Operation: '
    ]


    defaults = []
    step_defaults = []

    if isfile('defaults_IDV.txt'):
        filedefaults = open('defaults_IDV.txt','r')

        k = 0
        for line in filedefaults:
            if line!="" and line!="\n":
                if k < 7:
                    defaults.append(line.rstrip('\r\n')) # add line and remove \r\n from it
                else:
                    step_defaults.append(line.rstrip('\r\n'))
                k+=1
        filedefaults.close()

    if len(defaults)<7: #Just in case defaults_IDV.txt gets empty, so program doesn't crash.
        defaults = [
            "C:\\Users\\RMENCHON\\Documents\\rmenchon\\Innovation\\fublet_data\\results\\",
            '950',
            '4 13',
            "C:\\Users\\RMENCHON\\Documents\\rmenchon\\Innovation\\fublet_data\\IDV_FULL_950_KBL_J0.xml",
            'example1',
            'statistics',
            'median'
        ]

        step_defaults= [
            'Kstep',
            'H601278A 765',
            'F24',
            '132320'
        ]#    'Jstep_KBL_1',
        #    'L602883F 567',
        #    'F32'
        #]



    #globals defined here, I could probably define them later anyways directly.
    #loco = lco(defaults[0], defaults[1], defaults[2].split( ))
    #step1 = step(step_defaults[0], step_defaults[1].split(","), step_defaults[2], loco)
    #step2 = step(step_defaults[3], step_defaults[4].split(","), step_defaults[5], loco)

    #xmlidv = xmlitem(defaults[3], loco.corner) ##This like this fails, better xml IDV title
    #pdf_title = defaults[4]
    #each_point = e_p.get()


    ### Widgets def and placement
    global l
    global e
    global j

    l = {}
    e = {}
    j = 0
    for field_item in fields:
        l[str(j)] = Label(root1, text= field_item, bg  ='black', fg = 'white')
        l[str(j)].grid(row = j, sticky=E)
        e[str(j)] = Entry(root1, width=80, bd =3, relief = FLAT)
        e[str(j)].insert(11,defaults[j])
        e[str(j)].grid(row = j, column = 1)
        j+=1

    n_step_fields = 4 ## number of fields for each step (Name in plot, Lots wafers, Site, Operation)

    # Variable for the scrolldown menu
    e[str(j)] = StringVar(root1)
    e[str(j)].set(str(defaults[j])) # default value

    l[str(j)] = Label(root1, text= "Plot type: ", bg  ='black', fg = 'white')
    l[str(j)].grid(row = j, sticky=E)
    menu1 = OptionMenu(root1, e[str(j)], "statistics", "each point", "no plot")
    menu1.grid(row = (j), column = 1, sticky=W)
    j=j+1


    ## statistics scrolldown
    e[str(j)] = StringVar(root1) # Variable for the scrolldown menu
    e[str(j)].set(str(defaults[j])) # default value

    l[str(j)] = Label(root1, text= "Statistics: ", bg  ='black', fg = 'white')
    l[str(j)].grid(row = j, sticky=E)
    menu1 = OptionMenu(root1, e[str(j)], "median", "mean", "std")
    menu1.grid(row = (j), column = 1, sticky=W)
    j=j+1

    ##rest of fields for steps
    for step_item in step_defaults:
        l[str(j)] = Label(root1, text= step_fields[(j-len(fields)-2)%n_step_fields], bg  ='black', fg = 'white')#, font = '-slant roman')
        l[str(j)].grid(row = j, sticky=E)
        e[str(j)] = Entry(root1, width=80, bd =3, relief = FLAT)
        e[str(j)].insert(11,step_item)
        e[str(j)].grid(row = j, column = 1)
        j+=1

    print(j)

    # Color button
    frame_color = Frame(root1, height=35, width=35, bd=1, relief=FLAT, bg = 'green')
    frame_color.grid(row = 6, column = 4, rowspan = 3)


    # Dummy frames for space
    frame_color = Frame(root1, height=5, width=10, bd=1, relief=FLAT, bg = 'black')
    frame_color.grid(row = 6, column = 3)
    frame_color = Frame(root1, height=5, width=10, bd=1, relief=FLAT, bg = 'black')
    frame_color.grid(row = 6, column = 5)



    ### Handler functions for events
    def GO(dummy):
        #print("value is", e_p.get())
        #print(each_point)
        #print(e["1"].get())

        global loco
        global step_num
        global xml_title
        global pdf_title
        global plot_type
        global j
        global e
        global frame_color

        step.stepcount = 0 # reset not to keep adding them
        step.stepappend = []

        # to fix if no \ at the end of the path
        location = e["0"].get()
        if not re.match(r".*\\$", location, flags = 0):
            location = str(location) + "\\"

        # we get the osc and if it has limits too
        limits = {}
        osc_array_lim = e["2"].get().split( )
        for osci in osc_array_lim:
            if re.match(r".*\:.*", osci, flags = 0):
                lim_low = float(re.match(r".*\((.*)\:.*", osci, flags = 0).group(1))
                lim_high = float(re.match(r".*:(.*)\)", osci, flags = 0).group(1))
                limits[str(sub(r"\(.*\)", "", osci))] = [lim_low, lim_high]
            else:
                lim_low = 0.0
                lim_high = 100000000.0
                limits[str(sub(r"\(.*\)", "", osci))] = [lim_low, lim_high]
        osc_array = [sub(r"\(.*\)", "", osci) for osci in osc_array_lim]


        loco = lco(location, e["1"].get(), osc_array)

        step_num = {}

        j_before = 7 ## num oj j before the step information starts
        for i in range(int((j-j_before)/n_step_fields)): ## to create the different steps
            if e[str(j_before+n_step_fields*i)].get() != "":  ## not to add steps in field name is empty
                step_num[str(i)] = step(e[str(j_before+n_step_fields*i)].get(), e[str(j_before+1+n_step_fields*i)].get().split(","), e[str(j_before+2+n_step_fields*i)].get(), e[str(j_before+3+n_step_fields*i)].get(), loco)


        loco.printdetails()

        xml_title = e["3"].get()
        pdf_title = e["4"].get()
        plot_type = e["5"].get()
        statistics = e["6"].get()

        for step_item in step.stepappend:
            step_item.printdetails()

        print(step.stepappend)
        print(step.stepcount)

        filedefaults = open('defaults_IDV.txt','w')
        for l in range(len(e)):
            if str(e[str(l)].get())!="":
                filedefaults.write(str(e[str(l)].get())+"\n")
        filedefaults.close()

        #We run all the plots
        IDV_fublet_comparison(loco, step, xml_title, pdf_title, plot_type, limits, statistics)

        # return the green color
        frame_color = Frame(root1, height=35, width=35, bd=1, relief=FLAT, bg = 'green')
        frame_color.grid(row = 6, column = 4, rowspan = 3)
        print("\nDone :) \n")

    def yellow(dummy):
        global frame_color
        frame_color = Frame(root1, height=35, width=35, bd=1, relief=FLAT, bg = 'yellow')
        frame_color.grid(row = 6, column = 4, rowspan = 3)


    def moresteps():
        global j
        global e
        print(j)
        for i in range(4):
            l[str(j)] = Label(root1, text= step_fields[(j-len(fields)-2-len(step_defaults))%4], bg  ='black', fg = 'white')
            l[str(j)].grid(row = j, sticky=E)
            e[str(j)] = Entry(root1, width=80, bd =3, relief = FLAT)
            #e[str(j)].insert(10,step_item)
            e[str(j)].grid(row = j, column = 1)
            j+=1

    def lesssteps():
        global j
        global e
        global l
        print(j)
        if j>12:
            for i in range(4):
                l[str(j-1)].destroy()
                del l[str(j-1)]
                e[str(j-1)].destroy()
                del e[str(j-1)]
                j-=1


    ### Event functions
    button = Button(root1, text="GO!", height = 1, width = 10)#, command=GO,)
    button.grid(row = 0, column = 4, rowspan = 2 )

    button.bind( "<ButtonPress-1>", yellow, add="+") #For the yellow color indicator
    button.bind( "<ButtonRelease-1>", GO, add="+") #For the plots

    button2 = Button(root1, text="More steps", command=moresteps, height = 1, width = 10)
    button2.grid(row = 2, column = 4, rowspan = 2)

    button2 = Button(root1, text="Less steps", command=lesssteps, height = 1, width = 10)
    button2.grid(row = 4, column = 4, rowspan = 2)



###############################################################################################
###############################################################################################
###############################################################################################

def rollups():
    root2 = Tk()
    root2.title('IDV rollups data analysis')
    root2.configure(background='black')
    ### Globals
    fields = [
        'Lot wafer/ Ituff: ',
        'Site: ',
        'To include: ',
        'To exclude: ',
        'Total fields: ',
        'Oscillator pos: ',
        'Corner pos: ',
        'Chain pos: '
    ]



    defaults = []
    step_defaults = []

    if isfile('defaults_IDV_rollups.txt'):
        filedefaults = open('defaults_IDV_rollups.txt','r')

        k = 0
        for line in filedefaults:
            if line!="" and line!="\n":
                if k < 18:
                    defaults.append(line.rstrip('\r\n')) # add line and remove \r\n from it
                k+=1
        filedefaults.close()

    if len(defaults)<18: #Just in case defaults_IDV.txt gets empty, so program doesn't crash.
        defaults = [
            'median',
            'H6092760',
            'F24',
            '.*FMAX_IDV.*',
            ".*ref.*",
            '5',
            '2',
            '4',
            '3',
            "H6092760",
            'F24',
            '.*FMAX_IDV.*',
            ".*ref.*",
            '4',
            '2',
            '3',
            'no',
            'no',
        ]



    ### Widgets def and placement
    global l_r
    global e_r
    global j_r

    l_r = {}
    e_r = {}
    j_r = 0

    e_r['0'] = StringVar(root2) # Variable for the scrolldown menu
    e_r['0'].set(str(defaults[0])) # default value


    l_r[str(j_r)] = Label(root2, text= "Statistics: ", bg  ='black', fg = 'white')
    l_r[str(j_r)].grid(row = j_r, sticky=E)
    menu1 = OptionMenu(root2, e_r['0'], "median", "mean", "std")
    menu1.grid(row = (j_r), column = 1, sticky=W)
    j_r=j_r+1

    #Labels for data dn reference
    label_title_1 = Label(root2, text= 'Data to compare:', bg  ='black', fg = 'white')
    label_title_1.grid(row = 1, column = 1,  sticky = W)

    l_r[str(j_r)] = Label(root2, text= 'Reference:', bg  ='black', fg = 'white')
    l_r[str(j_r)].grid(row = 1, column = 3,  sticky = W)


    for field_item in fields:
        l_r[str(j_r)] = Label(root2, text= field_item, bg  ='black', fg = 'white')
        l_r[str(j_r)].grid(row = j_r+1, sticky=E)
        e_r[str(j_r)] = Entry(root2, width=40, bd =3, relief = FLAT)
        e_r[str(j_r)].insert(10,defaults[j_r])
        e_r[str(j_r)].grid(row = j_r+1, column = 1)
        if not field_item == 'Chain pos: ':
            e_r[str(j_r+8)] = Entry(root2, width=40, bd =3, relief = FLAT)
            e_r[str(j_r+8)].insert(10,defaults[j_r+8])
            e_r[str(j_r+8)].grid(row = j_r+1, column = 3)
        j_r+=1

    # Color button
    frame_color_r = Frame(root2, height=35, width=35, bd=1, relief=FLAT, bg = 'green')
    frame_color_r.grid(row = 6, column = 5, rowspan = 3)


    ###Ituff/CB selection
    e_r['16'] = StringVar(root2) # Variable for the scrolldown menu
    e_r['16'].set(str(defaults[16])) # default value
    #l_r[str(j_r)] = Label(root2, text= "Ituff? ", bg  ='black', fg = 'white')
    #l_r[str(j_r)].grid(row = 0, column=1, sticky = E)
    menu2 = OptionMenu(root2, e_r['16'], "Ituff", "CB or File")
    menu2.grid(row = 1, column = 1, sticky=E)

    frame_color_r = Frame(root2, height=5, width=10, bd=1, relief=FLAT, bg = 'black')
    frame_color_r.grid(row = 6, column = 2)

    ###Ituff/CB selection for reference
    e_r['17'] = StringVar(root2) # Variable for the scrolldown menu
    e_r['17'].set(str(defaults[17])) # default value
    #l_r[str(j_r)] = Label(root2, text= "Ituff for ref? ", bg  ='black', fg = 'white')
    #l_r[str(j_r)].grid(row = 0, column=2, sticky = E)
    menu3 = OptionMenu(root2, e_r['17'], "Ituff ref", "CB or File for ref")
    menu3.grid(row = 1, column = 3, sticky=E)


    # Dummy frames for space
    frame_color_r = Frame(root2, height=5, width=10, bd=1, relief=FLAT, bg = 'black')
    frame_color_r.grid(row = 6, column = 4)
    frame_color_r = Frame(root2, height=5, width=10, bd=1, relief=FLAT, bg = 'black')
    frame_color_r.grid(row = 6, column = 6)



    ### Handler functions for events
    def GO(dummy):
        global j_r
        global e_r
        global frame_color_r


        statistics          =   e_r["0"].get()
        print(statistics)

        lotwafer            =   e_r["1"].get().split(",")
        print(lotwafer)
        site                =   e_r["2"].get()
        print(site)
        to_include          =   e_r["3"].get()
        print(to_include)
        to_exclude          =   e_r["4"].get()
        if to_exclude == "":
            e_r["4"].insert(10,"empty")
        print(to_exclude)
        total_fields        =   int(e_r["5"].get())
        print(total_fields)
        osc_pos             =   int(e_r["6"].get()) - 1 #-1 because array starts counting from zero
        print(osc_pos)
        corner_pos          =   int(e_r["7"].get()) - 1 #-1 because array starts counting from zero
        print(corner_pos)
        chain_pos           =   int(e_r["8"].get()) - 1 #-1 because array starts counting from zero
        print(chain_pos)

        lotwafer_ref        =   e_r["9"].get().split(",")
        print(lotwafer_ref)
        site_ref            =   e_r["10"].get()
        print(site_ref)
        to_include_ref      =   e_r["11"].get()
        print(to_include_ref)
        to_exclude_ref      =   e_r["12"].get()
        print(to_exclude_ref)
        if to_exclude_ref == "":
            e_r["12"].insert(10,"empty")
        total_fields_ref    =   int(e_r["13"].get())
        print(total_fields_ref)
        osc_pos_ref         =   int(e_r["14"].get()) - 1#-1 because array starts counting from zero
        print(osc_pos_ref)
        corner_pos_ref      =   int(e_r["15"].get()) - 1#-1 because array starts counting from zero
        print(corner_pos_ref)
        if e_r["16"].get() == 'Ituff':
            ituff = 'yes'
        else:
            ituff = 'no'
        print(ituff)
        if e_r["17"].get() == 'Ituff ref':
            ituff_ref = 'yes'
        else:
            ituff_ref = 'no'
        print(ituff_ref)


        filedefaults = open('defaults_IDV_rollups.txt','w')
        for l in range(len(e_r)+1):
            if l!= 18 and str(e_r[str(l)].get())!="":
                filedefaults.write(str(e_r[str(l)].get())+"\n")
        filedefaults.close()

        #Location added here so when compiling is taking the folder where the exe file is, not a temp folder.
        current_location = str(dirname(abspath(__file__)))+"\\"
        print(current_location)

        #We run the main function and produce the plot
        rollup_data(statistics, ituff, ituff_ref, lotwafer, site, to_include, to_exclude, osc_pos, corner_pos,chain_pos, total_fields,
                    lotwafer_ref, site_ref, to_include_ref, to_exclude_ref, osc_pos_ref, corner_pos_ref, total_fields_ref, current_location)

        # return the green color
        frame_color_r = Frame(root2, height=35, width=35, bd=1, relief=FLAT, bg = 'green')
        frame_color_r.grid(row = 6, column = 5, rowspan = 3)
        print("\nDone :) \n")

    def yellow(dummy):
        global frame_color_r
        frame_color_r = Frame(root2, height=35, width=35, bd=1, relief=FLAT, bg = 'yellow')
        frame_color_r.grid(row = 6, column = 5, rowspan = 3)


    def Delete_CB_files():
        lotwafer            =   e_r["1"].get().split(",")
        lotwafer_ref        =   e_r["9"].get().split(",")
        if e_r["16"].get() == 'Ituff':
            ituff = 'yes'
        else:
            ituff = 'no'
        if e_r["17"].get() == 'Ituff ref':
            ituff_ref = 'yes'
        else:
            ituff_ref = 'no'

        location = str(dirname(abspath(__file__)))+"\\"
        name = ''.join(lotwafer).replace(' ', '_')
        if ituff == 'no':
            if isfile(str(location)+str(name)):
                remove(str(location)+str(name))
                print('File deleted: '+str(location)+str(name))
            else:
                print('File not found: '+str(location)+str(name))
        else:
            print("You can delete data ituff manually at: " +str(location)+str(name))
        name_ref = ''.join(lotwafer_ref).replace(' ', '_')+"_ref"
        if ituff_ref == 'no':
            if isfile(str(location)+str(name_ref)):
                remove(str(location)+str(name_ref))
                print('File deleted: '+str(location)+str(name_ref))
            else:
                print('File not found: '+str(location)+str(name_ref))
        else:
            print("You can delete reference ituff manually at: " +str(location)+str(name))

    ### Event functions
    button_1 = Button(root2, text="GO!", height = 1, width = 10)#, command=GO,)
    button_1.grid(row = 0, column = 5, rowspan = 2 )
    button_1.bind( "<ButtonPress-1>", yellow, add="+") #For the yellow color indicator
    button_1.bind( "<ButtonRelease-1>", GO, add="+") #For the plots

    button_2 = Button(root2, text="Delete CB files", height = 1, width = 12, command = Delete_CB_files)
    button_2.grid(row = 2, column = 5, rowspan = 2 )



# ### Main Root
# root = Tk()
# root.title('IDV data analysis toolkit')
# root.configure(background='black')
# #root.geometry('350x350')


# # Dummy frames for space
# spacex = 70
# spacey = 110
# frame_color_r = Frame(root, height=spacey, width=spacex, bd=1, relief=FLAT, bg = 'black')
# frame_color_r.grid(row = 1, column = 1)
# frame_color_r = Frame(root, height=spacey, width=spacex, bd=1, relief=FLAT, bg = 'black')
# frame_color_r.grid(row = 5, column = 1)
# frame_color_r = Frame(root, height=spacey, width=spacex, bd=1, relief=FLAT, bg = 'black')
# frame_color_r.grid(row = 1, column = 3)
# frame_color_r = Frame(root, height=spacey, width=spacex, bd=1, relief=FLAT, bg = 'black')
# frame_color_r.grid(row = 5, column = 3)

# frame_color_r = Frame(root, height=10, width=10, bd=1, relief=FLAT, bg = 'black')
# frame_color_r.grid(row = 3, column = 3)


# image = PhotoImage(file = "IDV_Tool_Kit.png")
# background_label = Label(root, image=image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

# #### Main buttons
# button_fublet = Button(root, text="Fublet data analysis", height = 1, width = 20, command = fublets, borderwidth = 4, bg = 'green', fg = 'white', font = '-family "SF Espresso Shack" -size 12')
# button_fublet.grid(row = 2, column = 2, rowspan = 1 )



# button_rollup = Button(root, text="Rollup data analysis", height = 1, width = 20, command = rollups, borderwidth = 4, bg = 'orange', font = '-family "SF Espresso Shack" -size 12')
# button_rollup.grid(row = 4, column = 2, rowspan = 1 )



# ### Main loop
# root.mainloop()