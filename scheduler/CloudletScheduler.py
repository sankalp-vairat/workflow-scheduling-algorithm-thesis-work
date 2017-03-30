'''
Created on 11-Mar-2017

@author: itadmin
'''
class CloudletScheduler():
    
    def __init__(self,scheduler):
        self.scheduler = scheduler

    def setScheduler(self,scheduler):
        self.scheduler = scheduler

    def getScheduler(self):
        return self.scheduler
    
    def executeScheduler(self,cloudlet,dataCentre):
        self.scheduler.execute(cloudlet,dataCentre)
    
    def execute(self, workflow, dataCentre):
        pass
    
    def findRootTasks(self,DAG):
        pass