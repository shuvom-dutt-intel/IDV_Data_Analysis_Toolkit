from tkinter import *
# from fublet_lib_SIU import *
# from general_lib_SIU import *
# from IDV_fublet_comparison_SIU import *
# from rollup_data import rollup_data
#from cbidvdata_SIU import *
import os
from os.path import isfile,dirname,abspath
#from re import sub
#from os import remove
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#from plot_ICC import *
import PyUber
from  limgrab import *
import datetime
import csv
import statistics
import math

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


def dicc():

    ###Root sicc
    root1 = Tk()
    root1.title('DICC data analysis')
    root1.configure(background='black')
    ### Globals
    fields = [
        'Path of results: ',
        'Part: ',
        'Site: ',
        'N Work Weeks: ',
        'Output pdf name: '
    ]


    defaults = []
    step_defaults = []

    if isfile('defaults_ICC.txt'):
        filedefaults = open('defaults_ICC.txt','r')
        for line in filedefaults:
            defaults.append(line.rstrip('\r\n')) # add line and remove \r\n from it
        filedefaults.close()

    if len(defaults)<5: #Just in case defaults.txt gets empty, so program doesn't crash.
        defaults = [
            "C:\\Users\\kevinrei\\Documents\\SpringHill\\IDV\\Results",
            '8PIPCVN',
            'F28',
			'-1',
			'CI_DICC_TEST_1'
        ]


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
        e[str(j)].insert(10,defaults[j])
        e[str(j)].grid(row = j, column = 1)
        j+=1

    # Add in Operation
    l[str(j)] = Label(root1, text="Operation(optional)", bg  ='black', fg = 'white')
    l[str(j)].grid(row = j, sticky=E)
    e[str(j)] = Entry(root1, width=80, bd =3, relief = FLAT)
    e[str(j)].insert(10,defaults[j])
    e[str(j)].grid(row = j, column = 1)
    j += 1

    # Add in Lots
    l[str(j)] = Label(root1, text="Lot(s)(optional)", bg  ='black', fg = 'white')
    l[str(j)].grid(row = j, sticky=E)
    e[str(j)] = Entry(root1, width=80, bd =3, relief = FLAT)
    e[str(j)].insert(10,defaults[j])
    e[str(j)].grid(row = j, column = 1)
    j += 1

    # Color button
    frame_color = Frame(root1, height=35, width=35, bd=1, relief=FLAT, bg = 'green')
    frame_color.grid(row = 3, column = 4, rowspan = 3)


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
		
        CB_method = "SCPREFETCH"
        cblocation = cbilocator()
        
        if not e["6"].get():      
            outfPRE = cblotdata(location, e, cblocation, CB_method)	
            lots, num_wfrs, operation = postprolots(outfPRE, CB_method)
        else:
            lots = e["6"].get().split(',')
            if not e["5"].get():
                operation = None
            else:
                operation = e["5"].get()
            num_wfrs = len(lots)
            
        filedefaults = open('defaults_ICC.txt','w')
        for l in range(len(e)):
            filedefaults.write(str(e[str(l)].get())+"\n")
        filedefaults.close()        
        
        dicctokendefault = getdefaults("defaults_DICC_tokens.txt")
        tokenlist = ["PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_COREDICC_CALC_PP_IADICC0_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_COREDICC_CALC_PP_IADICC0_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_COREDICC_CALC_PP_IADICC1_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_COREDICC_CALC_PP_IADICC1_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE2_DICC_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE2_DICC_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE2_DICC_V3","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE3_DICC_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE3_DICC_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE3_DICC_V3","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE4_DICC_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE4_DICC_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE4_DICC_V3","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE5_DICC_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE5_DICC_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE5_DICC_V3","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE6_DICC_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE6_DICC_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE6_DICC_V3","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE7_DICC_V1","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE7_DICC_V2","PTH_POWER::POWER_X_SCREEN_K_BEGIN_X_X_X_X_ICEBO_DICC_CALC_PP_ICE7_DICC_V3"]        
        CB_method = "SCDICEDIST" 
        dtype = "DIERTD"
        outfDD = cbdddata(location, e, cblocation, CB_method, lots, operation, tokenlist, dtype)	     
        postprolots(outfDD, CB_method)        
        mkplotdicc(outfDD + "_todelete.csv", dicctokendefault)

        # return the green color
        frame_color = Frame(root1, height=35, width=35, bd=1, relief=FLAT, bg = 'green')
        frame_color.grid(row = 6, column = 4, rowspan = 3)
        print("\nDone :) \n")
     
    
    def getdefaults(dfile):
        defaults = []
        with open(dfile,'r') as df:
            for line in df:
                if line != "":
                    defaults.append(line.strip('\n'))
        df.close()
        return defaults
    

    def yellow(dummy):
        global frame_color
        frame_color = Frame(root1, height=35, width=35, bd=1, relief=FLAT, bg = 'yellow')
        frame_color.grid(row = 6, column = 4, rowspan = 3)



    ### Event functions
    button = Button(root1, text="GO!", height = 1, width = 10)#, command=GO,)
    button.grid(row = 0, column = 4, rowspan = 2 )

    button.bind( "<ButtonPress-1>", yellow, add="+") #For the yellow color indicator
    button.bind( "<ButtonRelease-1>", GO, add="+") #For the plots


