'''
Created on 11-Mar-2017

@author: itadmin
'''
from generator.randomgenerator import RandomGenerator.RandomGenerator

class DataCentre():
    
    def __init__(self,id,hostList,vmList):
        self.id = id
        self.hostList = hostList
        self.vmList = vmList
        
    def getId(self):
        return self.id
    
    def getHostList(self):
        return self.hostList
    
    def getVmList(self):
        return self.vmList
    
    def setId(self,id):
        self.id = id
    
    def setHostList(self,hostList):
        self.hostList = hostList
    
    def setVmList(self,vmList):
        self.vmList = vmList
        
    def createHostList(self,numberOfHosts,maxStorage):
        randomGenerator = RandomGenerator()
        self.setHostList(randomGenerator.randomHostGenerator(numberOfHosts,maxStorage))
        
    def createPeList(self,maxPesPerHost,maxMipsPerHost):
        randomGenerator = RandomGenerator()
        randomGenerator.randomPeListGenerator(self.hostList, maxMipsPerHost, maxPesPerHost)

        
    
        