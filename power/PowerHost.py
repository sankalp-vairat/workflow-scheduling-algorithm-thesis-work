'''
Created on 16-Feb-2017

@author: itadmin
'''
from power.HostDynamicWorkload import HostDynamicWorkload
from power.PowerModel import PowerModel
import sys
from power.PowerModelLinear import PowerModelLinear

class PowerHost(HostDynamicWorkload):
    powerModel = PowerModel()
    def __init__(self,id,storage=0,peList=None,powerModel = PowerModelLinear()):
        HostDynamicWorkload.__init__(self,id, storage, peList)
        self.powerModel = powerModel
    
    def getPowerModel(self):
        return self.powerModel
    
    def setPowerModel(self,powerModel):
        self.powerModel = powerModel
        
    def getEnergy(self,utilizationMips,totalUtilizationMips,currentCompletionTime):
        return self.powerModel.getEnergy(utilizationMips,totalUtilizationMips,currentCompletionTime)
    
    def getPower(self):
        return self.getPowerUtility(self.getUtilizationOfCPU())

    def getEnergyDefinedHost(self,utilizationMips,totalUtilizationMips,currentCompletionTime):
        return self.getPowerUtility(utilizationMips/totalUtilizationMips)
        
        
    def getPowerUtility(self,utilization):
        power = 0
        #power = self.getPowerModel().getPowerData(utilization)
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
    
        
    