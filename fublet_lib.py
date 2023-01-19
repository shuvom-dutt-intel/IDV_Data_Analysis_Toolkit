from cbidvdata import *
from general_lib import *
from ituff_parse import *

class lco:
        def __init__(self,location,corner,osc):
            self.location = location
            self.corner = corner
            self.osc = osc

        def printdetails(self):
            print(self.location, self.corner, self.osc)


class step:
    stepcount = 0
    stepappend = []
    def __init__(self, name, lotwafer, site, ope, lco):
        self.name = name
        self.lotwafer = lotwafer
        self.site = site
        self.ope = ope
        self.lco = lco
        step.stepappend.append( self )
        step.stepcount += 1

    def printdetails(self):
         print(self.name, self.lotwafer, self.site)
         #self.lco.printdetails()

    def cbidv(self, cblocation, xmlidv):
        cbidvdata( self, cblocation, xmlidv )

    def ituff(self):
        ituff_data( self )