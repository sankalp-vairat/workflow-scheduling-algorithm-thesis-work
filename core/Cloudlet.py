'''
Created on 11-Mar-2017

@author: itadmin
'''

class Cloudlet():
    
    def __init__(self,cloudletId,userId,numberOfPes,status,execStartTime,finishTime,resList):
        self.clouletId = cloudletId
        self.useId = userId
        self.numberOfPes = numberOfPes
        self.status = status
        self.execStartTime = execStartTime
        self.finishTime = finishTime
        self.resList = resList
        
    def getCloudletId(self):
        return self.clouletId
    
    def getUseId(self):
        return self.useId
    
    def getNumberOfPes(self):
        return self.numberOfPes
    
    def getStatus(self):
        return self.status
    
    def getExecStartTime(self):
        return self.execStartTime
    
    def getFinishTime(self):
        return self.finishTime
    
    def getResList(self):
        return self.resList

    def setCloudletId(self,cloudletId):
        self.clouletId = cloudletId
    
    def setUseId(self,userId):
        self.useId = userId
    
    def setNumberOfPes(self, numberOfPes):
        self.numberOfPes = numberOfPes
    
    def setStatus(self,status):
        self.status = status
    
    def setExecStartTime(self,execStartTime):
        self.execStartTime = execStartTime
    
    def setFinishTime(self,finishTime):
        self.finishTime = finishTime
    
    def setResList(self,resList):
        self.resList = resList
    
    
    