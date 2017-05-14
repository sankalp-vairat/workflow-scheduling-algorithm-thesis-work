'''
Created on 11-Mar-2017

@author: itadmin
'''

from generator.randomgenerator.RandomGenerator import RandomGenerator

class DataCentre:

    def __init__(self,id):
        self.id = id
        self.hostList = list()
        self.vmList = list()

    def getId(self):
        return self.id

    def getHostList(self):
        return self.hostList

    def getVMList(self):
        return self.vmList

    def setId(self,id):
        self.id = id

    def __setHostList(self,hostList):
        for host in hostList:
            self.hostList.append(host)

    def __setVmList(self,hostList):
        for host in hostList:
            for vm in host.VMList:
                self.vmList.append(vm)

    def setUpDatacentre(self,numberOfHosts,maxStorage,maxMipsPerPe,maxPesPerHost,powerModel):
        randomGenerator = RandomGenerator()
        self.__setHostList(randomGenerator.randomHostGenerator(numberOfHosts,maxStorage,maxMipsPerPe,maxPesPerHost,powerModel))
        self.__setVmList(self.getHostList())


    def setUpDefinedDatacentre(self,numberOfHosts,maxStorage,maxMipsPerPe,maxPesPerHost,powerModel):
        randomGenerator = RandomGenerator()
        self.__setHostList(randomGenerator.randomHostGenerator(numberOfHosts,maxStorage,maxMipsPerPe,maxPesPerHost,powerModel))
        self.__setVmList(self.getHostList())