from fublet_lib import *
from general_lib import *
from plot_fublet_level import *
from ituff_parse import ituff_all_osc
import os.path
from matplotlib.backends.backend_pdf import PdfPages

def IDV_fublet_comparison(loco, step, xml_title, pdf_title, plot_type, limits, statistics):
    ############################################################################################
    ## Inputs ##
    ############################################################################################
    #print("#####################################################################################\nInputs:")
    #loco = lco("C:\\Users\\RMENCHON\\Documents\\rmenchon\\Innovation\\fublet_data\\results\\", "950", ["4", "13"])#, "14", "15", "16", "19"])

    #This would be better using a dictionary, change it, although it works good how it is now too. Depends on GUI?
    #step0 = step("Dstep", ["H5521921 045"], "F24", loco)
    #step1 = step("Kstep", ["H601278A 765"], "F24", loco)
    #step2 = step("Jstep_KBL", ["L602883F 567"], "F32", loco)

    #xmlidv = xmlitem('IDV_FULL_950_KBL_J0.xml', loco.corner)

    #pdf_title = "example6"
    #each_point = 'no'

    ############################################################################################
    ############################################################################################
    ############################################################################################

    #step0.printdetails()
    #step1.printdetails()
    loco.printdetails()

    xmlidv = xmlitem(xml_title, loco.corner, loco.osc[0])
    print("XML chains: %s" % xmlidv.chains)
    print("XML low: %s" % xmlidv.lowrange)
    print("XML high: %s" % xmlidv.highrange)

    print("#####################################################################################")

    ############################################################################################
    ############################################################################################
    print(step.stepcount)
    print(step.stepappend)

    print("\#################################################################################")

    cb_iter = 0
    for i in range(0,step.stepcount): ### downloading data per "step" object
        step.stepappend[i].printdetails()
        #print("Aixo es: " + str(step.stepappend[i].lotwafer[0]))
        if os.path.isfile(step.stepappend[i].lotwafer[0]): ##In this way with the same gui I can use it for both ituff and crystal ball, or even mix them
            ### in case we added All for all oscillators
            if loco.osc == ['all'] or loco.osc == ['All']:
                loco.osc = ituff_all_osc(step.stepappend[i])#for ituff to get all osciillators
                for osci in loco.osc:
                    limits[str(osci)] = [0.0, 100000000.0]
            #We parse the ituff with All the oscillators
            step.stepappend[i].ituff()#for ituff
        else:
            if cb_iter == 0: ### we run this only once and if there is a LOT
                cblocation = cbilocator()
            cb_iter += 1
            step.stepappend[i].cbidv(cblocation,xmlidv)#for steps and crystal ball

    xmlidv = {}
    reportfilename = str(loco.location) + str(pdf_title) + '.txt'
    reportfile = open(reportfilename,'w')
    with PdfPages(str(loco.location) + str(pdf_title) + '.pdf') as pdf: ### to set up the multipage pdf
        for osc in loco.osc:
            print(osc)
            xmlidv[str(osc)] = xmlitem(xml_title,loco.corner,osc) ###otherwise seems too keep filling the xmlidv object, even if it is inside the function... is it because it is still the same object? That's possible... now I'm generating a different object and works.
            #print("XML chains: %s" % xmlidv[str(osc)].chains)
            #print("XML low: %s" % xmlidv[str(osc)].lowrange)
            #print("XML high: %s" % xmlidv[str(osc)].highrange)

            plot_fublet_level(step.stepappend, xmlidv[str(osc)].chains, plot_type, osc, pdf, reportfile, limits[str(osc)], statistics)
            del xmlidv[str(osc)]

    #### to remove all data files
    for step in step.stepappend:
        os.remove(str(step.lco.location)+str(step.name))
    if plot_type == 'no plot':
        os.remove(str(loco.location) + str(pdf_title) + '.pdf')
    reportfile.close()
#IDV_fublet_comparison()