def sicc():
    #SICC paths etc.
    global analysis_type
    global pre_type
    global comparison
    analysis_type = 'SICC'
    pre_type = 'TPI_SIU_STATIC::'
    comparison = 0
    makeICCwindow()


def vcc():
    #VCC paths etc.
    global analysis_type
    global pre_type
    global comparison
    analysis_type = 'VCC'
    pre_type = 'TPI_VCC::'
    comparison = 0
    makeICCwindow()

    
def makeICCwindow():
    ###Root sicc
    root1 = Tk()
    root1.title(analysis_type + ' Data Analysis')
    root1.configure(background='black')
    ### Globals
    # fields = [
    #     'Output Dir: ',
    #     'Output Name:',
    #     'Site: ',
    #     'Part(optional): ',
    #     'N Work Weeks(optional): ',
    #     'Operation(optional): ',
    #     'Lots(optional): ',
    #     'TP Path(optional): ',
    #     'Test Program Name(optional): ' 
    # ]
    fields = [
        'Output Dir',
        'Output Name',
        'Site',
        'PartID',
        'N Work Weeks',
        'Operation',
        'Lots',
        'Test Program Name', 
        'TP Path'
    ]
    
    compFields = [
         'Site',
         'PartID',
         'N Work Weeks',
         'Operation',
         'Lots',
         'Test Program Name' 
    ]


    defaults = []
    step_defaults = []
    defaults_file = 'defaults_' + analysis_type + '_inputs.txt'

    if isfile(defaults_file):
        filedefaults = open(defaults_file,'r')
        for line in filedefaults:
            defaults.append(line.rstrip('\r\n')) # add line and remove \r\n from it
        filedefaults.close()

    if len(defaults)<9: #Just in case defaults.txt gets empty, so program doesn't crash.
        defaults = [
            "C:\\Users\\kevinrei\\Documents\\Creativity\\SICC_Data_Analysis\\",
            'Test',
            'F24',
            '8PEBCVA',
			'-1',
            '132110',
            'H00681801',
            'RKL%',
            'I:\program\1272\eng\hdmtprogs\rkl_sds\kevinrei\81F_Patch_1'
        ]
    

    labels = {}
    user_inputs = {}
    j = 0
    for field_item in fields:
        labels[j] = Label(root1, text = field_item + ': ', bg  ='black', fg = 'white')
        labels[j].grid(row = j, sticky=E)
        user_inputs[field_item] = Entry(root1, width=80, bd =3, relief = FLAT)
        user_inputs[field_item].insert(10,defaults[j])
        user_inputs[field_item].grid(row = j, column = 1)
        j+=1
        
    user_comp_inputs = {}   
    user_comp_inputs['Output Dir'] = user_inputs['Output Dir']
    user_comp_inputs['TP Path'] = user_inputs['TP Path']
    user_comp_inputs['Output Name'] = user_inputs['Output Name']


    green(root1)
    ### Event functions
    buttonComp = Button(root1, text="Compare", height = 1, width = 10, command=lambda: compareFields(root1, compFields, user_comp_inputs))
    buttonComp.grid(row = 1, column = 4, rowspan = 2 )
    
    buttonGo = Button(root1, text="GO!", height = 1, width = 10, command=lambda: GO(root1, user_inputs, user_comp_inputs))
    buttonGo.grid(row = 0, column = 4, rowspan = 2 )
    buttonGo.bind( "<ButtonPress-1>", lambda event: yellow(root1)) #For the yellow color indicator
    root1.mainloop()
    

