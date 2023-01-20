import numpy as np
from numpy import median, mean, std
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import re
from subprocess import call

#pdf_title = "ricard"
#output_file = ["Dstep_v1_4", "Kstep_v1_4"]
#xmlidv_chains = [['CORE0', '1000', '1199'], ['CORE1', '1200', '1399'], ['CORE2', '1400', '1599'], ['CORE3', '1600', '1799'], ['CBO0', '2000', '2199'], ['CBO1', '2200', '2399'], ['CBO2', '2400', '2599'], ['CBO3', '2600', '2799'], ['SA', '5000', '5199'], ['NTR', '3000', '3499'], ['MC', '4000', '4999'], ['IMGU', '3500', '3699'], ['PEGL', '5500', '5599'], ['GTU', '6000', '6199'], ['GT0', '6200', '6399'], ['GT1', '6400', '6599']]
#plot_type = 'no'

def plot_fublet_level(step_stepappend, xmlidv_chains, plot_type, osc, pdf, reportfile, limits, statistics):
    print("\n\n###############################################################################################")
    print("###############################################################################################")
    oscstrip=osc.lstrip("0")#Strips out any leading zeros from input OSC value
    print("Oscillator: " + str(oscstrip))

    reportfile.write("###############################################################################################")
    reportfile.write("\nOscillator: " + str(oscstrip))

    #print(str(step_stepappend[0].lco.location)+str(step_stepappend[0].name))
    output_file = [str(step.lco.location)+str(step.name) for step in step_stepappend]
    output_file_name = [str(step.name) for step in step_stepappend]
    #print(xmlidv_chains)

    lim_low = limits[0]
    lim_high = limits[1]

    ############################################################################################
    ## Data from files into memory
    ############################################################################################
    l = 0
    m = 0 # if zero means that the file does not contain that oscillator. We will use it to stop the plotting process.
    yarray = [] # later for finding y max and min if plotting all points, and to remove strange characters
    for file in output_file:
        ## Adding two new fields where I'll put the specific aries fublet numbers and the data. Each field will be an array
        for j in range(len(xmlidv_chains)):
            xmlidv_chains[j].append([])
            xmlidv_chains[j].append([])
        #print(xmlidv_chains)

        ## Data from CB being added in the two new fields.
        output_cb = open(file, 'r')
        i = 0
        for line in output_cb:
            if (not (i == 0 or line == "\n" or line == "")) and (line.split()[6] == str(oscstrip)):  ### added here  and (line.split()[6] == str(osc)) so we can take all data at once from CB, which should be way shorter, and filter here then
                m += 1
                ariesnum = int(line.split()[5])
                for j in range(len(xmlidv_chains)):
                    if int(xmlidv_chains[j][1]) <= ariesnum <= int(xmlidv_chains[j][2]):
                        #print("PRINT: "+ str(xmlidv_chains[j][1]) +";"+str(ariesnum)+";"+str(xmlidv_chains[j][2]))
                        xmlidv_chains[j][3 + 2*l].append(ariesnum)              ## l accounts for a different file.
                        if line.split()[7] == "0": ### To fill with -5 the values that are OVERFLOW and then are filtered later
                            xmlidv_chains[j][4 + 2*l].append(line.split()[8])
                        else:
                            xmlidv_chains[j][4 + 2*l].append("-5")
            i += 1
        output_cb.close()
        #print("M is: "+str(m))
        ##Puting the frequency data in an array and checking there are no errors(doesn't include characters).
        for yy in xmlidv_chains:
            for y in yy[4 + 2*l]:
                yarray.append(float(y))
                #print(y)
                if re.match( r".*[a-zA-Z].*", y, flags = 0):
                    print("something strange instead of a number: " + str(y))
        l += 1
    ############################################################################################

    if m == 0: ### If oscillator not present in files, do this, else continue
        print("None of your Lots/ituffs contains this oscillator. Skipping to next oscillator.")
        reportfile.write("\nNone of your Lots/ituffs contains this oscillator. Skipping to next oscillator.\n\n")

        #Special feature :D
        if osc == 'Piotr':
            special = "start \"\" \"https:\/\/www.youtube.com\/watch?v=z8ZvBSzNFsY\""
            call(special, shell=True)

        if osc == 'Dragon':
            special = "start \"\" \"https:\/\/www.youtube.com\/watch?v=Fn0F9rfV_jU\""
            call(special, shell=True)

        #Special feature 2 :D
        if osc == 'help' or osc == 'Help':
            special = "start \"\" \"https:\/\/securewiki.ith.intel.com\/display\/ClientIDV\/IDV+Data+Analysis+toolkit\""
            call(special, shell=True)

    else:
        ############################################################################################
        ## Max and min common for the plots with all points
        if plot_type == 'each point':
            ymax = max(yarray)
            ymin = min(yarray)
            print("Max value:\t" + str(ymax))
            print("Min value:\t" + str(ymin))

            #reportfile.write("\nMax value:\t" + str(ymax))
            #reportfile.write("\nMin value:\t" + str(ymin))
        ############################################################################################



        ############################################################################################
        ## Construction of the x and y for the plot. We have lots of points per each x.
        ############################################################################################
        ## Items that are common for several steps

        ##########################################
        ## Let's find the step with more fublets first, to decide which. And to add extra values if fublet number do not match.
        ## Add -9999 as freq value, and ignore it from the ymax and ymin limits.
        fublet_num = [0]*len(xmlidv_chains)
        num_dies_file = []
        chain_file_size_x = []
        x = [0]*len(xmlidv_chains)

        ############ Finding num of dies per file, and max num of fub per chain in all files
        for l in range(len(output_file)):
            #print("File number: "+str(l))
            #To find num dies per file, I need to make sure that I check with a chain that exists for that fublet. Count is so that corresponds to the chain has fublets.
            #print(len(xmlidv_chains))
            count = 0
            while len(set(xmlidv_chains[count][3 + 2*l]))==0:
                count += 1
            #print("count: "+str(count))

            num_dies_file.append(len(xmlidv_chains[count][4 + 2*l])//len(set(xmlidv_chains[count][3 + 2*l]))) ## number of dies i each "l" file
            ############# Finding the max num of fublets per chain in the different files:
            chain_file_size_x.append([])
            for chain in xmlidv_chains:
                chain_file_size_x[l].append(len(set(chain[3 + 2*l]))) ## number of fublets per chain in each "l" file
                #print(chain_file_size_x[l])
            fublet_num = list(np.maximum(fublet_num,chain_file_size_x[l]))
            #print(chain_file_size_x[l])
            #print(fublet_num)
        ############


        ############# Adjusting "y" values to max fublets per chain, creating "x" with max values, in order to be able to plot them together
        for l in range(len(output_file)):
            j = 0
            for chain in xmlidv_chains:
                #print(str(chain_file_size_x[l][j])+" - "+str(fublet_num[j]))
                if chain_file_size_x[l][j] < fublet_num[j]:
                    for i in range(num_dies_file[l]): #### need to insert the -999999 as if they were the next in the chain per each die.
                        for k in range(int(fublet_num[j]-chain_file_size_x[l][j])):
                            #print(chain_file_size_x[l][j]+k+i*fublet_num[j])
                            xmlidv_chains[j][4 + 2*l].insert(chain_file_size_x[l][j]+k+i*fublet_num[j], "-99999")
                    #print(xmlidv_chains[j][4 + 2*l])
                if chain_file_size_x[l][j] == fublet_num[j]:
                    #print(j)
                    x[j] = set(chain[3 + 2*l])
                    #print(x[j])
                j += 1


        ## To remove empty chains like IMGU, that have no values in any of the steps.
        xmlidv_2 = []
        #print(len(xmlidv_chains))
        for chain in xmlidv_chains:
            l = 0
            if len(output_file)>1:
                onetime = 0
                for l in range(len(output_file)):
                    if chain[3 + 2*l] != [] and onetime == 0:# or chain[3 + 2*l + 2] != []:
                        #print("full chain")
                        xmlidv_2.append(chain)#.remove(chain) # the remove doesn't work fine, but this way with a nex variable increases the memory consumption...
                        onetime = 1
                    l += 1
            else:
                if chain[3 + 2*l] != []:
                    #print("full chain")
                    xmlidv_2.append(chain)#.remove(chain)
        xmlidv_chains = xmlidv_2


        ### Removing empty items from x and from fublet_num
        x = [item for item in x if (item!=[])]
        x = [item for item in x if (item!=set())]
        fublet_num = [item for item in fublet_num if (item!=0)]
        ###########################################


        xlabel = [sorted(set(xset)) for xset in x] ### x per chain sorted. Only those that are different, not the whole of them.
        #print("xlabel: "+str(xlabel))



        title = []
        for chain in xmlidv_chains:
            title.append(chain[0]) ## create the titles for each chain


        percent = np.multiply(100,np.divide(fublet_num,fublet_num[0])) ###percentage respect the first figure



        newy = {}
        newy_a = {}
        newy_ac = {}
        die_num = {}
        ## Freq items (not common in different steps)
        for l in range(len(output_file)):
            #print("########################")
            print("\n" +str(step_stepappend[l].name) + ":")
            reportfile.write("\n"+str(step_stepappend[l].name) + ":")
            y = []
            for chain in xmlidv_chains:
                y_string_float = np.array(chain[4 + 2*l])
                y_float = y_string_float.astype(np.float)## ned to transform values to float otherwise each_point doesn't work
                y.append(y_float) #y.append(np.array(chain[4 + 2*l])) ## nparray per each set of freq corresponding to each chain
                
            leny = [len(yv) for yv in y] ### length of results per each chain
            #For debug:
            #print(y[7])

            #print("Length of Y and of X per chain:")
            #print(leny)
            #print(fublet_num)

            ###!!! with this I have all "y" here, it is a lot of memory. If needed, I could make average per wafers by getting more files, and then make a weigted average.
            ###!!! this is kind of defined above with: num_dies_file, try to unify
            die_num[str(l)] = np.divide(leny, fublet_num) ### length of results per chain divided per aries fublet in each chain: Gives the number of dies (repetitions) per chain (or per each fublet number).
            die_num[str(l)] = [int(value) for value in die_num[str(l)]] ### Transform them in integers

            ###!!! probably I can generate this without the need of defining y
            y = [y[i].reshape((die_num[str(l)][i],fublet_num[i])) for i in range(len(y))] ### Reshape y into a matrix,so we have all frequency data distributed per fublet aries number.
            newy[str(l)] = [np.transpose(y[i]) for i in range(len(y))] ### Transpose necessary in order to have the fublets well grouped, i.e., the 1000 in the same row/column, the 1005, etc per each aries fublet number
            #For debug
            #print(newy[str(l)][7])
            #print(newy[str(l)][0])
            #print(die_num[str(l)])


            ## AVERAGE per FUBLET
            ## Create new array that has index per chain, and index per aries fublet with one value for the average Frequency
            newy_a[str(l)] = []
            for k in range(len(xmlidv_chains)):
                newy_a[str(l)].append(np.zeros((fublet_num[k],1)))
            #print(np.array(newy_a).shape)

            total_num_fublets = 0
            overflow_values = 0
            zero_values = 0
            all_negative = 0
            out_of_limits = 0
            ## Calculation of the average per chain per fublet
            for k in range(len(xmlidv_chains)):
                for i in range(fublet_num[k]):
                    array_freq = []
                    zeros = 0.0
                    for value_freq in newy[str(l)][k][i,:]:
                        value_freq = float(value_freq)
                        if value_freq > 0: #### 0 or below not included
                            ## Adding extra filters for limits
                            if lim_low < value_freq < lim_high:
                                array_freq.append(value_freq)
                            else:
                                out_of_limits += 1
                            total_num_fublets += 1
                        else: ### the ones below zero:
                            if value_freq != -99999:
                                if value_freq == -5:
                                    overflow_values += 1
                                if value_freq == 0:
                                    zero_values += 1
                                all_negative += 1
                                total_num_fublets += 1
                                #print(all_negative)
                                #print("Zero (0), missing/zero (-999), or overflow (-5): " + str(value_freq))
                            zeros += 1.0
                    #print(np.sum(array_freq)/len(newy[k][i,:]))
                    #This was calculating the average. However, I could have done just divided by len(array_freq)
                    #newy_a[str(l)][k][i] = np.sum(array_freq)/(len(newy[str(l)][k][i,:])-zeros)
                    if plot_type == 'statistics':
                        if statistics == 'median':
                            newy_a[str(l)][k][i] = median(array_freq)
                        if statistics == 'mean':
                            newy_a[str(l)][k][i] = mean(array_freq)
                        if statistics == 'std':
                            newy_a[str(l)][k][i] = std(array_freq)
            #print(np.array(newy_a).shape)

            print("###################################################################")
            print("Total number of dies: \t\t\t\t\t" + str(die_num[str(l)][0])) 
            print("Total number of fubs: \t\t\t\t\t" + str(total_num_fublets))
            print("Number of fubs with zero values (0): \t\t\t" + str(zero_values))
            print("Number of fubs with overflow values (-5): \t\t" + str(overflow_values))
            print("Number of fubs with 0 or overflow: \t\t\t" + str(all_negative))
            print("Number of fubs out of filter limits values: \t\t" + str(out_of_limits))
            print("###################################################################\n")

            reportfile.write("\nTotal number of dies: \t\t\t\t\t" + str(die_num[str(l)][0]))
            reportfile.write("\nTotal number of fubs: \t\t\t\t\t" + str(total_num_fublets))
            reportfile.write("\nNumber of fubs with zero values (0): \t\t\t" + str(zero_values))
            reportfile.write("\nNumber of fubs with overflow values: \t\t\t" + str(overflow_values))
            reportfile.write("\nNumber of fubs with 0 or overflow: \t\t\t\t" + str(all_negative))
            reportfile.write("\nNumber of fubs out of filter limits values: \t\t" + str(out_of_limits) + "\n")

            ###################################################################

            ## AVERAGE PER CHAIN
            ## Create average per chain
            newy_ac[str(l)] = []
            for k in range(len(xmlidv_chains)):
                newy_ac[str(l)].append(np.zeros((fublet_num[k],1)))
            #print(np.array(newy_ac).shape)


            ## Calculation of the average/median/std per chain (but adding the same value per fublet to make the plot)
            for k in range(len(xmlidv_chains)):
                array_freq = []
                num_negative_added = 0.0  ### This is because if we compare 2 files with different num of fublets, we
                                        ### set extra values at -9999 and we do not want to include them into the average
                for i in range(fublet_num[k]):
                    for value_freq in newy[str(l)][k][i,:]:
                        value_freq = float(value_freq)### is this still needed???
                        if value_freq > 0:   ### 0 or below not included
                            ##Adding extra filtering as above
                            if lim_low < value_freq < lim_high:
                                array_freq.append(value_freq)
                        else:
                            num_negative_added += 1.0

                #old way average to be printed
                #print(title[k],":\t",np.sum(array_freq)/((len(newy[str(l)][k][:,0])*len(newy[str(l)][k][0,:])) - num_negative_added))
                #reportfile.write("\n" + str(title[k]) + ":\t" + str(np.sum(array_freq)/((len(newy[str(l)][k][:,0])*len(newy[str(l)][k][0,:])) - num_negative_added)))

                #new way average and adding same value per plot:
                if statistics == 'median':
                    median_val = median(array_freq)
                    print(title[k],":\t", median_val)
                    reportfile.write("\n %25s: %20.2f" % (title[k] , median_val))
                    for i in range(fublet_num[k]):
                        newy_ac[str(l)][k][i] = median_val
                if statistics == 'mean':
                    mean_val = mean(array_freq)
                    print(title[k],":\t", mean_val)
                    reportfile.write("\n %25s: %20.2f" % (title[k] , mean_val))
                    for i in range(fublet_num[k]):
                        newy_ac[str(l)][k][i] = mean_val
                if statistics == 'std':
                    sd_val = std(array_freq)
                    print(title[k],":\t", sd_val)
                    reportfile.write("\n %25s: %20.2f" % (title[k] , sd_val))
                    for i in range(fublet_num[k]):
                        newy_ac[str(l)][k][i] = sd_val



            #print(np.array(newy_ac).shape)
            ###################################################################
            ############################################################################################
            reportfile.write("\n")

        ## Max and min common for the plots with only averages/median/std
        if plot_type == 'statistics':
            all_average_array = []
            for l in range(len(output_file)):
                for k in range(len(xmlidv_chains)):
                    for i in range(fublet_num[k]):
                        all_average_array.append(newy_a[str(l)][k][i])
            all_average_array = [item for item in all_average_array if (item>0)] ## Remove -99999 in case we have added extra ficticious fublets to compare 2 steps.
            #
            # for item in all_average_array: ## Remove -99999 in case we have added extra ficticious fublets to compare 2 steps.
            #     if item < 0:
            #         print(item)
            #         all_average_array.remove(item)
            ymax = max(all_average_array)
            ymin = min(all_average_array)
            print("Max average value:\t" + str(ymax))
            print("Min average value:\t" + str(ymin))

            #reportfile.write("\nMax average value:\t" + str(ymax))
            #reportfile.write("\nMin average value:\t" + str(ymin))






        #######################################################################################################################
        ## THE FIGURE ###################
        #######################################################################################################################
        if plot_type != 'no plot': ## if no plot we do not make the plot and win time. basically when we want to check zeros and overflows in ituffs
            fig = plt.figure(num=None, figsize=(15, 5.3), dpi=20, facecolor='w', edgecolor='k')
            if plot_type == 'statistics':
                fig.suptitle(str(statistics)+' of oscillator: ' + str(osc), fontsize=12, fontweight='bold')
            if plot_type == 'each point':
                fig.suptitle('Oscillator: ' + str(osc), fontsize=12, fontweight='bold')
            ######################################################################
            ########## To make the axes look how they do:
            ax = {} #A dictionary, no need to use globals :)
            for i in range(len(xmlidv_chains)): ### For all chains
                if i==0:
                    ax[str(i)]  = plt.axes([0, 0, 1, 1])
                    divider = make_axes_locatable(ax[str(i)] )
                else:
                    ax[str(i)] = divider.new_horizontal(str(percent[i]) + "%", pad=0, sharey=ax[str(i-1)])
                    ax[str(i)].tick_params(labelleft=False)
                    fig.add_axes(ax[str(i)])


            divider.add_auto_adjustable_area(use_axes=[ax[str(0)] ], pad=0.15,
                                             adjust_dirs=["left"])
            divider.add_auto_adjustable_area(use_axes=[ax[str(len(xmlidv_chains)-1)] ], pad=0.15,
                                             adjust_dirs=["right"])
            divider.add_auto_adjustable_area(use_axes=[ax[str(0)], ax[str(len(xmlidv_chains)-1)]], pad=0.1,
                                             adjust_dirs=["top"])
            divider.add_auto_adjustable_area(use_axes=[ax[str(0)], ax[str(len(xmlidv_chains)-1)]], pad=0.75,
                                             adjust_dirs=["bottom"])

            ax[str(0)].set_ylabel('Frequency [MHz]')   ## To set the vertical title for Frequency
            #####################################################################

            ######################################################################
            ## To plot the real data, properly grouped in Aries fublet number and chain
            handle = [0]*len(output_file) #create empty vector to be used as handle for the legend
            for l in range(len(output_file)):
                for k in range(len(xmlidv_chains)):
                    if plot_type == 'statistics':
                        handle[l], = ax[str(k)].plot(newy_a[str(l)][k][:],'-,', label = output_file_name[l])
                        ax[str(k)].plot(newy_ac[str(l)][k][:],'r-', linewidth=0.5, label = 'the data')
                    if plot_type == 'each point':
                        for i in range(die_num[str(l)][k]):
                            ax[str(k)].plot(newy[str(l)][k][:,i],'.', label = output_file_name[l])
            ######################################################################

            ######################################################################
            ## To add labels and ticks and titles
            for i in range(len(xmlidv_chains)):
                ax[str(i)].set_title("\n\n_", size=8, color = "white") ## Set title at the top of each chain str(title[i])
                x_ticks = np.arange(0, fublet_num[i], 1)
                ax[str(i)].set_xticks(x_ticks)     ## Set the aries fublet number
                ax[str(i)].set_xlabel("" + str(title[i]), size=7.5, rotation=90)    ## to add the chain title for each
                ax[str(i)].set_ylim([ymin,ymax])    ## To set the same y scale for all
                ax[str(i)].set_xlim( -1, fublet_num[i] )  ## To leave space between y axis and data
                ax[str(i)].set_xticklabels(xlabel[i], rotation=90, size=4) ## Rotates the fublet aries number
                ax[str(i)].tick_params(direction = 'in', bottom = True, top = True, left = True, right = True) ## Needed for newer matplotlib to add axis up and down left and right and inner ticks
            #######################################################################

            ######################################################################
            ## To add the legend
            #plt.legend(handles=handle)
            if plot_type == 'statistics':
                plt.legend(handles=handle, bbox_to_anchor=(1, 1.07), ncol=len(output_file_name), loc='right', fontsize=9)
            ######################################################################

            pdf.savefig(fig)
            #pdf.close()
            plt.close()
            ######################################################################
            ## To show the plot
            #plt.show()
            #######################################################################################################################
            #######################################################################################################################


#plot_fublet_level(pdf_title, output_file, xmlidv_chains, plot_type)