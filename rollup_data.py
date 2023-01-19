#rollup_dic = {'700' : {'osc1' : {'core0' : 10000}}}
#print(rollup_dic['700'])
#print(rollup_dic['700']['osc1'])
#print(rollup_dic['700']['osc1']['core0'])
#print(list(rollup_dic.keys()))

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from collections import defaultdict
from numpy import linspace, median, mean, std
from general_lib import cbilocator
from cbidvdata import cbsql
from os.path import isfile, dirname, abspath
from rollup_func_dic import *

def rollup_data(statistics, ituff, ituff_ref, lotwafer, site, to_include, to_exclude, osc_pos, corner_pos,chain_pos, total_fields,
                lotwafer_ref, site_ref, to_include_ref, to_exclude_ref, osc_pos_ref, corner_pos_ref, total_fields_ref, location):
    ######################################################################################
    ### inputs ###########################################################################
    ######################################################################################
    name = ''.join(lotwafer).replace(' ', '_')#'SKL_vsKBL_rollups_1'
    #print(name)
    #print(ituff)
    #print(ituff_ref)
    # statistics = 'median'# 'median, 'mean' or, 'std'
    #
    # lotwafer = ['H6092760']#['ATT17891.1']#['ituff_edge.1']#['H616854D 373', 'H616854C']#
    # site = 'F24'
    # to_include = ".*FMAX_IDV.*"#".*IDV.*MED"
    # to_exclude = ".*ref.*"
    # ##Rollup positions starting with zero
    # osc_pos = 2#1
    # corner_pos = 4#4
    # chain_pos = 3
    # #total fields counting from 1
    # total_fields = 5
    #
    #
    # #reference to compare
    # lotwafer_ref = ['c']#['ATT17891.1']#['H5488570 731']
    # site_ref = 'F24'
    # to_include_ref = ".*FMAX_IDV.*"
    # to_exclude_ref = ".*CORE.*"
    # osc_pos_ref = 2#1
    # corner_pos_ref = 3
    # total_fields_ref = 4


    chain_pos_ref = 'REFERENCE' #Not an input
    ######################################################################################
    # end of inputs ######################################################################
    ######################################################################################


    if to_exclude == "":
        to_exclude = "nothing"

    if to_exclude_ref == "":
        to_exclude_ref = "nothing"

    cblocation = cbilocator()

    ### To select data_file properly depending on selection of Ituff or CB/file
    if ituff == 'no':
        if not isfile(str(location)+str(name)):
            data_file = cbsql(location, name, site, lotwafer, cblocation, to_include, to_exclude)
        else:
            data_file = str(location)+str(name)
    else:
        data_file = lotwafer[0]
    print(data_file)

    name_ref = ''.join(lotwafer_ref).replace(' ', '_')+"_ref"
    if ituff_ref == 'no':
        if not isfile(str(location)+str(name_ref)):
            data_file_ref = cbsql(location, name_ref, site_ref, lotwafer_ref, cblocation, to_include_ref, to_exclude_ref)
        else:
            data_file_ref = str(location)+str(name_ref)
        print(data_file_ref)
    else:
        data_file_ref = lotwafer_ref[0]

    #OLD WAY of finding if a file is ituff or CB below:
    #ituff = ''
    #if not isfile(lotwafer[0]): ##In this way with the same gui I can use it for both ituff and crystal ball, or even mix them
    #    if not isfile(str(location)+str(name)):
    #        data_file = cbsql(location, name, site, lotwafer, cblocation, to_include, to_exclude)
    #    else:
    #        data_file = str(location)+str(name)
    #    print(data_file)
    #    ituff = 'no'
    #else:
    #    data_file = lotwafer[0]
    #    ituff = 'yes'

    ##same for the reference file:
    #ituff_ref = ''
    # if not isfile(lotwafer_ref[0]): ##In this way with the same gui I can use it for both ituff and crystal ball, or even mix them
    #     if not isfile(str(location)+str(name_ref)):
    #         data_file_ref = cbsql(location, name_ref, site_ref, lotwafer_ref, cblocation, to_include_ref, to_exclude_ref)
    #     else:
    #         data_file_ref = str(location)+str(name_ref)
    #     print(data_file_ref)
    #     ituff_ref = 'no'
    # else:
    #     data_file_ref = lotwafer_ref[0]
    #     ituff_ref = 'yes'


    ######################################################################################
    ##rollup dictionary
    def nested_dict():
        return defaultdict(nested_dict)

    rollup_dic = nested_dict()

    print(to_include)

    ######################################################################################
    rollup_func_dic(rollup_dic, data_file, osc_pos, corner_pos, chain_pos, total_fields, to_include, to_exclude, ituff)
    rollup_func_dic(rollup_dic, data_file_ref, osc_pos_ref, corner_pos_ref, chain_pos_ref, total_fields_ref, to_include_ref, to_exclude_ref, ituff_ref)


    ######################################################################################

    #Remove data from sql query
    #if ituff == 'no':
        #remove(data_file)


    #########################################################################################
    #### Make the median, mean, or std of each freq array for the rollup_dic:
    for corner_item in rollup_dic:
        for osc_item in rollup_dic[str(corner_item)]:
            for chain_item in rollup_dic[str(corner_item)][str(osc_item)]:
                #print(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                if statistics == 'median':
                    rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)] = median(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                    #print(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                if statistics == 'mean':
                    rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)] = mean(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                    #print(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                if statistics == 'std':
                    rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)] = std(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                    #print(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])


    ############################################################################
    ## prepare and normalize the data for the plot
    corners_list = sorted(rollup_dic)
    oscillators_list = []
    chain_list = []


    y = nested_dict()
    chain_list = []

    for corner_item in corners_list:
        oscillators_list = sorted(rollup_dic[str(corner_item)])
        x = oscillators_list

        for osc_item in oscillators_list:
            chain_list.append(sorted(rollup_dic[str(corner_item)][str(osc_item)]))
        chain_list_extended = sorted(set().union(*chain_list))
        print(chain_list_extended)

        for osc_item in oscillators_list:
            for chain_item in chain_list_extended:
                #print(chain_item)
                if not rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)]: ### when oscillator doesn't have that rollup
                    if chain_item in y[str(corner_item)]:
                        y[str(corner_item)][str(chain_item)].append(float('NaN'))#rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                    else:
                        y[str(corner_item)][str(chain_item)] = [float('NaN')]#rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)]]
                elif not rollup_dic[str(corner_item)][str(osc_item)][str('REFERENCE')]: ### when oscillator doesn't have the fullchip rollup but some other
                    if chain_item in y[str(corner_item)]:
                        y[str(corner_item)][str(chain_item)].append(1)#rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)])
                    else:
                        y[str(corner_item)][str(chain_item)] = [1]#rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)]]
                else: ### When the oscillator is for both the chain and the chip rollup
                    if chain_item in y[str(corner_item)]:
                        if rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)] <= 0:
                            y[str(corner_item)][str(chain_item)].append(-9)
                        else:
                            y[str(corner_item)][str(chain_item)].append(rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)]/float(rollup_dic[str(corner_item)][str(osc_item)]['REFERENCE']))
                    else:
                        if rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)] <= 0:
                                y[str(corner_item)][str(chain_item)] = [-9]
                        else:
                                y[str(corner_item)][str(chain_item)] = [rollup_dic[str(corner_item)][str(osc_item)][str(chain_item)]/rollup_dic[str(corner_item)][str(osc_item)]['REFERENCE']]


    ###############################################
    ######## The plot
    #x = ['osc1', 'osc2', 'osc3', 'osc4', 'osc5']
    #y = [[10000, 8000, 8500, 8900, 8100], [10010, 8010, 8510, 8800, 8200], [9000, 7000, 7500, 8000, 8500]]

    fig = plt.figure()
    corner_num = 1
    ax = {}
    markers = ['o','s','*','p','h','v','8','d'] ###%8  http://matplotlib.org/api/markers_api.html
    for corner_item in corners_list:
        ax[str(corner_item)] = fig.add_subplot(str(len(corners_list))+"1"+str(corner_num))
        ax[str((corner_item))].set_title(str(corner_item)+ " mV", size=15)
        ax[str(corner_item)].set_xlim( -1 , len(x))  ## To leave space between y axis and data
        ax[str(corner_item)].set_xticks(range(len(x)))
        ax[str(corner_item)].set_xticklabels(x, rotation=90, size = 10)
        ax[str(corner_item)].set_ylabel('Frequency/(Reference Frequency)', size=15)   ## To set the vertical title for Frequency

        #ax[str(corner_item)].set_ylim([0.8,1.2])    ## To set the same y scale for all
        corner_num += 1
        i = 0
        color=iter(cm.jet(linspace(0,1,len(y[str(corner_item)])))) #http://matplotlib.org/examples/color/colormaps_reference.html
        for chain_item in sorted(y[str(corner_item)]):
            if chain_item == 'REFERENCE':
                ax[str(corner_item)].plot(y[str(corner_item)][str(chain_item)], 'r-', label = str(chain_item))
            else:
                c=next(color)
                ax[str(corner_item)].plot(y[str(corner_item)][str(chain_item)], c=c, linestyle = '', marker = markers[i%8], label = str(chain_item))
            i += 1
        #ax[str(corner_item)].plot(y[str(corner_item)][str('WITHGT')], 'o', label = str('WITHGT'))

    ax[str(corners_list[0])].legend(loc='center left', bbox_to_anchor=(1, 0.5*(2-len(corners_list))), prop={'size': 6})

    plt.show()