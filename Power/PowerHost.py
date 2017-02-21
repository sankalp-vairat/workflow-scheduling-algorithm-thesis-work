'''
Created on 16-Feb-2017

@author: itadmin
'''
from Power.HostDynamicWorkload import HostDynamicWorkload
from Power.PowerModel import PowerModel
import sys

class PowerHost(HostDynamicWorkload):
    powerModel = PowerModel()
    def __init__(self,id1,storage,peList,powerModel):
        HostDynamicWorkload.__init__(self,id1, storage, peList)
        self.powerModel = powerModel
    
    def getPowerModel(self):
        return self.powerModel
    
    def setPowerModel(self,powerModel):
        self.powerModel = powerModel
    
    def getPower(self):
        return self.getPowerUtility(self.getUtilizationOfCPU())
        
        
    def getPowerUtility(self,utilization):
        power = 0

        try:
            power = self.getPowerModel().getPower(utilization)

        except Exception:
            print "Exception in get power utility"
            sys.exit(1)
        return power
    
    def getmaxPower(self):
        power = 0
        power = self.getPowerModel().getPower(1)
        return power
    
        
    