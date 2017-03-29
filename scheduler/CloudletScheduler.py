'''
Created on 11-Mar-2017

@author: itadmin
'''
def CloudletScheduler():
    
    def __init__(self,scheduler):
        self.scheduler = scheduler

    def setScheduler(self,scheduler):
        self.scheduler = scheduler

    def getScheduler(self):
        return self.scheduler
    
    def executeScheduler(self,scheulder):
        self.scheduler.execute()
    
    def execute(self, workflow, dataCentre):
        pass
    
    def findRootTasks(self,DAG):
        pass