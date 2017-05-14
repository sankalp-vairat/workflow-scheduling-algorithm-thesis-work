'''
Created on 11-Mar-2017

@author: itadmin
'''
from random import randint, random
from power.Host import Host
from power.PowerHost import PowerHost
from power.Pe import Pe
from core.VM import VM
from power.PowerModelSpecPowerAppleIncXserve31 import PowerModelSpecPowerAppleIncXserve31
from power.PowerModelSpecPowerAcerAR380F1 import PowerModelSpecPowerAcerAR380F1
from power.PowerModelSpecPowerIBMSystemx3650M3 import PowerModelSpecPowerIBMSystemx3650M3
from power.PowerModelSpecPowerAcerIncorporatedAltosR380F2 import PowerModelSpecPowerAcerIncorporatedAltosR380F2
from power.PowerModelSpecPowerAcerIncorporatedGatewayGT350F1 import PowerModelSpecPowerAcerIncorporatedGatewayGT350F1
from power.PowerModelSpecPowerDellIncPowerEdgeR720 import PowerModelSpecPowerDellIncPowerEdgeR720
from power.PowerModelSpecPowerHuaweiTechnologiesCoLtdRH2288HV2 import PowerModelSpecPowerHuaweiTechnologiesCoLtdRH2288HV2
from power.PowerModelSpecPowerFujitsuServerPRIMERGYTX2560M1 import PowerModelSpecPowerFujitsuServerPRIMERGYTX2560M1
from power.PowerModelSpecPowerDellIncPowerEdgeT630 import PowerModelSpecPowerDellIncPowerEdgeT630
from power.PowerModelSpecPowerHPProLiantDL160G5  import PowerModelSpecPowerHPProLiantDL160G5

class DefinedGenerator():
    
    def definedHostGenerator(self,numberOfHosts = 1000,maxStorage,maxMipsPerPe,maxPesPerHost,powerModel):
        
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
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerAppleIncXserve31)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerAcerAR380F1)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerIBMSystemx3650M3)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerAcerIncorporatedAltosR380F2)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerAcerIncorporatedGatewayGT350F1)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerDellIncPowerEdgeR720)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerHuaweiTechnologiesCoLtdRH2288HV2)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerFujitsuServerPRIMERGYTX2560M1)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerDellIncPowerEdgeT630)
            
        for i in range(numberOfHosts):
            host = PowerHost(id =  i,powerModel = PowerModelSpecPowerHPProLiantDL160G5) 
            
            #host.setId(i)
            #make the GB to KB
            host.setStorage(randint(1,maxStorage*1024))
            #host.setpeList(None)
            #host.setVMList(None)
            hostList.append(host)
        
        self.__randomPeListGenerator(hostList,maxMipsPerPe,maxPesPerHost)
        self.__randomVMListGenerator(hostList)
            
        return hostList
    
    def __definedPeListGenerator(self,hostList,maxMipsPerPe,maxPesPerHost):
        
        numberOfHosts = len(hostList)
        for i in range(numberOfHosts):
            noOfPesPerHost = randint(1,maxPesPerHost)
            #peList = []
            for j in range(noOfPesPerHost):
                mipsPerPe = 1000 * randint(1,maxMipsPerPe)
                hostList[i].addPe(Pe(mipsPerPe))
                #peList.append()
            #hostList[i].setpeList(self, peList)
            
    def __definedVMListGenerator(self,hostList):
        
        globalVMId = 0
        for host in hostList:
            noOfVMsPerHost = randint(1,len(host.getpelist()))
            VMList = []
            noOfPes = host.getpelist()
            i = 0;
            vmId = 0
            vmNo = 0
            for pe  in host.getpelist():
                if(i < noOfVMsPerHost):
                    vmId = str(host.id)+':' + str(vmNo)
                    vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                    vm.addPeList(pe)
                    #host.addVm(vm)
                    VMList.append(vm)
                    globalVMId = globalVMId +1
                    vmNo = vmNo + 1
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
