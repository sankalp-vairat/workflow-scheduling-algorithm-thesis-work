'''
Created on 21-Feb-2017

@author: itadmin
'''
from power.Host import Host

class HostDynamicWorkload(Host):
    utilizationMips = 0
    previousUtilizationMips = 0
    
    def __init__(self,id,storage,peList):
        Host.__init__(self,id, storage, peList)
        self.utilizationMips = 0
        self.previousUtilizationMips = 0
        
    def getUtilizationMips(self):
        return self.utilizationMips;
    
    def getpreviousUtilizationMips(self):
        return self.previousUtilizationMips
    
    def setUtilizationMips(self,utilizationMips):
        self.utilizationMips = utilizationMips;
    
    def setpreviousUtilizationMips(self,previousUtilizationMips):
        self.previousUtilizationMips = previousUtilizationMips
       
    def getUtilizationOfCPU(self):
        utilization = float(self.getUtilizationMips())/float(self.getTotalMips())
        if (utilization > 1 and utilization < 1.01):
            utilization = 1;
        return utilization;