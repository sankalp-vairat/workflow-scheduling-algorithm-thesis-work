'''
Created on 11-Mar-2017

@author: itadmin
'''
import copy
class Cloudlet():
    
    def __init__(self,cloudletId,userId,status,execStartTime,workFlow):
        self.clouletId = cloudletId
        self.useId = userId
        self.status = status
        self.execStartTime = execStartTime
        self.finishTime = 0
        self.workFlow = copy.deepcopy(workFlow)
        self.energyConsumption = 0
        self.SLAViolationList = list() 

    def addSLAViolationList(self,SLAViolation):
        self.SLAViolationList.append(SLAViolation)

    def getCloudletId(self):
        return self.clouletId
    
    def getUseId(self):
        return self.useId
    
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
    
    def setStatus(self,status):
        self.status = status
    
    def setExecStartTime(self,execStartTime):
        self.execStartTime = execStartTime
    
    def setFinishTime(self,finishTime):
        self.finishTime = finishTime
    
    def setResList(self,resList):
        self.resList = resList

    def getWorkFlow(self):
        return self.workFlow