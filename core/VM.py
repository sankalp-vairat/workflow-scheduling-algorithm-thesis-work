'''
Created on 11-Mar-2017

@author: itadmin
'''
class VM:

    def __init__(self,id ,globalVMId , host ,mips = 1, storage =1 , currentAllocatedMips = None , currentAllocatedStorage = None, currentAvailableMips = None , currentAvailableStorage = None):
        self.id = id
        self.mips = mips
        self.peList = list()
        self.storage= storage
        self.currentAllocatedMips = currentAllocatedMips
        self.currentAllocatedStorage = currentAllocatedStorage
        self.currentAvailableMips = currentAvailableMips
        self.currentAvailableStorage = currentAvailableStorage
        self.host =  host
        self.globalVMId = globalVMId
        self.tasksAllocated = list()
    
    def setTotalMips(self):
        mips = 0
        for pe in self.peList:
            mips = mips + pe.mips
        self.mips = mips
        self.currentAllocatedMips = 0
        self.currentAvailableMips = mips
        
    def setOldStorage(self):
        self.currentAllocatedStorage = 0
        self.currentAvailableStorage = self.storage
        
    def setNewMips(self,mips):
        self.currentAllocatedMips =  self.currentAllocatedMips - mips
        if(self.currentAllocatedMips < 0):
            self.currentAllocatedMips = 0
        
    def setNewStorage(self,storage):
        self.currentAllocatedStorage = self.currentAllocatedStorage - storage
        if(self.currentAllocatedStorage < 0):
            self.currentAllocatedStorage = 0 
        
    
    def getid(self):
        return self.id
    
    def addPeList(self,pe):
        self.peList.append(pe)
        
    def addTask(self,task):
        self.tasksAllocated.append(task)

    def getHost(self):
        return self.host
    
    def getMips(self):
        return self.mips
    
    def getNumberOfPes(self):
        return self.numberOfPes
    
    def getStorage(self):
        return self.storage
    
    def getCurrentAllocatedmips(self):
        return self.currentAllocatedMips
    
    def getcurrentAllocatedStorage(self):
        return self.currentAllocatedStorage
    
    def setid(self,id):
        self.id = id
    
    def setHost(self,host):
        self.host = host
    
    def setMips(self,mips):
        self.mips = mips 
    
    def setNumberOfPes(self,numberOfPes):
        self.numberOfPes = numberOfPes
    
    def setStorage(self,storage):
        self.storage = storage
    
    def setCurrentAllocatedmips(self,currentAllocatedMips):
        self.currentAllocatedMips = currentAllocatedMips
    
    def setcurrentAllocatedStorage(self,currentAllocatedStorage):
        self.currentAllocatedSize = currentAllocatedStorage