def compareFields(root1, compFields, user_comp_inputs):
    global comparison
    comparison = 1
    k = 2
    for field_item in compFields:
        user_comp_inputs[field_item] = Entry(root1, width=80, bd =3, relief = FLAT)
        user_comp_inputs[field_item].grid(row = k, column = 2)
        k+=1
    
def checkInputs(root1, user_inputs):
    if user_inputs['Site'].get() == '':
        print("Must provide a Site")
        green(root1)
        return 0
    elif user_inputs['Lots'].get() == '' and user_inputs['PartID'].get() == '':
        print("Must enter either Part ID or Lots(s)")
        green(root1)
        return 0
    elif user_inputs['Lots'].get() == '' and (user_inputs['N Work Weeks'].get() == '' or user_inputs['Operation'].get() == ''):
        print("If not using lots, must use Part ID, Operation and Last N Work Weeks")
        green(root1)
        return 0    
    if user_inputs['Output Dir'].get()[-1] != '\\':
        output_path = user_inputs['Output Dir'].get()
        user_inputs['Output Dir'].delete(0, END)
        user_inputs['Output Dir'].insert(0, output_path + '\\')
    if user_inputs['TP Path'].get()[-1] != '\\':
        tp_path = user_inputs['TP Path'].get()
        user_inputs['TP Path'].delete(0, END)
        user_inputs['TP Path'].insert(0, tp_path + '\\')
    return 1



### Handler functions for events
def GO(root1, user_inputs, user_comp_inputs):
    
    if not checkInputs(root1, user_inputs) :
        return
    elif comparison:
        if not checkInputs(root1, user_comp_inputs):
            return
    
    
    print("Inputs are ok")
#    return
#    yellow(root1)

    print("Saving Defaults")
    
    with open('defaults_' + analysis_type + '_inputs.txt', 'w') as filedefaults:
        for key in user_inputs:
            filedefaults.writelines(user_inputs[key].get() + '\n')
        filedefaults.close()
    
    print("Fetching limits ...")
    
    try:
        tokens_limits_dict = limitgrabber(user_inputs['TP Path'].get(), analysis_type)
    except:
        print(user_inputs['TP Path'].get() + " is not a valid path")
        green(root1)
        return
    
    print("Limits fetched")
    
    tokens_default = []
    for key, value in tokens_limits_dict.items():
        tokens_default.append(key)
        
    tokens_instonly = toinstanceonly(tokens_default)
    tokens_avg_str = toavgonly(tokens_instonly)
    tokens_case_str = tocaseonly(tokens_default, tokens_instonly)
    quote_str = toquonly(tokens_default)
    as_str = toasonly(tokens_instonly)
    
    print("Writing SQL script ...")
    uber_script = writeSQLscript(user_inputs, tokens_avg_str, as_str, tokens_case_str, quote_str)
    print("Pulling data ...") 
    try:
        conn = PyUber.connect(datasource=(user_inputs['Site'].get() + "_PROD_ARIES"))
    except:
        print(user_inputs['Site'].get() + "_PROD_ARIES failed, check Site is correct")
        green(root1)
        return
    curr = conn.cursor()
    curr.execute(uber_script)
    curr.to_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv")
    print("Creating CSV ...")   
    # nominus999(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv")
    # print("Removing -999's ...")
    # token_max_values = get_max_values(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv", 0.25, 0.75)
    # df1 = pd.read_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv")
    # df1['DATA'] = ['NEW'] * len(df1.index)
    # df1.to_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv")
        

    if comparison:
        print("Writing comparison SQL script ...")
        uber_script = writeSQLscript(user_comp_inputs, tokens_avg_str, as_str, tokens_case_str, quote_str)
        print("Pulling comparison data ...") 
        conn = PyUber.connect(datasource=(user_comp_inputs['Site'].get() + "_PROD_ARIES"))
        curr = conn.cursor()
        curr.execute(uber_script)
        # curr.to_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_Comparison_SQL_Output.csv")
        df1 = pd.read_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv")
        df2 = pd.DataFrame(data=curr, columns=df1.columns)
        print("Creating comparison CSV ...")   
        # nominus999(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_Comparison_SQL_Output.csv")
        # print("Removing -999's ...")
        # token_max_values_comp = get_max_values(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_Comparison_SQL_Output.csv", 0.25, 0.75)
        # df2 = pd.read_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_Comparison_SQL_Output.csv")
        df1['DATA'] = ['NEW'] * len(df1.index)
        df2['DATA'] = ['REFERENCE'] * len(df2.index)
        # df2.to_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_Comparison_SQL_Output.csv")
        dfconcat = pd.concat([df1, df2])
        dfconcat.to_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv")
        

