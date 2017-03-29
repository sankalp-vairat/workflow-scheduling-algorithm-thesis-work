'''
Created on 29-Mar-2017

@author: sankalp
'''

from scheduler.CloudletScheduler import CloudletScheduler
import time
from core.DataCentre import DataCentre
import copy 
from multiprocessing import Queue
from threading import Thread
from scheduler.Allocation import Allocation

global global_queue
global_queue = Queue()

global myopicList
myopicList = []


class MyopicScheduler(CloudletScheduler):

    def __init__(self):
        cloudlet = None
        workflow = None
        vmList = None
        DAG = None
        dependencyMatrix = None

    def execute(self,cloudlet,dataCentre):
        self.cloudlet = cloudlet
        self.workflow = self.cloudlet.getWorkFlow()
        cloudlet.setExecStartTime(time.asctime())
        self.vmList = copy.deepcopy(dataCentre.getVMList())
        self.DAG = self.workflow.DAG_matrix
        self.dependencyMatrix = self.DAG.dependencyMatrix
        
        rootTasksIndexes = self.cloudletScheduler.findRootTasks(self.DAG)
        
        starting_thread = Thread(target=self.__myopicSchedulerUtil(), args=())
        #starting_thread.daemon = True
        starting_thread.start()
        
        
        for rootTaskIndex in rootTasksIndexes:
            self.__synchronizedQueue(2,rootTaskIndex)

    def __synchronizedQueue(self,choice,pos):
        '''
        Function:    This function synchronizes 1) the reading the values from global_q and then applying ACO and 2) putting the tasks in the global_q 
        Input:       choice --> (1) ACO operation (2) putting in global queue   and pos --> 0 for the ACO operation and different values for putting 
                     in global_q   
        Output:      none

        '''
        global global_queue
        global rlock
    
        rlock.acquire()
        try:
            if(choice==1):
                flag=False
                while(global_queue.qsize() != 0):
                    flag=True
                    myopicList.append(global_queue.get())
                if(flag==True):
                    self.__resetVMs()
                    self.__myopicScheduler(self.cloudlet, self.workflow, self.vmList, self.DAG, self.dependencyMatrix)
            if(choice==2):
                if(self.dependencyMatrix[pos]==0):
                    global_queue.put(pos)
        finally:
            rlock.release()

    def __resetVMs(self):
        for vm in self.vmList:
            vm.setTosetTotalMips()
            vm.setOldStorage()

    def __myopicSchedulerUtil(self):
        while True:
            self.synchronized_queue(1,0)
            time.sleep(5)

    def __myopicScheduler(self):
        allocationList = []
        for taskIndex in global_queue:
            task = self.workflow.taskDict.get(taskIndex)
            execTimeList = []
            minimumExecTime = 0
            for vm in self.vmList:
                try:
                    execTime = (task.mips / vm.currentAllocatedMips)
                    execTimeList.append(execTime)
                    if(minimumExecTime > execTime):
                        minimumExecTime = execTime                     
                except ZeroDivisionError:
                    execTimeList.append(None)
            
            vmIndex = execTime.index(minimumExecTime)
            allocation = Allocation(task.id,self.vmList[vmIndex].id,self.vmList[vmIndex].globalVMId)
            self.vmList[vmIndex].currentAvailableMips = (self.vmList[vmIndex].currentAvailableMips - task.mips) if (self.vmList[vmIndex].currentAvailableMips - task.mips) >=  0 else 0
            self.vmList[vmIndex].currentAvailableStorage = (self.vmList[vmIndex].currentAvailableStorage - task.storage) if (self.vmList[vmIndex].currentAvailableStorage - task.storage) >=  0 else 0
            self.vmList[vmIndex].currentAllocatedMips = (self.vmList[vmIndex].currentAllocatedMips + task.mips) if self.vmList[vmIndex].mips > (self.vmList[vmIndex].currentAllocatedMips + task.mips) else self.vmList[vmIndex].mips
            self.vmList[vmIndex].currentAllocatedStorage = (self.vmList[vmIndex].currentAllocatedStorage + task.storage) if self.vmList[vmIndex].storage > (self.vmList[vmIndex].currentAllocatedStorage + task.storage) else self.vmList[vmIndex].storage 
            allocationList.append(allocation)
            self.vmList[vmIndex].host.utilizationMips = self.vmList[vmIndex].host.utilizationMips + self.vmList[vmIndex].currentAllocatedMips 

        for vm in self.vmList:
            energyConsumed = vm.host.getPower()
            self.cloudlet.energyConsumption = self.cloudlet.energyConsumption + energyConsumed
