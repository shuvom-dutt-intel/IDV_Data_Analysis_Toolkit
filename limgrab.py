import re
import xml.etree.ElementTree as ET
import pprint

def main():
    parsed_pgt = tokens_settings("C:/Users/Hcollins/OneDrive - Intel Corporation/projects/13p1_881_SIUP_SDT/5 - SUPERMV Limits/pgt.xml", "ALL_700MV", "")
    pprint.pp(parsed_pgt)
    names = []
    limits = []
    clamps = []
    for name, parameters in parsed_pgt.items():
        name = name[32:]
        names.append(name)
        limits.append(parameters["limit_high"])
        clamps.append(parameters["clamp_high"])
    print("Formatted names: ")
    print("{",end="")
    print(*('"{0}"'.format(name) for name in names), sep=", ", end="")
    print("}")
    print("Limits: ")
    print("{",end="")
    print(*('{0}'.format(limit) for limit in limits), sep=", ", end="")
    print("}")
    print("Clamps: ")
    print("{",end="")
    print(*('{0}'.format(clamp) for clamp in clamps), sep=", ", end="")
    print("}")

def limitgrabber(path, analysis_type):
    config_dict = {}

    if analysis_type == "VCC":
        config_dict = limitgrabberVCC(path)
    else:
         config_dict = limitgrabberSICC(path)
    return config_dict

def limitgrabberVCC(path):
    tokdict = {}
    searchflag = 0
               
    with open(path + 'Modules\TPI_VCC\TPI_VCC.mtpl', 'r') as f:
        for line in f:
            if "iCVccContinuityCPGTest" in line and "PARALLEL" not in line and "PRESURGE" not in line and not "_CHAR" in line and not "RECOVERY" in line:
                supply = re.match(r'Test iCVccContinuityCPGTest (\w+)', line) 
                tokdict['TPI_VCC::' + supply.group(1)] = {}
                searchflag = 1
                # for ts in tokens:
                #     if supply.group(1) in ts:
                #         searchflag = 1
                #         break
            if "limit_high" in line and searchflag:
                lm = re.match(r'\tlimit_high = "([-]?\w+[.]?\w+)";', line)
                tokdict['TPI_VCC::' + supply.group(1)]['limit_high'] = getnum(lm.group(1))
            elif  "limit_low" in line and searchflag:
                lm = re.match(r'\tlimit_low = "([-]?\w+[.]?\w+)";', line)
                tokdict['TPI_VCC::' + supply.group(1)]['limit_low'] = getnum(lm.group(1))
            elif  "clamp_high" in line and searchflag:
                lm = re.match(r'\tclamp_high = "([-]?\w+[.]?\w+)";', line)
                tokdict['TPI_VCC::' + supply.group(1)]['clamp_high'] = getnum(lm.group(1))
            elif  "clamp_low" in line and searchflag:
                lm = re.match(r'\tclamp_low = "([-]?\w+[.]?\w+)";', line)
                tokdict['TPI_VCC::' + supply.group(1)]['clamp_low'] = getnum(lm.group(1))
            elif  "pins" in line and searchflag:
                lm = re.match(r'\tpins = "(\w+_\w+)";', line)
                tokdict['TPI_VCC::' + supply.group(1) + "_" + lm.group(1)] = tokdict.pop('TPI_VCC::' + supply.group(1))
            elif "}" in line:
                searchflag = 0
    return tokdict
    
    
def limitgrabberSICC(path):
    tokens_settings_dict = {}
    searchflag = 0
   
    with open(path + 'Modules\TPI_SIU_STATIC\TPI_SIU_STATIC.mtpl', 'r') as df:
        for line in df:
            if "iCAnalogMeasureTest" in line:
                test_name = re.match(r'Test iCAnalogMeasureTest (\w+)', line) 
                test_name_var = test_name.group(1)
                searchflag = 1
            elif "config_file" in line and searchflag:
                lm = re.match(r'\tconfig_file = "(\.\/\w+\/\w+\/\w+\/\w+\.\w+)";', line)
                config_file_var = lm.group(1)
                searchflag += 1
            elif "config_set" in line and searchflag:
                lm = re.match(r'\tconfig_set = "(\w+)";', line)
                config_set_var = lm.group(1)
                searchflag += 1
            elif searchflag == 3:
                tokens_settings_dict.update(tokens_settings(path + config_file_var, config_set_var, test_name_var))
                searchflag = 0
            elif "}" in line:
                searchflag = 0  
    return tokens_settings_dict
    
    
def tokens_settings(config_path, config_set, test_name):
    tree = ET.parse(config_path)
    root = tree.getroot()
    
    config_dict = {}
    
    for configlist in root.findall('ConfigList'):
        if configlist.get('name') == config_set:
            for ituff_token in configlist.findall('./Config/Cores/Core/iTuff'):
                config_dict['TPI_SIU_STATIC::' + test_name + '_' + ituff_token.find('Token').text] = {}
                for measurement in configlist.findall('./Config/Measurements/Measurement'):                   
                    for pin in measurement.iter('Pin'):
                        if pin.text == ituff_token.find('./DataLookup/Equations/Pin').text:
                            config_dict['TPI_SIU_STATIC::' + test_name + '_' + ituff_token.find('Token').text]['limit_high'] = float(measurement.find('./MeasurementSettings/limit_high').text)
                            config_dict['TPI_SIU_STATIC::' + test_name + '_' + ituff_token.find('Token').text]['limit_low'] = float(measurement.find('./MeasurementSettings/limit_low').text)
                            config_dict['TPI_SIU_STATIC::' + test_name + '_' + ituff_token.find('Token').text]['clamp_high'] = float(measurement.find('./MeasurementSettings/clamp_high').text)
                            config_dict['TPI_SIU_STATIC::' + test_name + '_' + ituff_token.find('Token').text]['clamp_low'] = float(measurement.find('./MeasurementSettings/clamp_low').text)
    return config_dict
    
    
    
    
