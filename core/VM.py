'''
Created on 11-Mar-2017

@author: itadmin
'''
def VM():
    
    def __init__(self,id , host ,mips, numberOfPes, storage, currentAllocatedMips, currentAllocatedSize):
        self.id = id
        self.mips = mips
        self.numberOfPes =numberOfPes
        self.storage= storage 
        self.currentAllocatedMips = currentAllocatedMips
        self.currentAllocatedSize = currentAllocatedSize
        self.host =  host
    
    def getid(self):
        return self.id
    
    def getHost(self):
        return self.host
    
    def getMips(self):
        return self.mips
    
    def getNumberOfPes(self):
        return self.numberOfPes
    
    def getStoarage(self):
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
    
    def setStoarage(self,storage):
        self.storage = storage
    
    def setCurrentAllocatedmips(self,currentAllocatedMips):
        self.currentAllocatedMips = currentAllocatedMips
    
    def setcurrentAllocatedSize(self,currentAllocatedSize):
        self.currentAllocatedSize = currentAllocatedSize   
    
   
    
    
    