'''
Created on 15-Mar-2017

@author: itadmin
'''
from generator.RandomGenerator import RandomGenerator

class RandomWorkFlowGenerator(RandomGenerator):
    
    def __init__(self,noOfTasks, noOfLevels, runTimeLowerBound, runTimeUpperBound, storageLowerbound, storageUpperBound, miLowerBound, miUpperBound):
        self.noOfTasks = noOfTasks
        self.noOfLevels = noOfLevels
        self.runTimeLowerBound = runTimeLowerBound
        self.runTimeUpperBound = runTimeUpperBound
        self.storageLowerbound = storageLowerbound
        self.storageUpperBound = storageUpperBound
        self.miLowerBound = miLowerBound
        self.miUpperBound = miUpperBound
        
    def getNoOfTasks(self):
        return self.noOfTasks
    
    def getNoOfLevels(self):
        return self.noOfLevels
    
    def getRunTimeLowerBound(self):
        return self.runTimeLowerBound
    
    def getRunTimeUpperBound(self):
        return self.getRunTimeUpperBound()
    
    def getStorageLowerBound(self):
        return self.storageLowerbound
    
    def getStorageUpperBound(self):
        return self.storageUpperbound
        
    def getMiLowerBound(self):
        return self.miLowerBound
    
    def getMiUpperBound(self):
        return self.miUpperBound

    def setNoOfTasks(self,noOfTasks):
        self.noOfTasks = noOfTasks
    
    def setNoOfLevels(self,noOfLevels):
        self.noOfLevels = noOfLevels
    
    def setRunTimeLowerBound(self,runTimeLowerBound):
        self.runTimeLowerBound = runTimeLowerBound
    
    def setRunTimeUpperBound(self,runTimeUpperBound):
        self.runTimeUpperBound = runTimeUpperBound
    
    def setStorageLowerBound(self,storageLowerbound):
        self.storageLowerbound = storageLowerbound
    
    def setStorageUpperBound(self,storageUpperbound):
        self.storageUpperbound = storageUpperbound
        
    def setMiLowerBound(self,miLowerBound):
        self.miLowerBound = miLowerBound
    
    def setMiUpperBound(self,miUpperBound):
        self.miUpperBound = miUpperBound
    
    def randomWorkFlowGenerator(self):
        noOfTasks = self.getNoOfTasks()
        noOfLevels = self.getNoOfLevels()
        runTimeLowerBound = self.getRunTimeLowerBound()
        runTimeUpperBound = self.getRunTimeUpperBound()
        storageLowerBound = self.getStorageLowerBound()
        storageUpperBound = self.getStorageUpperBound()
        miLowerBound = self.getMiLowerBound()
        miUpperbound = self.getMiUpperBound()
        
        
        