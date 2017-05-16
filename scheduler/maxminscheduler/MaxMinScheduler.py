'''
Created on 29-Mar-2017

@author: sankalp
'''

from scheduler.CloudletScheduler import CloudletScheduler
import time
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

global maxMinList
maxMinList = []

global W_mi
W_mi = 0.3

global W_storage
W_storage = 0.3

global W_deadline
W_deadline = 0.4

global W_energy
W_energy = 0.5

global noOfTasks
noOfTasks = 0

global total_time
total_time = 0

class MaxMinScheduler(CloudletScheduler):

    def __init__(self):
        self.cloudlet = None
        self.workflow = None
        self.vmList = None
        self.DAG_matrix = None
        self.dependencyMatrix = None

    def execute(self,cloudlet,dataCentre):
        global noOfTasks 
        noOfTasks = 0
        global total_time
        total_time = 0
        self.cloudlet = cloudlet
        self.cloudlet.energyConsumption = 0
        self.workflow = self.cloudlet.getWorkFlow()
        cloudlet.setExecStartTime(time.asctime())
        self.vmList = copy.deepcopy(dataCentre.getVMList())
        self.DAG_matrix = self.workflow.DAG_matrix
        
        self.dependencyMatrix = self.DAG_matrix.dependencyMatrix
        rootTasksIndexes = cloudletSchedulerUtil.findRootTasks(self.DAG_matrix)

        for rootTaskIndex in rootTasksIndexes:
            #self.__synchronizedQueue(2,rootTaskIndex)
            global_queue.put(rootTaskIndex)
            
        #starting_thread = Thread(target = self.__maxMinSchedulerUtil(), args = ())
        #starting_thread.daemon = True
        #starting_thread.start()
        
        self.__maxMinScheduler()

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
                    maxMinList.append(global_queue.get())
                if(flag == True):
                    self.__resetVMs()
                    self.__resetHosts()
                    self.__maxMinScheduler()
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

    def __maxMinSchedulerUtil(self):
        while(noOfTasks < self.DAG_matrix.DAGRows):
            self.__synchronizedQueue(1,0)
            time.sleep(5)
        #threading.current_thread().__stop()

    def __makespanCalculations(self,ant_allocation_list):
        self.__resetVMs()
        self.__resetHosts()    

        total_length = len(ant_allocation_list)

        VM_list_a={}
        for i in range(0,total_length):
            if(VM_list_a.has_key(ant_allocation_list[i].assignedVMGlobalId)):
                VM_list_a[ant_allocation_list[i].assignedVMGlobalId] = VM_list_a.get(ant_allocation_list[i].assignedVMGlobalId) + self.workflow.taskDict.get(str(ant_allocation_list[i].taskID)).MI
            else:
                VM_list_a[ant_allocation_list[i].assignedVMGlobalId] = self.workflow.taskDict.get(str(ant_allocation_list[i].taskID)).MI
            
        time_temp = 0   
            
        for k,v in VM_list_a.items():
            try:
                time_temp = time_temp + v / self.vmList[k].getMips()
            except ZeroDivisionError:
                time_temp = sys.float_info.max

        return time_temp


    def __calculateEnergyConsumptionOfSchedule(self,ant_allocation_list):
        '''
        Function:    calculates the partial energy consumption of schedule   
        Input:       
        Output:      

        '''
        
        self.__resetHosts()
        self.__resetVMs()
        
        temp_len = len(ant_allocation_list)
        vmDict = {}

        for i in range(temp_len):
            taskID = int(ant_allocation_list[i].taskID)
            vmID = int(ant_allocation_list[i].assignedVMGlobalId)
            self.vmList[vmID].addTask(self.workflow.taskDict.get(str(taskID)))
            vmDict.update({vmID:self.vmList[vmID]})

        hostTasksBucket = {}
        hostDict = {}
        for vmID,vm in vmDict.iteritems():
            numberOfTasksAssigned = len(vm.tasksAllocated)
            for i in range(numberOfTasksAssigned):
                vm.host.utilizationMips = vm.host.utilizationMips + vm.tasksAllocated[i].MI
                try:
                    time_taken = vm.tasksAllocated[i].MI / vm.currentAvailableMips
                except ZeroDivisionError:
                    time_taken = sys.float_info.max
                vm.tasksAllocated[i].currentCompletionTime = time_taken 
                vm.currentAvailableMips = vm.currentAvailableMips - vm.tasksAllocated[i].MI
                vm.currentAvailableMips = vm.currentAllocatedMips + vm.tasksAllocated[i].MI
                if(hostTasksBucket.has_key(vm.host.id)):
                    tempList = hostTasksBucket.get(vm.host.id)
                    tempList.append(vm.tasksAllocated[i])
                    hostTasksBucket.update({vm.host.id:tempList})
                else:
                    hostTasksBucket.update({vm.host.id:[vm.tasksAllocated[i]]})

                hostDict.update({vm.host.id:vm.host})
        
        for hostID,tasksList in hostTasksBucket.iteritems():
            tasksList_d = hostTasksBucket.get(hostID)
            tasksList_d.sort(key = lambda x: x.currentCompletionTime)
            hostTasksBucket.update({hostID:tasksList_d})
        #new changes
        totalEnergyConsumed = 0
        energyConsumed = [] 
        for hostID,tasksList in hostTasksBucket.iteritems():
            numberOftasks = len(tasksList)
            energyConsumedByHost = []
            flag = True
            timeSlice = 0.0
            for i in range(numberOftasks):
                if(flag == True):
                    utilizationMips = tasksList[i].MI
                if((i+1 < numberOftasks) and tasksList[i].currentCompletionTime == tasksList[i+1].currentCompletionTime):
                    utilizationMips = utilizationMips + tasksList[i+1].MI
                    flag =False
                else:
                    EnergyConsumed = hostDict.get(hostID).getEnergyDefinedHost(hostDict.get(hostID).utilizationMips,hostDict.get(hostID).getTotalMips(),(tasksList[i].currentCompletionTime-timeSlice))
                    #EnergyConsumed = hostDict.get(hostID).getEnergy(hostDict.get(hostID).utilizationMips,hostDict.get(hostID).getTotalMips(),(tasksList[i].currentCompletionTime-timeSlice))
                    energyConsumedByHost.append(EnergyConsumed)
                    totalEnergyConsumed =  totalEnergyConsumed + EnergyConsumed
                    hostDict.get(hostID).utilizationMips = hostDict.get(hostID).utilizationMips - utilizationMips
                    timeSlice = tasksList[i].currentCompletionTime
                    flag =  True
            energyConsumed.append(energyConsumedByHost)
        return totalEnergyConsumed

    def __maxMinScheduler(self):
        self.__resetVMs()
        self.__resetHosts()

        global W_deadline
        global W_mi
        global W_storage
        global noOfTasks
        global total_time
        
        while(global_queue.qsize() != 0):
            maxMinList.append(global_queue.get())

        allocationList = []
        SLAVMi = 0
        SLAVStorage = 0
        SLAVRuntime = 0

        totalMi = 0
        totalStorage = 0
        totalRuntime = 0
        
        lenMaxMinList = len(maxMinList)
        for l in range(lenMaxMinList):
            allocation = Allocation()
            maximumExecTime =  0
            taskSelectedIndex = 0
            vmIndex = 0
            for taskIndex in maxMinList:
                task = self.workflow.taskDict.get(str(taskIndex))
                execTimeList = []
                vmIndex = 0
                tempVMIndex = 0
                for vm in self.vmList:
                    try:
                        execTime = (task.MI / vm.currentAvailableMips)
                        execTimeList.append(execTime)
                        if(maximumExecTime < execTime):
                            maximumExecTime = execTime
                            allocation.taskId = task.id.split('_')[1]
                            allocation.assignedVMId = vm.id
                            allocation.assignedVMGlobalId = vm.globalVMId
                            taskSelectedIndex = taskIndex
                            vmIndex = tempVMIndex
                    except ZeroDivisionError:
                        execTimeList.append(None)
                    tempVMIndex = tempVMIndex + 1
            del maxMinList [maxMinList.index(taskSelectedIndex)]

            #SLA violation calculation
            SLAVMi = SLAVMi + (self.workflow.taskDict.get(allocation.taskId).MI - self.vmList[vmIndex].currentAvailableMips)
            SLAVStorage = SLAVStorage + 0 if(self.workflow.taskDict.get(allocation.taskId).storage - self.vmList[vmIndex].currentAvailableStorage)<0 else (self.workflow.taskDict.get(allocation.taskId).storage - self.vmList[vmIndex].currentAvailableStorage)
            SLAVRuntime = SLAVRuntime + maximumExecTime 

            totalMi = totalMi + self.workflow.taskDict.get(allocation.taskId).MI
            totalStorage = totalStorage + self.workflow.taskDict.get(allocation.taskId).storage 
            totalRuntime = totalRuntime + self.workflow.taskDict.get(allocation.taskId).runtime

            self.vmList[vmIndex].currentAvailableMips = (self.vmList[vmIndex].currentAvailableMips - self.workflow.taskDict.get(allocation.taskId).MI) if (self.vmList[vmIndex].currentAvailableMips - self.workflow.taskDict.get(allocation.taskId).MI) >=  0 else 0
            self.vmList[vmIndex].currentAvailableStorage = (self.vmList[vmIndex].currentAvailableStorage - self.workflow.taskDict.get(allocation.taskId).storage) if (self.vmList[vmIndex].currentAvailableStorage - self.workflow.taskDict.get(allocation.taskId).storage) >=  0 else 0
            self.vmList[vmIndex].currentAllocatedMips = (self.vmList[vmIndex].currentAllocatedMips + self.workflow.taskDict.get(allocation.taskId).MI) if self.vmList[vmIndex].mips > (self.vmList[vmIndex].currentAllocatedMips + self.workflow.taskDict.get(allocation.taskId).MI) else self.vmList[vmIndex].mips
            self.vmList[vmIndex].currentAllocatedStorage = (self.vmList[vmIndex].currentAllocatedStorage + self.workflow.taskDict.get(allocation.taskId).storage) if self.vmList[vmIndex].storage > (self.vmList[vmIndex].currentAllocatedStorage + self.workflow.taskDict.get(allocation.taskId).storage) else self.vmList[vmIndex].storage 
            allocationList.append(allocation)
            self.vmList[vmIndex].host.utilizationMips = self.vmList[vmIndex].host.utilizationMips + self.vmList[vmIndex].currentAllocatedMips

            for j in range(self.DAG_matrix.DAGRows):
                if(self.DAG_matrix.DAG[j][int(allocation.taskId)] == 1):
                    self.DAG_matrix.dependencyMatrix[j] = self.DAG_matrix.dependencyMatrix[j] - 1
                    if(self.DAG_matrix.dependencyMatrix[j] == 0):
                        #self.__synchronizedQueue(2, j)
                        global_queue.put(j)

            noOfTasks = noOfTasks + 1

        energyConsumed = self.__calculateEnergyConsumptionOfSchedule(allocationList)
        self.cloudlet.energyConsumption = self.cloudlet.energyConsumption + energyConsumed
            
        SLAViolation = (( 0 if SLAVMi < 0 else SLAVMi) / totalMi) * W_mi + ( (0 if SLAVStorage < 0 else SLAVStorage)  / totalStorage) * W_storage + ((0 if SLAVRuntime < 0 else SLAVRuntime) / totalRuntime) * W_deadline
        self.cloudlet.addSLAViolationList(SLAViolation)
            
        #for vm in self.vmList:
        #    energyConsumed = vm.host.getPower()
        #    self.cloudlet.energyConsumption = self.cloudlet.energyConsumption + energyConsumed
        total_time = total_time + self.__makespanCalculations(allocationList) 

        if(noOfTasks == self.DAG_matrix.DAGRows):

            print "Total Energy Consumed is ::",self.cloudlet.energyConsumption
            cloudletSchedulerUtil.printf( "Total Energy Consumed is ::"+str(self.cloudlet.energyConsumption))

            sumSLAViolation = 0

            for SLAViolation in self.cloudlet.SLAViolationList:
                sumSLAViolation = sumSLAViolation + SLAViolation

            averageSLAViolation = sumSLAViolation / len(self.cloudlet.SLAViolationList) 

            print "Average SLA Violation is ::",averageSLAViolation
            
            cloudletSchedulerUtil.printf("Average SLA Violation is ::"+str(averageSLAViolation))

            print "Execution Start Time::",self.cloudlet.execStartTime
            
            cloudletSchedulerUtil.printf("Execution Start Time::"+str(self.cloudlet.execStartTime))

            self.cloudlet.finishTime = time.asctime()

            print "Execution finish time::",self.cloudlet.finishTime
            
            cloudletSchedulerUtil.printf("Execution finish time::"+str(self.cloudlet.finishTime))

            print "Makespan::",total_time
            
            cloudletSchedulerUtil.printf("Makespan::"+str(total_time))
        
        else:
            if(global_queue.qsize() != 0):
                self.__maxMinScheduler()