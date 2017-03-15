'''
Created on 11-Mar-2017

@author: itadmin
'''
from random import randint, random
from power.Host import Host

class RandomGenerator():
    
    def randomHostGenerator(self,numberOfHosts,maxStorage,maxMipsPerHost,maxPesPerHost):
        hostList = []

        for i in range(numberOfHosts):
            host = Host() 
            host.setId(i)
            host.setStorage(randint.uniform(1,maxStorage))
            host.setpeList(None)
            hostList.append(host)
        
        self.__randomPeListGenerator(hostList,maxMipsPerHost,maxPesPerHost)
            
        return hostList
    
    def __randomPeListGenerator(self,hostList,maxMipsPerHost,maxPesPerHost):
        numberOfHosts = len(hostList)
        for i in range(numberOfHosts):
            noOfPesPerHost = randint.uniform(1,maxPesPerHost)
            peList = []
            for j in range(noOfPesPerHost):
                mipsPerHost = randint.uniform(1,maxMipsPerHost)
                peList.append(mipsPerHost)
            hostList[i].setpeList(self, peList)
            
            
    def randomWorkFlowGenerator(self):
        pass