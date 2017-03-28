'''
Created on 11-Mar-2017

@author: itadmin
'''
from random import randint, random
from power.Host import Host
from core.VM import VM

class RandomGenerator():
    
    def randomHostGenerator(self,numberOfHosts,maxStorage,maxMipsPerPe,maxPesPerHost):
        
        if(numberOfHosts <= 0):
            raise ValueError("Number of hosts can't be less than or equal to 0..")
        
        if(maxStorage <= 0):
            raise ValueError("max storage of hosts can't be less than or equal to 0..")
        
        if(maxMipsPerPe <= 0 and maxMipsPerPe > 30):
            raise ValueError("max mips per host can't be less than or equal to 0 or grater than 50000",)
        
        if(maxPesPerHost <= 0 and maxPesPerHost > 100):
            raise ValueError("max pes per hosts can't be less than or equal to 0 or greater than 100")
                
        hostList = []

        for i in range(numberOfHosts):
            host = Host() 
            host.setId(i)
            host.setStorage(randint.uniform(1,maxStorage))
            host.setpeList(None)
            hostList.append(host)
        
        self.__randomPeListGenerator(hostList,maxMipsPerPe,maxPesPerHost)
            
        return hostList
    
    def __randomPeListGenerator(self,hostList,maxMipsPerPe,maxPesPerHost):
        
        numberOfHosts = len(hostList)
        for i in range(numberOfHosts):
            noOfPesPerHost = randint.uniform(1,maxPesPerHost)
            peList = []
            for j in range(noOfPesPerHost):
                mipsPerPe = 1000 * randint.uniform(1,maxMipsPerPe)
                peList.append(mipsPerPe)
            hostList[i].setpeList(self, peList)
            
    def __randomVMListGenerator(self,hostList):
        
        globalVMId = 0
        for host in hostList:
            noOfVMsPerHost = random.randint(1,len(host.getpelist()))
            VMList = []
            noOfPes = host.getpelist()
            i = 0;
            vmId = 0
            for pe  in host.getpelist():
                if(i < noOfVMsPerHost):
                    vmId = str(host.id)+':' + str(vmId)
                    vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                    vm.addPeList(pe)
                    VMList.append(vm)
                else:
                    vmIndex = random.randint(0,len(VMList))
                    VMList[vmIndex].addPeList(pe)  
                i = i + 1
                globalVMId = globalVMId +1
                
            
                 
    def randomWorkFlowGenerator(self):
        pass