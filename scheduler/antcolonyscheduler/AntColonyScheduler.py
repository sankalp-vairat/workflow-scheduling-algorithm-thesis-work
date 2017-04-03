'''
Created on 16-Mar-2017

@author: itadmin
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

global ACO_list
ACO_list = []

global W_mi
W_mi = 0.2

global W_storage
W_storage = 0.4

global W_deadline
W_deadline = 0.4

global noOfTasks
noOfTasks = 0

global noOfAnts
noOfAnts = 15

global iterations
iterations = 10

class AntColonyScheduler(CloudletScheduler):
    
    def __init__(self):
        self.cloudlet = None
        self.workflow = None
        self.vmList = None
        self.DAG_matrix = None
        self.dependencyMatrix = None

    def __initializeParameters(self):
        '''
        Function:    Initialize all the parameters such as number of tasks ,number of VMs, dimensions of DAG,VM
        Input:       DAG, VM, pheromone
        Output:      none
        
        '''
        print "Initializing parameters......."
        
        global DAG_row
        global DAG_column
        global VM_row
        global VM_column
        global p_row_task
        global p_column_task
        global p_row_VM
        global p_column_VM
        global DAG
        DAG_row=len(DAG)
        DAG_column=len(DAG)
        VM_row=len(VM)
        VM_column=len(VM[0])
        p_row_task=DAG_row
        p_column_task=DAG_column
        p_row_VM=DAG_row
        p_column_VM=VM_row

        graph_vm_mapping=[[1 for i in range(DAG_row)] for j in range(VM_row) ]

    def __initializePheromone(self):
        '''
        Function:    Initialize Pheromone trails
        Input:        initial value of pheromone trails "initial_trail"
        Output:    none

        '''
        print "Initializing trails with pheromone :"
        del pheromone_task_level [:]
        del pheromone_VM_level [:]
        
        for i in range(p_row_task):
            pheromone_task_level.append(tau_0_task)
            
        for i in range(p_column_task):
            temp_pheromone_list=[]
            for j in range(p_column_VM):
                temp_pheromone_list.append(tau_0_VM)
            pheromone_VM_level.append(temp_pheromone_list)


    def __evaporationTaskLevel(self):
        '''
        FUNCTION:      implements the pheromone trail evaporation for task level
        INPUT:         pheromone matrix task level
        OUTPUT:        none
        (SIDE)EFFECTS: pheromones are reduced by factor rho

        '''
        
        print "Performing pheromone evaporation task level.............."
        
        for i in range(p_row_task):
            for j in range(p_column_task):
                pheromone_task_level[i][j] = (1 - rho_task) * pheromone_task_level[i][j];


    def __evaporationVMLevel(self):
        '''
        FUNCTION:      implements the pheromone trail evaporation for VM level
        INPUT:         pheromone matrix task level
        OUTPUT:        none
        (SIDE)EFFECTS: pheromones are reduced by factor rho

        '''
        print "evaporating pheromone on VM level.............."
        
        for i in range(p_row_VM):
            for j in range(p_column_VM):
                pheromone_VM_level[i][j] = (1 - rho_VM) * pheromone_VM_level[i][j];


    def __localPheromoneUpdateTaskLevel(self,i):
        '''
        FUNCTION:      reinforces the last visited edge by ant k at task level
        INPUT:         pheromone matrix of task level, phi, tau_0_task
        OUTPUT:        none
        (SIDE)EFFECTS: pheromone value is updated on the edge (i,j)
        
        '''         
        print "performing local pheromone update at task level................."
        
        phi=0.2                                                                         #decay coefficient
        pheromone_task_level[i]=(1-phi)*pheromone_task_level[i]+phi*tau_0_task


    def __localPheromoneUpdateVMLevel(self,i,j):
        '''
        FUNCTION:      reinforces the last visited edge by ant k at VM level
        INPUT:         pheromone matrix of VM level, phi, tau_0_VM
        OUTPUT:        none
        (SIDE)EFFECTS: pheromone value is updated on the edge (i,j)
        
        '''
        
        print "performing local pheromone update at VM level................."
                     
        phi=0.2                                                                         #decay coefficient
        pheromone_VM_level[i][j]=(1-phi)*pheromone_VM_level[i][j]+phi*tau_0_VM


    def __globalUpdatePheromoneTaskLevel(self,SLAV_delta_tau_global_list,ants_allocation_list):
        '''
        FUNCTION:      reinforces edges used in ant k's solution at task level
        INPUT:         pheromone matrix of task level, phi, tau_0_VM
        OUTPUT:        none
        (SIDE)EFFECTS: pheromone value is updated on the edges (i,j) which are part of ant k's solution
        
        '''
        print "performing global pheromone update at task level................."
        
        min_SLAV_delta_tau = min(SLAV_delta_tau_global_list)
        index = SLAV_delta_tau_global_list.index(min_SLAV_delta_tau)
        
        ant_allocation_list = ants_allocation_list[index]
        
        temp_len = len(ant_allocation_list)
        
        task = ant_allocation_list[0].task
        gamma=0.1
        pheromone_task_level[task] = (1 - rho_task) * pheromone_task_level[task] + rho_task * (1 - min_SLAV_delta_tau**gamma)
        
        for i in range(1,temp_len):
            gamma=gamma+0.1
            task = ant_allocation_list[i].task
            #VM = ant_allocation_list[i].assigned_VM
            pheromone_task_level[task] = (1 - rho_task) * pheromone_task_level[task] + rho_task * (1 - min_SLAV_delta_tau**gamma)


    def __globalUpdatePheromoneVMLevel(self,SLAV_delta_tau_global_list,ants_allocation_list):
        '''
        FUNCTION:      reinforces edges used in ant k's solution at task level
        INPUT:         pheromone matrix of task level, phi, tau_0_VM
        OUTPUT:        none
        (SIDE)EFFECTS: pheromone value is updated on the edges (i,j) which are part of ant k's solution
        
        '''    

        print "performing global pheromone update at VM level................."
        
        normalize(SLAV_delta_tau_global_list)
        min_SLAV_delta_tau = min(SLAV_delta_tau_global_list)
        index = SLAV_delta_tau_global_list.index(min_SLAV_delta_tau)
        
        ant_allocation_list = ants_allocation_list[index]
        
        temp_len = len(ant_allocation_list)
        for i in range(temp_len):
            task = ant_allocation_list[i].task
            VM = ant_allocation_list[i].assigned_VM
            pheromone_VM_level[task][VM] = (1 - rho_VM) * pheromone_VM_level[task][VM] + rho_VM * (1 - min_SLAV_delta_tau)

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
            
        starting_thread = Thread(target = self.__maxMinSchedulerUtil(), args = ())
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
            print "hello"
            self.__synchronizedQueue(1,0)
            time.sleep(5)
        #threading.current_thread().__stop()
