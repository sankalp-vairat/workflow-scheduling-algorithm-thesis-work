 '''
Created on 11-Mar-2017

@author: itadmin
'''
def VM():

    def __init__(self,id,globalId , host ,mips, storage, currentAllocatedMips, currentAllocatedSize):
        self.id = id
        self.mips = mips
        self.peList = list()
        self.storage= storage
        self.currentAllocatedMips = currentAllocatedMips
        self.currentAllocatedSize = currentAllocatedSize
        self.host =  host
        self.globalId = globalId
    
    def setTotalMips(self):
        mips = 0
        for pe in self.peList:
            mips = mips + pe.mips
        self.mips = mips
        self.currentAllocatedMips = mips
        
    def setOldStorage(self):
        self.cuurentAllocatedSize = self.storage
        
    def setNewMips(self,mips):
        self.currentAllocatedMips =  self.currentAllocatedMips - mips
        if(self.currentAllocatedMips < 0):
            self.currentAllocatedMips = 0
        
    def setNewStorage(self,storage):
        self.currentAllocatedSize = self.currentAllocatedSize - storage
        if(self.currentAllocatedSize < 0):
            self.currentAllocatedSize = 0 
        
    
    def getid(self):
        return self.id
    
    def addPeList(self,pe):
        self.peList(pe)
    
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
    
    def getcurrentAllocatedSize(self):
        return self.currentAllocatedSize
    
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
    
    def setcurrentAllocatedSize(self,currentAllocatedSize):
        self.currentAllocatedSize = currentAllocatedSize   
    
   
    
    
    