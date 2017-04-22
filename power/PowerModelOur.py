'''
Created on 22-Apr-2017

@author: itadmin
'''

from power.PowerModel import PowerModel
import math

class PowerModelOur(PowerModel):

    maxPower = 0.0
    constant = 0.0
    staticPower = 0.0

    def __init__(self,maxPower = 250,staticPowerPercent= 50):
        self.maxPower=maxPower
        self.setStaticPower(staticPowerPercent*maxPower)
        self.setConstant(self.maxPower - self.getStaticPower() / 100)
        
        
    def getEnergy(self,utilizationMips,totalMips,time):
        return self.getPower(self,utilizationMips/totalMips) * time
        
    def getPower(self,utilization,time):
        if(utilization < 0 and utilization >1 ):
            try:
                raise Exception()
            except Exception:
                print "Utilization value must be between 0 and 1"
        if(utilization == 0):
            return 0
        
        power = ((1 - (utilization))*self.staticPower + (utilization) * self.maxPower )

    def setStaticPower(self,staticPower):
        self.staticPower = staticPower

    def setmaxPower(self,maxPower):
        self.maxPower = maxPower

    def setConstant(self,constant):
        self.constant = constant

    def getStaticPower(self):
        return self.staticPower

    def getmaxPower(self):
        return self.maxPower

    def getConstant(self):    
        return self.constant