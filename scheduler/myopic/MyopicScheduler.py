'''
Created on 29-Mar-2017

@author: sankalp
'''
from scheduler.CloudletScheduler import CloudletScheduler
import time
from core.DataCentre import DataCentre
import copy 

class MyopicScheduler(CloudletScheduler):
    
    def execute(self,cloudlet,dataCentre):
        workflow = cloudlet.getWorkFlow()
        cloudlet.setExecStartTime(time.asctime())
        vmList = copy.deepcopy(dataCentre.getVMList())
        