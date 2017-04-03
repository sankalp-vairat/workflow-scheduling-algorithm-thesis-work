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
from scheduler.CloudletSchedulerUtil import CloudletSchedulerUtil
import threading
import sys

global cloudletSchedulerUtil
cloudletSchedulerUtil = CloudletSchedulerUtil()

global rlock                            #rentrant lock for the synchronized method
rlock = threading.RLock()


global global_queue
global_queue = Queue()

global minMinList
minMinList = []

global W_mi
W_mi = 0.2

global W_storage
W_storage = 0.4

global W_deadline
W_deadline = 0.4

global noOfTasks
noOfTasks = 0

class MinMInScheduler(CloudletScheduler):

    def __init__(self):
        self.cloudlet = None
        self.workflow = None
        self.vmList = None
        self.DAG_matrix = None
        self.dependencyMatrix = None

    def execute(self,cloudlet,dataCentre):
        self.cloudlet = cloudlet
        self.workflow = self.cloudlet.getWorkFlow()
        cloudlet.setExecStartTime(time.asctime())
        self.vmList = copy.deepcopy(dataCentre.getVMList())
        self.DAG_matrix = self.workflow.DAG_matrix
        
        self.dependencyMatrix = self.DAG_matrix.dependencyMatrix
        rootTasksIndexes = cloudletSchedulerUtil.findRootTasks(self.DAG_matrix)

        for rootTaskIndex in rootTasksIndexes:
            self.__synchronizedQueue(2,rootTaskIndex)
            
        starting_thread = Thread(target = self.__myopicSchedulerUtil(), args = ())
        #starting_thread.daemon = True
        starting_thread.start()

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
            if(choice == 1):
                flag = False
                while(global_queue.qsize() != 0):
                    flag = True
                    minMinList.append(global_queue.get())
                if(flag == True):
                    self.__resetVMs()
                    self.__resetHosts
                    self.__minMinScheduler()
            if(choice == 2):
                if(self.dependencyMatrix[pos] == 0):
                    global_queue.put(pos)
        finally:
            rlock.release()


    def __resetVMs(self):
        for vm in self.vmList:
            vm.setTotalMips()
            vm.setOldStorage()
            
    def __resetHosts(self):
        for vm in self.vmList:
            vm.host.resetUtilizationMips()

    def __minMinSchedulerUtil(self):
        while(noOfTasks < self.DAG_matrix.DAGRows):
            print "hello"
            self.__synchronizedQueue(1,0)
            time.sleep(5)
        #threading.current_thread().__stop()

    def __minMinScheduler(self):

        global W_deadline
        global W_mi
        global W_storage
        global noOfTasks
        
        allocationList = []
        SLAVMi = 0
        SLAVStorage = 0
        SLAVRuntime = 0

        totalMi = 0
        totalStorage = 0
        totalRuntime = 0

        for taskIndex in myopicList:
            task = self.workflow.taskDict.get(str(taskIndex))
            execTimeList = []
            minimumExecTime =  sys.float_info.max 
            for vm in self.vmList:
                try:
                    execTime = (task.MI / vm.currentAvailableMips)
                    execTimeList.append(execTime)
                    if(minimumExecTime > execTime):
                        minimumExecTime = execTime     
                except ZeroDivisionError:
                    execTimeList.append(None)

            vmIndex = execTimeList.index(minimumExecTime)
            allocation = Allocation(task.id,self.vmList[vmIndex].id,self.vmList[vmIndex].globalVMId)

            #SLA violation calculation
            SLAVMi = SLAVMi + (task.MI - self.vmList[vmIndex].currentAvailableMips)
            SLAVStorage = SLAVStorage + (task.storage - self.vmList[vmIndex].currentAvailableStorage)
            SLAVRuntime = SLAVRuntime + minimumExecTime 

            totalMi = totalMi + task.MI
            totalStorage = totalStorage + task.storage 
            totalRuntime = totalRuntime + task.runtime

            self.vmList[vmIndex].currentAvailableMips = (self.vmList[vmIndex].currentAvailableMips - task.MI) if (self.vmList[vmIndex].currentAvailableMips - task.MI) >=  0 else 0
            self.vmList[vmIndex].currentAvailableStorage = (self.vmList[vmIndex].currentAvailableStorage - task.storage) if (self.vmList[vmIndex].currentAvailableStorage - task.storage) >=  0 else 0
            self.vmList[vmIndex].currentAllocatedMips = (self.vmList[vmIndex].currentAllocatedMips + task.MI) if self.vmList[vmIndex].mips > (self.vmList[vmIndex].currentAllocatedMips + task.MI) else self.vmList[vmIndex].mips
            self.vmList[vmIndex].currentAllocatedStorage = (self.vmList[vmIndex].currentAllocatedStorage + task.storage) if self.vmList[vmIndex].storage > (self.vmList[vmIndex].currentAllocatedStorage + task.storage) else self.vmList[vmIndex].storage 
            allocationList.append(allocation)
            self.vmList[vmIndex].host.utilizationMips = self.vmList[vmIndex].host.utilizationMips + self.vmList[vmIndex].currentAllocatedMips
            
            noOfTasks = noOfTasks + 1
        
        SLAViolation = (( 0 if SLAVMi < 0 else SLAVMi) / totalMi) * W_mi + ( (0 if SLAVStorage < 0 else SLAVStorage)  / totalStorage) * W_storage + ((0 if SLAVRuntime < 0 else SLAVRuntime) / totalRuntime) * W_deadline
        self.cloudlet.addSLAViolationList(SLAViolation)
        
        for vm in self.vmList:
            energyConsumed = vm.host.getPower()
            self.cloudlet.energyConsumption = self.cloudlet.energyConsumption + energyConsumed
        
        # Clearing the dependencies----------------------------------------------------------------------------------------------------------
        for i in range(len(myopicList)):
            for j in range(self.DAG_matrix.DAGRows):
                if(self.DAG_matrix.DAG[j][myopicList[i]]==1):
                    self.DAG_matrix.dependencyMatrix[j]=self.DAG_matrix.dependencyMatrix[j]-1
                    if(self.DAG_matrix.dependencyMatrix[j]==0):
                        self.__synchronizedQueue(2, j)

        del myopicList[:]

        if(noOfTasks == self.DAG_matrix.DAGRows):

            print "Total Energy Consumed is ::",self.cloudlet.energyConsumption

            sumSLAViolation = 0

            for SLAViolation in self.cloudlet.SLAViolationList:
                sumSLAViolation = sumSLAViolation + SLAViolation

            averageSLAViolation = sumSLAViolation / len(self.cloudlet.SLAViolationList) 

            print "Average SLA Violation is ::",averageSLAViolation

            print "Execution Start Time::",self.cloudlet.execStartTime

            self.cloudlet.finishTime = time.asctime()

            print "Execution finish time::",self.cloudlet.finishTime