def getnum(numstr):
    if numstr.endswith("A"):
        numstr = numstr[:-1]
    if numstr.endswith("m"):
        num = float(numstr[:-1])/1000
    elif numstr.endswith("u"):
        num = float(numstr[:-1])/1000000
    return num
        
    
    
#if __name__ == "__main__":
#    mtplpathSICC = r"I:\program\1274\eng\hdmtprogs\adl_sds\tptorrent\ADLSDJCQ0H40A012104\Modules\TPI_SIU_STATIC\TPI_SIU_STATIC.mtpl"
#    xmlpath = r"I:\program\1274\eng\hdmtprogs\adl_sds\tptorrent\ADLSDJCQ0H40A012104\Modules\TPI_SIU_STATIC\InputFiles\pgt.xml"
#    dir = r"I:\program\1274\prod\hdmtprogs\adl_sds\ADLSDJCQ0H40B002104"
#    ld = limitgrabberSICC(dir)
#    print(ld)
#    mtplpathVCC = r"I:\program\1272\eng\hdmtprogs\rkl_sds\kevinrei\RKL81S_81J\RKL81S_81J_ph1a_rev02\Modules\TPI_VCC\TPI_VCC.mtpl"
#    xmlpath = 'dummypath'
#    tokensVCC = ['TPI_VCC::CONT_VCC0_VLC_K_START_X_CORE_X_X_VLC01_POSTSURGE_VCC0_VLC','TPI_VCC::CONT_VCC1_VLC_K_START_X_CORE_X_X_VLC02_POSTSURGE_VCC1_VLC','TPI_VCC::CONT_VCC2_VLC_K_START_X_CORE_X_X_VLC03_POSTSURGE_VCC2_VLC','TPI_VCC::CONT_VCC3_VLC_K_START_X_CORE_X_X_VLC04_POSTSURGE_VCC3_VLC','TPI_VCC::CONT_VCC4_VLC_K_START_X_CORE_X_X_VLC05_POSTSURGE_VCC4_VLC','TPI_VCC::CONT_VCC5_VLC_K_START_X_CORE_X_X_VLC06_POSTSURGE_VCC5_VLC','TPI_VCC::CONT_VCC6_VLC_K_START_X_CORE_X_X_VLC07_POSTSURGE_VCC6_VLC','TPI_VCC::CONT_VCC7_VLC_K_START_X_CORE_X_X_VLC08_POSTSURGE_VCC7_VLC','TPI_VCC::CONT_VCCDDQTX_HC_K_START_X_IO_X_X_HC03_POSTSURGE_VCCDDQTX_HC','TPI_VCC::CONT_VCCDDQ_LC_K_START_X_DDR_X_X_LC01_POSTSURGE_VCCDDQ_LC','TPI_VCC::CONT_VCCFPGM0_LC_K_START_X_X_X_X_LC02_POSTSURGE_VCCFPGM0_LC','TPI_VCC::CONT_VCCFPGM1_LC_K_START_X_X_X_X_LC03_POSTSURGE_VCCFPGM1_LC','TPI_VCC::CONT_VCCFPGM2_LC_K_START_X_X_X_X_LC04_POSTSURGE_VCCFPGM2_LC','TPI_VCC::CONT_VCCGT_HC_K_START_X_GT_X_X_HC04_POSTSURGE_VCCGT_HC','TPI_VCC::CONT_VCCHSDISP_LC_K_START_X_IO_X_X_LC07_POSTSURGE_VCCHS_DISP_LC','TPI_VCC::CONT_VCCHSDMI_LC_K_START_X_IO_X_X_LC06_POSTSURGE_VCCHS_DMI_LC','TPI_VCC::CONT_VCCHS_HC_K_START_X_IO_X_X_HC05_POSTSURGE_VCCHS_HC','TPI_VCC::CONT_VCCIO_HC_K_START_X_IO_X_X_HC06_POSTSURGE_VCCIO_HC','TPI_VCC::CONT_VCCR_HC_K_START_X_CORE_X_X_HC01_POSTSURGE_VCCR_HC','TPI_VCC::CONT_VCCSAGMEM12DG_HC_K_START_X_X_X_X_HC05_POSTSURGE_VCCSAGMEM12DG_HC','TPI_VCC::CONT_VCCSA_HC_K_START_X_SA_X_X_HC02_POSTSURGE_VCCSA_HC','TPI_VCC::CONT_VCCSFR_LC_K_START_X_X_X_X_LC05_POSTSURGE_VCCSFR_OC_LC','TPI_VCC::CONT_VCCSTGCENTRAL_LC_K_START_X_IO_X_X_LC10_POSTSURGE_VCCSTG_CENTRAL_LC','TPI_VCC::CONT_VCCSTGFABRIC_LC_K_START_X_IO_X_X_LC11_POSTSURGE_VCCSTG_FABRIC_LC','TPI_VCC::CONT_VCCSTGLGCIO_LC_K_START_X_IO_X_X_LC09_POSTSURGE_VCCSTG_LGCIO_LC','TPI_VCC::CONT_VCCSTG_LC_K_START_X_IO_X_X_LC07_POSTSURGE_VCCSTG_LC','TPI_VCC::CONT_VCCST_HC_K_START_X_ST_X_X_LC07_POSTSURGE_VCCST_HC']
#    ld = limitgrabber(mtplpathVCC, tokensVCC)
#    print(ld)
if __name__ == "__main__":
    main()
