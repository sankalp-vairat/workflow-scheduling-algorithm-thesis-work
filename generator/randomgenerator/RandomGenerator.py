'''
Created on 11-Mar-2017

@author: itadmin
'''
from random import randint, random
from power.Host import Host
from power.PowerHost import PowerHost
from power.Pe import Pe
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
            host = PowerHost(id =  i ) 
            #host.setId(i)
            host.setStorage(randint(1,maxStorage))
            #host.setpeList(None)
            #host.setVMList(None)
            hostList.append(host)
        
        self.__randomPeListGenerator(hostList,maxMipsPerPe,maxPesPerHost)
        self.__randomVMListGenerator(hostList)
            
        return hostList
    
    def __randomPeListGenerator(self,hostList,maxMipsPerPe,maxPesPerHost):
        
        numberOfHosts = len(hostList)
        for i in range(numberOfHosts):
            noOfPesPerHost = randint(1,maxPesPerHost)
            #peList = []
            for j in range(noOfPesPerHost):
                mipsPerPe = 1000 * randint(1,maxMipsPerPe)
                hostList[i].addPe(Pe(mipsPerPe))
                #peList.append()
            #hostList[i].setpeList(self, peList)
            
    def __randomVMListGenerator(self,hostList):
        
        globalVMId = 0
        for host in hostList:
            noOfVMsPerHost = randint(1,len(host.getpelist()))
            VMList = []
            noOfPes = host.getpelist()
            i = 0;
            vmId = 0
            for pe  in host.getpelist():
                if(i < noOfVMsPerHost):
                    vmId = str(host.id)+':' + str(vmId)
                    vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                    vm.addPeList(pe)
                    #host.addVm(vm)
                    VMList.append(vm)
                    globalVMId = globalVMId +1
                else:
                    vmIndex = randint(0,len(VMList)-1)
                    VMList[vmIndex].addPeList(pe)  
                i = i + 1

            size = host.storage
            for  vm in VMList:
                  vm.storage = int(size / noOfVMsPerHost)
            for j in range(size % noOfVMsPerHost):
                VMList[j].storage += 1
            
            host.setVMList(VMList)
            
                 
    def randomWorkFlowGenerator(self):
        pass