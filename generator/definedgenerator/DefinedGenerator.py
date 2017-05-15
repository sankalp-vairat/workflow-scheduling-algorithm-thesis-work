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


    def DefinedHostGenerator(self,numberOfHosts,maxStorage):

        hostList = []        
        hostid = 0
        globalVMId = 0

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerAppleIncXserve31())

            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(8):
                host.addPe(Pe(15000))

            vmNo = 0
            VMList = []

            for k in range(6):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 6)

            for j in range(size % 6):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)

#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerAcerAR380F1())

            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(12):
                host.addPe(Pe(15000))

            vmNo = 0
            VMList = []

            for k in range(10):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 10)

            for j in range(size % 10):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)

#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerIBMSystemx3650M3())

            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(12):
                host.addPe(Pe(15000))

            vmNo = 0
            VMList = []

            for k in range(10):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 10)

            for j in range(size % 10):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)

#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerAcerIncorporatedAltosR380F2())
            
            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))
            
            for j in range(16):
                host.addPe(Pe(10000))

            vmNo = 0
            VMList = []

            for k in range(14):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 14)

            for j in range(size % 14):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)


#---------------------------------------------------------------------------------------------


        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerAcerIncorporatedGatewayGT350F1())
            
            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))
            
            for j in range(12):
                host.addPe(Pe(15000))
                
            vmNo = 0
            VMList = []

            for k in range(10):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 10)

            for j in range(size % 10):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)

#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerDellIncPowerEdgeR720())

            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(16):
                host.addPe(Pe(10000))
                
            vmNo = 0
            VMList = []

            for k in range(14):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 14)

            for j in range(size % 14):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)

#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerHuaweiTechnologiesCoLtdRH2288HV2())
            
            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(8):
                host.addPe(Pe(12000))
            vmNo = 0
            VMList = []

            for k in range(6):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 6)

            for j in range(size % 6):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)

#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerFujitsuServerPRIMERGYTX2560M1())

            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(36):
                host.addPe(Pe(11500))

            vmNo = 0
            VMList = []

            for k in range(34):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 34)

            for j in range(size % 34):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)

#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerDellIncPowerEdgeT630())
            
            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(18):
                host.addPe(Pe(11500))

            vmNo = 0
            VMList = []

            for k in range(16):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 16)

            for j in range(size % 16):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)
            
#---------------------------------------------------------------------------------------------

        for i in range(numberOfHosts):
            host = PowerHost(id =  hostid,powerModel = PowerModelSpecPowerHPProLiantDL160G5())
            
            hostid = hostid + 1

            host.setStorage(randint(1,maxStorage*1024))

            for j in range(8):
                host.addPe(Pe(12500))

            vmNo = 0
            VMList = []

            for k in range(6):
                vmId = str(host.id)+':' + str(vmNo)
                vmNo = vmNo + 1
                vm = VM(id = vmId,host = host,globalVMId = globalVMId)
                globalVMId = globalVMId + 1
                vm.addPeList(host.getpelist()[k])
                VMList.append(vm)

            size = host.storage
            for  vm in VMList:
                vm.storage = int(size / 6)

            for j in range(size % 6):
                VMList[j].storage += 1

            host.setVMList(VMList)
            
            hostList.append(host)
            
        return hostList