import re

def ituff_data(stepobject):# necessary inputs: ituff, corner, osc_vector, outputdata, SITE
    output_file_name = str(stepobject.lco.location) + re.sub(r"\s", "_", str(stepobject.name))
    output_file = open(output_file_name,'w')
    output_file.write("SITE\tLOT\tWAFER\tX\tY\tFUBLET\tOSC\tOVERFLOW\tIDV\n")

    corner = stepobject.lco.corner[:-1] ### remove the last character
    print(corner)
    if len(corner)<3:
        corner = "0"+str(corner)
    oscillator = stepobject.lco.osc
    REGEX = stepobject.site #Used to match the IDV lines
    print(REGEX)
    print(corner)


    LOT = 'default'
    WAFER = 'default'
    X = '0'
    Y = '0'

    for osc in oscillator:
        print(osc)
        for itufffiles in stepobject.lotwafer:
            itufffile = open(itufffiles.strip(),'r')
            linestatus = 0
            for line in itufffile:
                if (re.match(".*_lotid_.*$", line, flags = 0)): LOT = re.match( r".*_lotid_(.*)$", line, flags = 0).group(1)
                if (re.match(".*_wafid_.*$", line, flags = 0)): WAFER = re.match( r".*_wafid_(.*)$", line, flags = 0).group(1)
                if (re.match(".*_xloc_.*$", line, flags = 0)): X = re.match( r".*_xloc_(.*)$", line, flags = 0).group(1)
                if (re.match(".*_yloc_.*$", line, flags = 0)): Y = re.match( r".*_yloc_(.*)$", line, flags = 0).group(1)

                if linestatus == 3 and not re.match( ".*_tname_.*", line):
                    fub_freq = re.match( r".*composite\_(.*)\_(.*)", line, flags = 0)
                    FUBLET = fub_freq.group(1)
                    print(FUBLET)
                    OVERFLOW = 0
                    if len(str(fub_freq.group(1)))>5 and re.match( r"100(.*)", fub_freq.group(1), flags = 0): ## Change from >4 to >5 for CNL & SPH
                        print(str(fub_freq.group(1)))
                        OVERFLOW = 1
                        FUBLET = re.match( r"100(.*)", fub_freq.group(1), flags = 0).group(1)
                        print("Overflow for fublet: "+str(FUBLET)+" and oscillator: "+str(osc))
                    print("Fublet: " + str(fub_freq.group(1)) + ", Freq: " + str(fub_freq.group(2)))
                    output_file.write(str(REGEX)+"\t"+str(LOT)+"\t"+str(WAFER)+"\t"+str(X)+"\t"+str(Y)+"\t"+str(FUBLET)+"\t"+str(osc)+"\t"+str(OVERFLOW)+"\t"+str(fub_freq.group(2))+"\n")
                if re.match( ".*"+str(REGEX)+".*", line):
                    linestatus = 1
                if linestatus == 1 and re.match(".*vccp_" + str(corner) + ".*", line):
                    linestatus = 2
                if linestatus == 2 and re.match(".*category_" + str(osc) + "$", line):
                    linestatus = 3
                if re.match( "^._tname_.*", line) and not re.match( ".*"+str(REGEX)+".*", line):
                    linestatus = 0
            itufffile.close()
    output_file.close()



def ituff_all_osc(stepobject):# necessary inputs: ituff, corner, osc_vector, outputdata, SITE

    corner = stepobject.lco.corner[:-1] ### remove the last character
    if len(corner)<3:
        corner = "0"+str(corner)
    REGEX = stepobject.site #Used to match the IDV lines
    #print(REGEX)
    #print(corner)
    osc_array = []

    for itufffiles in stepobject.lotwafer:
        itufffile = open(itufffiles.strip(),'r')
        linestatus = 0
        for line in itufffile:
            if re.match( ".*"+str(REGEX)+".*", line):
                linestatus = 1
            if linestatus == 1 and re.match(".*_vccp_" + str(corner) + ".*", line):
                linestatus = 2
            if linestatus == 2 and re.match(".*_comnt_A\!_category_.*$", line):
                osc = re.match(".*_comnt_A\!_category_(.*)$", line)
                osc_array.append(str(osc.group(1)))
                linestatus = 3
            if re.match( "^._tname_.*", line):
                linestatus = 0
        itufffile.close()

        osc_array = sorted(list(set(osc_array)))
        print(osc_array)
        return osc_array