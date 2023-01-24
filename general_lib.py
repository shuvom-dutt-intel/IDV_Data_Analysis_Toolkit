import re
import subprocess
import os.path

def linereturn(file,match):
        fileopen = open(file,'r')
        linearray = []
        for line in fileopen:
            #print(line)
            if re.match(".*%s.*" % match, line):
                linearray.append(line)
        fileopen.close()
        return(linearray)

def cbilocator():
    un = os.getlogin()# calls username from user
    path="C:\\Users\\%s\\CrystalBall\\Production\\Cry"%un #adds usernameto user crystalball location
    exists=os.path.exists(path)#check if path exists
    if  exists== True:
        print(exists)
        cbloc ="C:\\Users\\%s\\CrystalBall\\Production\\CBCLI.exe"%un
        print ("CB location: ", cbloc)
    else:#If the path doenst exist pulls the .bat script to find where the exe lives 
        subprocess.call("cbcli_locator.bat", shell=True)
        cbloc = linereturn('cbcli_loc.txt','Production')[0]
        print("CB location: ", cbloc)
        print(cbloc)
    return (cbloc)
    


class xmlitem:
    def __init__(self,xml,corner,osc):
        ch = []
        low = []
        high = []
        fileopen = open(xml,'r')
        counter = 0
        for xmline in fileopen:

            if re.match(r".*<Chain_group type=\"(.*)\".*", xmline, flags = 0):
                matcheschain = re.match(r".*<Chain_group type=\"(.*)\".*", xmline, flags = 0)
            if re.match(r".*<Fub.*name=.*", xmline, flags = 0):#re.match(r".*<Fub name=.*", xmline, flags = 0):
                if counter == 0:
                    matchesrange_low = re.match(r".*<Fub.*name=\"(.*?)\".*", xmline, flags = 0)#matchesrange_low = re.match(r".*<Fub name=\"(.*)\".*Type.*", xmline, flags = 0)
                    counter += 1
                else:
                    matchesrange_high = re.match(r".*<Fub.*name=\"(.*?)\".*", xmline, flags = 0)#matchesrange_high = re.match(r".*<Fub name=\"(.*)\".*Type.*", xmline, flags = 0)

            if re.match(r".*</Chain_group>.*", xmline, flags = 0):
                counter = 0
                ch.append([matcheschain.group(1),matchesrange_low.group(1),matchesrange_high.group(1)])
                low.append(matchesrange_low.group(1))
                high.append(matchesrange_high.group(1))
                    
        fileopen.close()
        self.chains = ch
        self.lowrange = low
        self.highrange = high