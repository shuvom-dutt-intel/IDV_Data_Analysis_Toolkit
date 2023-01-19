#######################################################################################
import re

def rollup_func_dic (rollup_dic, data_file, osc_pos, corner_pos, chain_pos, total_fields, to_include, to_exclude, ituff):
    fileopen = open(data_file,'r')
    nextline = 0

    osc = ""
    corner = ""
    chain = ""
    rollup_vector = []

    num_empty = 0
    for line in fileopen:
        if (ituff == 'yes' and re.match(r"._tname_"+str(to_include), line, flags = 0) and not re.match(r"._tname_.*testtime", line, flags = 0) and not re.match(r"._tname_.*DFF", line, flags = 0) and not re.match(r""+str(to_exclude)+"", line, flags = 0)) or \
                (re.match(r""+str(to_include)+"", line, flags = 0) and ituff == 'no'):
            if ituff == 'yes':
                rollup_line = re.match(r"._tname_(.*)$", line, flags = 0)
            else:
                rollup_line = re.match(r"(.*)\s.*\d", line, flags = 0)
            rollup_vector = rollup_line.group(1).strip().split('_') ## remove blank spaces and then separate items following "_"
            #print(max(corner_pos, osc_pos, chain_pos))
            if len(rollup_vector) == total_fields:
                osc = rollup_vector[osc_pos]
                corner = rollup_vector[corner_pos]
                if chain_pos == 'REFERENCE':
                    chain = 'REFERENCE'
                else:
                    chain = rollup_vector[chain_pos]
                nextline = 1
                #print("\n")
                #print(osc)
                #print(corner)
                #print(chain)
                #print(ituff)
            #if chain == '':
            #    print(line)

        if (ituff == 'yes' and re.match(r"._mrslt_.*$", line, flags = 0) and nextline == 1) or \
                (ituff == 'no' and re.match(r""+str(to_include)+"", line, flags = 0) and len(rollup_vector) == total_fields):
            if ituff == 'yes':
                freq_line = re.match(r"._mrslt_(.*)$", line, flags = 0)
            else:
                freq_line = re.match(r""+str(rollup_line.group(1))+"\s(.*)", line, flags = 0)
            freq = freq_line.group(1).strip()#remove possible zeros
            ### fix to sor oscillators for SKL/KBL:
            if osc == 'NESTED':
                osc = 'OSC004'
            if len(osc) == 4:
                osc = osc.replace("OSC","OSC00")
            if len(osc) == 5:
                osc = osc.replace("OSC","OSC0")

            ### arrays of frequencies created - ona value per die
            if not rollup_dic[str(corner)][str(osc)][str(chain)]:
                rollup_dic[str(corner)][str(osc)][str(chain)] = [float(freq)]
            else:
                rollup_dic[str(corner)][str(osc)][str(chain)].append(float(freq))

            #print("Corner = " + str(corner) + "\tOsc = " + str(osc) + "\tChain = " + str(chain) + "\tFreq = " + str(freq))
            if float(freq) <= 0:
                num_empty += 1
                if ituff == 'yes':
                    print("Corner = " + str(corner) + "\tOsc = " + str(osc) + "\tChain = " + str(chain) + "\tFreq = " + str(freq))
            nextline = 0
    print("Number of chains with values below zero: %d" % num_empty)
    fileopen.close()