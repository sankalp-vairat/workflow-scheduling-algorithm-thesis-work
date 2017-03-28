'''
Created on 16-Feb-2017

@author: itadmin
'''
from power.Pe import Pe

class Host:

    def __init__(self,id = 0 ,storage = 1,peList = None,VMList = None):
        self.id = id
        self.storage = storage
        self.peList = list()
        self.VMList = list()        
        #self.setpeList(peList)
        #self.setVMList(VMList)

    def setId(self,id):
        self.id = id
    
    def setStorage(self,storage):
        self.storage = storage
        
    def getId(self):
        return self.id
    
    def getStorage(self):
        return self.storage
    
    def  addPe(self,pe):
        self.peList.append(pe)
    def addVm(self,vm):
        self.VMList.append(vm)        
    def setpeList(self,peList):
        for i in range(len(peList)):
            self.peList.append(peList[i])
            
    def setVMList(self,VMList):
        for i in range(len(VMList)):
            self.VMList.append(VMList[i])
            
    def getVMList(self):
        return self.VMList

    def getpelist(self):
        return self.peList
    
    def getTotalMips(self):
        peList = self.getpelist()
        totalMips = 0;
        lenPeList =  len(peList)
        for i in range(lenPeList):
            totalMips += peList[i].getMips();
        return totalMips;