#    standardised_CSV(analysis_type + "_SQL_Output.csv", analysis_type, token_max_values, user_inputs)
    
#    standardised_data_values = get_max_values(analysis_type + "_Standardised_SQL_Output.csv", 0.25, 0.75)

    print("Removing -999's ...")
    nominus999(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv")
    
    print("Calculating parameters ...")
    token_max_values = get_max_values(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv", 0.25, 0.75)
    
#    stack_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv", user_inputs)
            
    writeJMPscript(user_inputs, tokens_limits_dict, tokens_instonly, token_max_values)
    
    print("Running JMP ...")
    
    os.system('"' + user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_JMP_script.jsl\"")
    
    green(root1)
    print("\nDone :) \n")


def writeJMPscript(user_inputs, limits_dict, tokens_instonly, token_max_values):
    sql_output_path = user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_Output.csv"
    with open(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_JMP_script.jsl", "w") as jmpscpt:
        jmpscpt.write("//!\ndt = open(\"" + sql_output_path + "\");\n\nmydist = dt << Distribution(\n\tStack( 1 ),\n")
        for token in tokens_instonly:
            jmpscpt.write("\tContinuous Distribution(\n\t\tColumn(\n\t\t\t:Name(\n\t\t\t\t\"" + token + "\"\n\t\t\t)\n\t\t),\n\t\tHorizontal Layout( 1 ),\n\t\tVertical( 0 ),\n\t\tNormal Quantile Plot( 1 )\n\t),\n")
        jmpscpt.write("\tSendToReport(\n")
        for token in tokens_instonly:
            jmpscpt.write("\t\tDispatch(\n\t\t\t{\"" + token + "\"},\n\t\t\t\"1\",\n\t\t\tScaleBox,\n\t\t\t{Min( " + str(token_max_values[token]['min'] - 0.5*abs(token_max_values[token]['min'])) + " ),\n\t\t\tMax( " + str(max(token_max_values[token]['max'], limits_dict[pre_type + token]["limit_high"])*1.1) + " ),\n\t\t\tAdd Ref Line( " + str(limits_dict[pre_type + token]["clamp_high"]) + ", \"Solid\", \"Black\", \"Clamp High\", 1),\n\t\t\tAdd Ref Line( " + str(limits_dict[pre_type + token]["limit_high"]) + ", \"Solid\", \"Medium Dark Red\", \"Limit High\", 1)\n\t\t\t},\n\t\t\tBorder Box( 3 ),\n\t\t\t{Set Summary Behavior( \"Collapse\" )}\n\t\t),\n")
        jmpscpt.write("\t)\n);")
        
        if comparison:
            jmpscpt.write("mydistrep = mydist << Report;\nmydistfbox = mydistrep[Frame Box( 1 )];\nmydistfbox << Row Legend(\"DATA\", Color( 1 ), Marker( 1 ));")
            
        # jmpscpt.write("\n\n\ndt = Current Data Table();\nfor (i = 6, i <= ncols(dt), i++,\n\tcolumn(dt, i) << data type(numeric);\n\tcolumn(dt, i) << set modeling type(continuous);\n );\n\ndt << Stack(\n\tColumns(")
        # for key in token_max_values.keys():
        #     jmpscpt.write("\n\t\t:" + key + ",")
        # jmpscpt.write("\n\t),\n\tSource Label Column( \"Label\" ),\n\tStacked Data Column( \"Data\" ),\n\tOutput Table( \"" + user_inputs['Output Name'].get() + "_Stacked\" )\n);")
    jmpscpt.close()
    return


def stack_csv(csv_file, user_inputs):
    df = pd.read_csv(csv_file)
    stacked_df = df.melt(id_vars=['LOT', 'WAFER_ID', 'SORT_X', 'SORT_Y', 'INTERFACE_BIN'])
    stacked_df['Voltage'] = '';
    stacked_df['Supply'] = '';
    stacked_df['Socket'] = '';
    Stacked_df['Flow'] = '';    
    
    stacked_df.to_csv(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_Stacked_SQL_Output.csv")
    return
        

def standardised_CSV(csv_file, token_data_values, user_inputs):
    standardised_data = []
    cell_row = []
    stdev_row = 0
    df = pd.read_csv(csv_file)
    headers = df.columns[5:]
    cols = np.append(df.columns.values, ['Median', 'Standard Deviation'])
    standardised_data.append(cols)
    for index, row in df.iterrows():
        cell_row[0:5] = row.values[0:5]
        for cell, header in zip(row[5:], headers):
            standardised_cell = (cell - token_data_values[header]['med']) / (token_data_values[header]['qhigh'] - token_data_values[header]['qlow'])
            cell_row.append(standardised_cell)
        cell_row.append(statistics.median(cell_row[5:]))
        for cl in cell_row[5:]:
            if not np.isnan(cl):
                stdev_row += (((cl - statistics.median(cell_row[5:])) ** 2) / len(headers))
        cell_row.append(math.sqrt(stdev_row))
        standardised_data.append(cell_row.copy())
        cell_row.clear()
        stdev_row = 0
    with open(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_Standardised_SQL_Output.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(standardised_data)
    f.close()
    return


def get_max_values(sql_output_path, qlow, qhigh):
    data_values = {}
    df = pd.read_csv(sql_output_path)
    headers = df.columns[5:]
    for header in headers:
        if header == 'DATA':
            continue
        else:
            data_values[header] = {}
            data_values[header]['max'] = df[header].max()
            data_values[header]['min'] = df[header].min()
            data_values[header]['qlow'] = df[header].quantile(qlow)
            data_values[header]['qhigh'] = df[header].quantile(qhigh)
            data_values[header]['med'] = df[header].median()
    return data_values


def writeSQLscript(user_inputs, tokens_avg_str, as_str, tokens_case_str, quote_str):
    with open(analysis_type + "_SQL_Query_Template.spfsql",'r') as sqlreadfile:
        uber_script = sqlreadfile.read()
    sqlreadfile.close()
    
    if user_inputs['Operation'].get():
        uber_script = uber_script.replace('##OPERATION##', '\t\t\t\t\t\tAND\tv0.operation = \'' + user_inputs['Operation'].get() + '\'\n')
    else:
        uber_script = uber_script.replace('##OPERATION##', '')        
    if user_inputs['Lots'].get():
        lot_string = '\t\t\t\t\t\tAND\tv0.lot In (\''
        lot_list = user_inputs['Lots'].get().split(',')
        for lot in lot_list:
            lot_string = lot_string + lot + '\',\''
        lot_string = lot_string + '\')\n'
        uber_script = uber_script.replace('##LOT##', lot_string)
    else:
        uber_script = uber_script.replace('##LOT##', '')        
    if user_inputs['Test Program Name'].get():
        uber_script = uber_script.replace('##TESTPROGRAM##', '\t\t\t\t\t\tAND\tv0.program_name Like \'' + user_inputs['Test Program Name'].get() + '\'\n')
    else:
        uber_script = uber_script.replace('##TESTPROGRAM##', '')        
    if user_inputs['PartID'].get():
        uber_script = uber_script.replace('##PRODUCT##', '\t\t\t\t\t\tAND\tv0.devrevstep = \'' + user_inputs['PartID'].get() + '\'\n')
    else:
        uber_script = uber_script.replace('##PRODUCT##', '')        
    if user_inputs['N Work Weeks'].get():
        today = datetime.datetime.now()
        n_ww = abs(int(user_inputs['N Work Weeks'].get()))
        n_ww_diff = datetime.timedelta(weeks = n_ww)
        n_ww_date = today - n_ww_diff
        uber_script = uber_script.replace('##TIME##', '\t\t\t\t\t\tAND\tv0.test_end_date_time Between To_Date(\'' + str(n_ww_date.strftime('%d-%b-%Y %H:%M:%S')) + '\',\'dd-Mon-yyyy hh24:mi:ss\') AND To_Date(\'' + str(today.strftime('%d-%b-%Y %H:%M:%S')) + '\',\'dd-Mon-yyyy hh24:mi:ss\')') 
    else:
        uber_script = uber_script.replace('##TIME##', '')

    uber_script = uber_script.replace('##AVGLIST##', tokens_avg_str)
    uber_script = uber_script.replace('##ASLIST##', as_str)
    uber_script = uber_script.replace('##CASELIST##', tokens_case_str)
    uber_script = uber_script.replace('##PARAMLIST##', quote_str)        
    
    with open(user_inputs['Output Dir'].get() + user_inputs['Output Name'].get() + "_SQL_script.spfsql", "w") as sqlwritefile:
        sqlwritefile.write(uber_script)
    sqlwritefile.close()
    return uber_script


    
        
def nominus999(csvfile):
    res=[]
    with open(csvfile) as f:
        content=csv.reader(f,delimiter=',')
        for row in content:
            for str in range (len(row)):
                row[str]=row[str].replace('-999','')
            res.append(row)
        f.close()
    with open(csvfile,'w') as ff:
        sw=csv.writer(ff,delimiter=',',quoting=csv.QUOTE_MINIMAL)
        for rows in res:
            sw.writerow(rows)
    ff.close()

    
    
def toasonly(tokenlist):
    new_str = ""
    for token in tokenlist:
        newtoken = "," + token + " AS " + token
        new_str = new_str + "\n\t" + newtoken
    return new_str

def toquonly(tokenlist):
    new_str = ""
    firstline = 0
    for token in tokenlist:
        if firstline == 0:
            newtoken = "'" + token + "'"
            new_str = new_str + "\n\t\t\t\t\t\t" + newtoken
            firstline += 1
        else:
            newtoken = ",'" + token + "'"
            new_str = new_str + "\n\t\t\t\t\t\t" + newtoken
    return new_str


def tocaseonly(tokenlist, instlist):
    new_str = ""
    for x in range(0, len(tokenlist)):
        newtoken = ",CASE WHEN t0.test_name = '" + tokenlist[x] + "' THEN pr.numeric_result ELSE NULL END AS " + instlist[x]
        new_str = new_str + "\n\t\t" + newtoken
    return new_str


def toavgonly(tokenlist):
    new_str = ""
    for token in tokenlist:
        newtoken = ",Avg(" + token + ") AS " + token
        new_str = new_str + "\n\t" + newtoken
    return new_str
 
 
def toinstanceonly(tokenlist):
    newlist = []
    for token in tokenlist:
        if "::" in token:
            for x in range(0, len(token)):
                if token[x:x+2] == "::":
                    token = token[x+2:]
                    break
        newlist.append(token)
    return newlist
 

def getdefaults(dfile):
    defaults = []
    with open(dfile,'r') as df:
        for line in df:
            if line != "":
                defaults.append(line.strip('\n'))
    df.close()
    return defaults


def yellow(root):
    frame_color = Frame(root, height=35, width=35, bd=1, relief=FLAT, bg = 'yellow')
    frame_color.grid(row = 3, column = 4, rowspan = 3)


def green(root):
    frame_color = Frame(root, height=35, width=35, bd=1, relief=FLAT, bg = 'green')
    frame_color.grid(row = 3, column = 4, rowspan = 3)



