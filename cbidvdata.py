from subprocess import call
from re import sub
from os import remove
from general_lib import *


def cbidvdata(stepobject, cblocation, xmlidv):
    #print(stepobject.name)
    #stepobject.printdetails()
    
    ##### CB script and data saved from script
    output_file = str(stepobject.lco.location) + sub(r"\s", "_", str(stepobject.name))
    scriptpath = str(stepobject.lco.location)+sub(r"\s", "_", str(stepobject.name)) + "_cb_script.acs"
    print("Path for script: %s" % scriptpath)
    #output_file = str(stepobject.lco.location)+ re.sub(r"\s", "_", str(lw))
    print("Output file: %s" % output_file)

    fo = open(scriptpath,'w')
    
    
    CB_method = "IDVRAW"
    if CB_method == "IDVDATA":   
        fo.write("<collection type=material >\n<group >\n")
        for lw in stepobject.lotwafer:
            fo.write(lw + "   SITE=" + str(stepobject.site) + "\n")
        fo.write("</group >\n</collection >\n")
        fo.write("<analysis app=cb  >\nTOOL=IDVDATA\n/FORMAT=TEXT\n/")
        fo.write("OUTPUT='" + str(output_file)+"'\n")
        fo.write("/OUTPUTTYPE=RAW\n")
        fo.write("IDV_TEST_NAME=IDV*" + str(stepobject.lco.corner) + "*\n")
        fo.write("OSC=")
        for j in stepobject.lco.osc: fo.write(str(j) + ",")
        fo.write("\n/NORESOLVE7\n/MEAN\n/OVERFLOW\n/LASTSORT\n/RAWDATA\n/ASMERLIN\n</analysis>")

    if CB_method == "IDVRAW":   
        fo.write("<collection type=material >\n<group >\n")
        for lw in stepobject.lotwafer:
            fo.write(lw + "   SITE=" + str(stepobject.site) + "\n")
        fo.write("</group >\n</collection >\n")
        fo.write("<analysis app=cb  >\nTOOL=IDVRAW\n")
        fo.write("IDVTESTNAME=IDV*" + str(stepobject.lco.corner) + "*\n")
        fo.write("OSCILLATOR=")
        for j in stepobject.lco.osc: fo.write(str(j) + ",")
        fo.write("\nOUTPUT='" + str(output_file)+"_todelete'\n")
        fo.write("SITE=" + str(stepobject.site) + "\n")
        fo.write("OPERATION=" + str(stepobject.ope) + "\n")
        fo.write("WAFERLAST=Y\n")
        fo.write("\n/ASMERLIN\n</analysis>")
   
    
    fo.close()

    cbicall = sub(r"\n", "", str(cblocation) + " tool=runscript script=" + str(scriptpath))
#    cbicall = sub(r"\n", "", "C:\\Users\\kevinrei\\CrystalBall\\Production\\CBCLI.exe" + " tool=runscript script=" + str(scriptpath))
    print("CBI call: %s" % cbicall)
    call(cbicall)#, stdout=open(os.devnull, 'wb'))
    #remove(scriptpath)


    if CB_method == "IDVRAW":   
        import csv
        with open(str(output_file)+"_todelete", "r") as fp_in, open(str(output_file), "w") as fp_out:
            reader = csv.DictReader(fp_in, delimiter=",")
            fieldnames = ['SITE','LOT','WAFER','X','Y','FUBLET','OSC','OFUF','VALUE','FX','FY','FP','FPX','FPY','IB','TESTNAME','TESTSTRUCT','X_POS','Y_POS']
#            fieldnames = ['SITE','LOT','WAFER','X','Y','FUBLET','OSC','OFUF','VALUE','FX','FY','FP','FPX','FPY','IB','TESTNAME','X_POS','Y_POS']
            writer = csv.DictWriter(fp_out, fieldnames=fieldnames, delimiter=",")
            # reorder the header first
            writer.writeheader()
            for row in reader:
                #del row[9:18]
                #del row[16:18]
                #del row[13:14]
                #del row[5:11]
                writer.writerow(row)

        # Read in the file
        with open(output_file, 'r') as file :
          filedata = file.read()
        # Replace the target string
        filedata = filedata.replace(',,', ',0,')
        filedata = filedata.replace(',', '\t')
        filedata = filedata.replace('\n\n', '\n')
        # Write the file out again
        with open(output_file, 'w') as file:
          file.write(filedata)
        remove(str(output_file)+"_todelete")
    #input("hola")

### SQL for rollups
def cbsql(location, name, site, lotwafer, cblocation, to_include, to_exclude):
    #print(stepobject.name)
    #stepobject.printdetails()
    ##### CB script and data saved from script
    to_include = to_include.replace('.*', '%')## SQL regex is different
    to_exclude = to_exclude.replace('.*', '%')## SQL regex is different
    to_include = to_include.replace('*', '%')## SQL regex is different
    to_exclude = to_exclude.replace('*', '%')## SQL regex is different

    output_file = str(location) + sub(r"\s", "_", str(name))
    scriptpath = str(location)+sub(r"\s", "_", str(name)) + "_cb_script.acs"
    print("Path for script: %s" % scriptpath)
    #output_file = str(stepobject.lco.location)+ re.sub(r"\s", "_", str(lw))
    print("Output file: %s" % output_file)

    fo = open(scriptpath,'w')
    fo.write("<analysis app=cb  >\n")
    fo.write("TOOL=RUNSQL\n")
    fo.write("SCHEMA=XEUS\n")
    fo.write("SITE="+ str(site)+"\n")
    fo.write("OUTPUT=" + str(output_file)+"\n")
    fo.write("/ASMERLIN\n")
    fo.write("<SQL >\n")
    fo.write("select test.TEST_NAME, apr.NUMERIC_RESULT\n")
    fo.write("from a_testing_session ats, a_parametric_result apr, a_test test\n")
    count = 0
    for lw in lotwafer:
        list_l_w = lw.split()
        if count == 0:
            fo.write("where   ((ats.LOT like '"+str(list_l_w[0])+"'")
        else:
            fo.write("or   (ats.LOT like '"+str(list_l_w[0])+"'")
        if len(list_l_w)>1:
            fo.write("    and   ats.WAFER_ID = '"+str(list_l_w[1])+"')\n")
        else:
            fo.write(")\n")
        count += 1
    fo.write(")\n")
    fo.write("and   test.TEST_NAME like '"+str(to_include)+"'\n")
    fo.write("and   test.TEST_NAME not like '"+str(to_exclude)+"'\n")
    fo.write("and   ats.lao_start_ww       = apr.lao_start_ww\n")
    fo.write("and   ats.ts_id              = apr.ts_id\n")
    fo.write("and   ats.latest_flag        = 'Y'\n")
    fo.write("and   apr.t_id               = test.t_id\n")
    fo.write("order by test.TEST_NAME\n")
    fo.write("</SQL >\n")
    fo.write("</analysis>\n")
    fo.close()

    cbicall = sub(r"\n", "", str(cblocation) + " tool=runscript script=" + str(scriptpath))
#    cbicall = sub(r"\n", "", "C:\\Users\\kevinrei\\CrystalBall\\Production\\CBCLI.exe" + " tool=runscript script=" + str(scriptpath))
    print("CBI call: %s" % cbicall)
    call(cbicall)#, stdout=open(os.devnull, 'wb'))
    remove(scriptpath)
    return output_file
