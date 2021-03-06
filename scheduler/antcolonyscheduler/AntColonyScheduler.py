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
import random

global SLA_violation_incidents
SLA_violation_incidents = 0

global cloudletSchedulerUtil
cloudletSchedulerUtil = CloudletSchedulerUtil()

global rlock                            #rentrant lock for the synchronized method
rlock = threading.RLock()

global min_delta_SLAV_list
min_delta_SLAV_list=[]

global global_queue
global_queue = Queue()

global total_time                       #total time taken for the execution of the DAG
total_time = 0

global ACO_list
ACO_list = []

global W_mi
W_mi = 0.2

global W_storage
W_storage = 0.1

global W_deadline
W_deadline = 0.5

global W_energy
W_energy = 0.5

global noOfTasks
noOfTasks = 0

global no_Of_Ants
no_Of_Ants = 30

global iterations
iterations = 100

global pheromone_task_level
pheromone_task_level = []

global pheromone_VM_level
pheromone_VM_level = []

global tau_0_task
tau_0_task = 0.2

global tau_0_VM
tau_0_VM = 0.2

global rho_task
rho_task = 0.2

global rho_VM
rho_VM = 0.2

global noOfVMs
noOfVMs = 0
400
global DAG_row
DAG_row = 0

global DAG_column
DAG_column = 0

global p_row_task
p_row_task = 0

global p_column_task
p_column_task = 0

global p_row_VM
p_row_VM = 0

global p_column_VM
p_column_VM = 0


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
        Output:      none400
        
        '''
        #print "Initializing parameters......."
        
        global DAG_row
        global DAG_column
        global p_row_task
        global p_column_task
        global p_row_VM
        global p_column_VM
        global noOfVMs
        
        DAG_row = self.DAG_matrix.DAGRows
        DAG_column = self.DAG_matrix.DAGColumns
        noOfVMs = len(self.vmList)
        p_row_task = DAG_row
        p_column_task = DAG_column
        p_row_VM = DAG_row
        p_column_VM = noOfVMs


    def __initializePheromone(self):
        '''
        Function:    Initialize Pheromone trails
        Input:        initial value of pheromone trails "initial_trail"
        Output:    none

        '''
        #print "Initializing trails with pheromone :"
        global pheromone_task_level
        global pheromone_VM_level
        global p_row_task
        global p_column_task
        global tau_0_task
        global tau_0_VM
        
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
        
        #print "Performing pheromone evaporation task level.............."
        
        for i in range(p_row_task):
            pheromone_task_level[i] = (1 - rho_task) * pheromone_task_level[i];


    def __evaporationVMLevel(self):
        '''
        FUNCTION:      implements the pheromone trail evaporation for VM level
        INPUT:         pheromone matrix task level
        OUTPUT:        none
        (SIDE)EFFECTS: pheromones are reduced by factor rho

        '''
        #print "evaporating pheromone on VM level.............."
        global p_row_task
        global p_column_task
        
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
        #print "performing local pheromone update at task level................."

        phi=0.1                                                                         #decay coefficient
        pheromone_task_level[i]=(1-phi)*pheromone_task_level[i]+phi*tau_0_task


    def __localPheromoneUpdateVMLevel(self,i,j):
        '''
        FUNCTION:      reinforces the last visited edge by ant k at VM level
        INPUT:         pheromone matrix of VM level, phi, tau_0_VM
        OUTPUT:        none
        (SIDE)EFFECTS: pheromone value is updated on the edge (i,j)
        
        '''
        
        #print "performing local pheromone update at VM level................."
                     
        phi=0.1                                                                         #decay coefficient
        pheromone_VM_level[i][j]=(1-phi)*pheromone_VM_level[i][j]+phi*tau_0_VM


    def __globalUpdatePheromoneTaskLevel(self,index,minDeltaTau,ants_allocation_list):
        '''
        FUNCTION:      reinforces edges used in ant k's solution at task level
        INPUT:         pheromone matrix of task level, phi, tau_0_VM
        OUTPUT:        none
        (SIDE)EFFECTS: pheromone value is updated on the edges (i,j) which are part of ant k's solution
        
        '''
        #print "performing global pheromone update at task level................."
        
        #min_SLAV_delta_tau = min(SLAV_delta_tau_global_list)
        #index = SLAV_delta_tau_global_list.index(min_SLAV_delta_tau)
        
        ant_allocation_list = ants_allocation_list[index]
        
        temp_len = len(ant_allocation_list)
        
        task = int(ant_allocation_list[0].taskID.split('_')[1])
        gamma=0.1
        pheromone_task_level[task] = (1 - rho_task) * pheromone_task_level[task] + rho_task * (1 - minDeltaTau**gamma)
        
        for i in range(1,temp_len):
            gamma=gamma + 0.1
            task = int(ant_allocation_list[i].taskID.split('_')[1])
            #VM = ant_allogetEnergycation_list[i].assigned_VM
            pheromone_task_level[task] = (1 - rho_task) * pheromone_task_level[task] + rho_task * (1 - minDeltaTau**gamma)


    def __globalUpdatePheromoneVMLevel(self,index,minDeltaTau,ants_allocation_list):
        '''
        FUNCTION:      reinforces edges used in ant k's solution at task level
        INPUT:         pheromone matrix of task level, phi, tau_0_VM
        OUTPUT:        none
        (SIDE)EFFECTS: pheromone value is updated on the edges (i,j) which are part of ant k's solution
        
        '''    

        #print "performing global pheromone update at VM level................."
        
        #length = len(SLAV_delta_tau_global_list)
        
        #SLAV_delta_tau_global_list_dummy = []
        
        #for i in range(length):
        #    SLAV_delta_tau_global_list_dummy.append(SLAV_delta_tau_global_list[i])
 
        #cloudletSchedulerUtil.normalize(SLAV_delta_tau_global_list_dummy)
        
        #min_SLAV_delta_tau = min(SLAV_delta_tau_global_list_dummy)
        #index = SLAV_delta_tau_global_list.index(min_SLAV_delta_tau)
        
        ant_allocation_list = ants_allocation_list[index]

        temp_len = len(ant_allocation_list)
        for i in range(temp_len):
            task = int(ant_allocation_list[i].taskID.split('_')[1])
            VM = int(ant_allocation_list[i].assignedVMGlobalId)
            pheromone_VM_level[task][VM] = (1 - rho_VM) * pheromone_VM_level[task][VM] + rho_VM * (1 - minDeltaTau)
        
        return ant_allocation_list 

    def __rouletteWheel(self,probability_list,limit):
        '''
        Function:    Roulette wheel selection
        Input:       
        Output:      

        '''
        len_roulette = len(probability_list)
        
        cumulative_probability_list = []
        
        cumulative_probability = 0.0
         
        for i in range(len_roulette):
            cumulative_probability = cumulative_probability + probability_list[i]
            cumulative_probability_list.append(cumulative_probability)
        
        random_probability = random.uniform(0,limit)
        
        index = 0
        
        for i in range(len_roulette):
            if(random_probability <= cumulative_probability_list[i]):
                index = i
                break
        
        return index

    def __selectTask(self,temp_ACO_list):
        '''
        Function:    Applies ACO on the independent tasks that are present in the ACO_list
        Input:       DAG, ACO_list, 
        Output:      A list of the ants solution for all the iterations

        '''
        
        #print "Selecting task......................................"    
        
        temp_len = len(temp_ACO_list)
        temp_MI_list = []
        temp_storage_list = []
        temp_deadline_list = []
        for i in range(temp_len):
            #temp_MI_list.append(float(self.workflow.taskDict.get(str(temp_ACO_list[i])).MI))
            #temp_storage_list.append(float(self.workflow.taskDict.get(str(temp_ACO_list[i])).storage))
            temp_deadline_list.append(float(self.workflow.taskDict.get(str(temp_ACO_list[i])).runtime))
        
        #min_MI = temp_MI_list[0]
        #max_MI = temp_MI_list[0]
        #min_storage = temp_storage_list[0]
        #max_storage = temp_storage_list[0]
        min_deadline = temp_deadline_list[0]
        max_deadline = temp_deadline_list[0]
        
        for i in range(1,temp_len):
            
            #if(temp_MI_list[i] > max_MI):
            #    max_MI = temp_MI_list[i]
            
            #if(temp_MI_list[i] < min_MI):
            #    min_MI = temp_MI_list[i]
                
            #if(temp_storage_list[i] > max_storage):
            #    max_storage = temp_storage_list[i]
            
            #if(temp_storage_list[i] < min_storage):
            #    min_storage = temp_storage_list[i]
                
            if(temp_deadline_list[i] > max_deadline):
                max_deadline = temp_deadline_list[i]
            
            if(temp_deadline_list[i] < min_deadline):
                min_deadline = temp_deadline_list[i]
            
        lambda_Mi_list = []
        lambda_storage_list = []
        lambda_deadline_list = []
        
        for i in range(temp_len):
            '''
            try:
                lambda_Mi_list.append((temp_MI_list[i] - min_MI) / (max_MI - min_MI ))
            except ZeroDivisionError:
                lambda_Mi_list.append(sys.float_info.max)
            
            try:
                lambda_storage_list.append((temp_storage_list[i] - min_storage) / (max_storage - min_storage ))
            except ZeroDivisionError:
                lambda_storage_list.append(sys.float_info.max)
            '''    
            try:
                lambda_deadline_list.append((temp_deadline_list[i] - min_deadline) / (max_deadline - min_deadline ))
            except ZeroDivisionError:
                lambda_deadline_list.append(sys.float_info.max)
        
        #cloudletSchedulerUtil.normalize(lambda_Mi_list)     
        #cloudletSchedulerUtil.normalize(lambda_storage_list)
        cloudletSchedulerUtil.normalize(lambda_deadline_list)
           
        eta_task_list=[]
        W_MI = 0.4                                          # weightage for MI
        W_storage = 0.2                                     # weightage for storage
        W_deadline = 0.4                                    # weightage for deadline
        W_deadline = 1.0                                    # weightage for deadline
            
        for i in range(temp_len):    
            #eta_task_list.append (  (lambda_Mi_list[i] * W_MI  +  lambda_storage_list[i] * W_storage  +  lambda_deadline_list[i] * W_deadline ))
            eta_task_list.append ( lambda_deadline_list[i] * W_deadline )

        #Heuristic information calculation--------------------------------------------------------------------------------------------
                    
        alpha_pheromone = 0.6                 # weightage for the pheromone
        beta_eta = 0.4                       # weightage for the eta(heuristic information) 
        alpha_pheromone_mult_beta_eta = 0
            
        for i in range(temp_len):    
            alpha_pheromone_mult_beta_eta = alpha_pheromone_mult_beta_eta + (pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * (1 - ( eta_task_list[i] ** beta_eta ))
            
        #----------------------------------------------------------------------------------------------------------------------------

        #probability calculation for edge selection----------------------------------------------------------------------------------

        probability_of_selection_list = []
        for i in range(temp_len):
            try:
                probability_of_selection_list.append( ( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( 1-((eta_task_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
            except ZeroDivisionError:
                probability_of_selection_list.append(1)

        temp_probability_of_selection_list = []

        for i in range(temp_len):
            temp_probability_of_selection_list.append(probability_of_selection_list[i])

        limit = 1.0
        temp_ACO_list_1 = []
        for  i in range(temp_len):
            index = self.__rouletteWheel(temp_probability_of_selection_list, limit)
            temp_ACO_list_1.append(temp_ACO_list[index])
            temp_probability = temp_probability_of_selection_list[index]
            old_limit = limit
            limit = limit - temp_probability
            del temp_probability_of_selection_list[index]
            del temp_ACO_list[index]
            self.__recalculateProbability(temp_probability_of_selection_list, limit, old_limit)
        
        return temp_ACO_list_1


    def __recalculateProbability(self, _list, new_limit ,old_limit):
        '''
        Function:    recalculates the probability out of new limit 
        Input:       
        Output:      

        '''
        temp_len = len(_list)
        for i in range(temp_len):
            try:
                new_value = (_list[i] / old_limit) * new_limit
                _list[i] = new_value
            except:
                _list[i] = 0 



    def __partialEnergyConsumption(self,VM,task):
        '''
        Function:    calculates the partial energy consumption of schedule   
        Input:       
        Output:      

        '''
        
        host = VM.host
        totalUtilizationMips = 0
        tasksList = []
        for vm in host.VMList:
            numberOfTasksAssigned = len(vm.tasksAllocated)
            for i in range(numberOfTasksAssigned):
                totalUtilizationMips = totalUtilizationMips + vm.tasksAllocated[i].MI
                try:
                    time_taken = vm.tasksAllocated[i].MI / vm.currentAvailableMips
                except ZeroDivisionError:
                    time_taken = sys.float_info.max
                vm.tasksAllocated[i].currentCompletionTime = time_taken
                vm.currentAvailableMips = vm.currentAvailableMips - vm.tasksAllocated[i].MI
                vm.currentAvailableMips = vm.currentAllocatedMips + vm.tasksAllocated[i].MI                 
                tasksList.append(vm.tasksAllocated[i])

        totalUtilizationMips = task.MI
        try:
            time_taken = task.MI / VM.currentAvailableMips
        except ZeroDivisionError:
            time_taken = sys.float_info.max
        task.currentCompletionTime = time_taken
        
        tasksList.append(task)
        numberOftasks = len(tasksList)
        energyConsumed = []
        tasksList.sort(key = lambda x: x.currentCompletionTime)
        totalEnergyConsumed = 0
        
        flag = True
        timeSlice = 0.0
        for i in range(numberOftasks):
            if(flag == True):
                utilizationMips = tasksList[i].MI
            if((i+1 < numberOftasks) and tasksList[i].currentCompletionTime == tasksList[i+1].currentCompletionTime):
                utilizationMips = utilizationMips + tasksList[i+1].MI
                flag =False
            else:
                #EnergyConsumed = host.getEnergyDefinedHost(totalUtilizationMips,host.getTotalMips(),(tasksList[i].currentCompletionTime-timeSlice))
                EnergyConsumed = host.getEnergy(totalUtilizationMips,host.getTotalMips(),(tasksList[i].currentCompletionTime-timeSlice))
                energyConsumed.append(EnergyConsumed)
                totalEnergyConsumed =  totalEnergyConsumed + EnergyConsumed
                totalUtilizationMips = totalUtilizationMips - utilizationMips
                timeSlice = tasksList[i].currentCompletionTime
                flag =  True
        return totalEnergyConsumed
    
    
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
            taskID = int(ant_allocation_list[i].taskID.split('_')[1])
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
                    #EnergyConsumed = hostDict.get(hostID).getEnergyDefinedHost(hostDict.get(hostID).utilizationMips,hostDict.get(hostID).getTotalMips(),(tasksList[i].currentCompletionTime-timeSlice))
                    EnergyConsumed = hostDict.get(hostID).getEnergy(hostDict.get(hostID).utilizationMips,hostDict.get(hostID).getTotalMips(),(tasksList[i].currentCompletionTime-timeSlice))
                    energyConsumedByHost.append(EnergyConsumed)
                    totalEnergyConsumed =  totalEnergyConsumed + EnergyConsumed
                    hostDict.get(hostID).utilizationMips = hostDict.get(hostID).utilizationMips - utilizationMips
                    timeSlice = tasksList[i].currentCompletionTime
                    flag =  True
            energyConsumed.append(energyConsumedByHost)
        return totalEnergyConsumed



    def __calculateDeltaTau(self,miList,storageList,deadlineList,energy_list):
        #cloudletSchedulerUtil.normalize(miList)
        #cloudletSchedulerUtil.normalize(storageList)
        cloudletSchedulerUtil.normalize(deadlineList)
        cloudletSchedulerUtil.normalize(energy_list)

        deltaTauList = []
        deltaTauList_shadow = []
        length =len(deadlineList)
        for i in range(length):
            #deltaTau = miList[i]*W_mi + storageList[i]*W_storage +deadlineList[i]*W_deadline + energy_list[i]*W_energy
            deltaTau = deadlineList[i]*W_deadline + energy_list[i]*W_energy
            deltaTauList.append(deltaTau)
            #deltaTauList_shadow.append(miList[i]*0.3 + storageList[i]*0.3 +deadlineList[i]*0.4)
            deltaTauList_shadow.append(deadlineList[i])
            
            
        index = deltaTauList.index(min(deltaTauList))
        
        #return index,min(deltaTauList),deltaTauList_shadow[index]
        return index,min(deltaTauList),deltaTauList_shadow[index]


        

    def __resetVMs(self):
        for vm in self.vmList:
            vm.setTotalMips()
            vm.setOldStorage()
            del vm.tasksAllocated[:]
            
    def __resetHosts(self):
        for vm in self.vmList:
            vm.host.resetUtilizationMips()
    
    def __ACOScheduler(self):
        '''
        Function:    Applies ACO on the independent tasks that are present in the ACO_list
        Input:       DAG, ACO_list, 
        Output:      A list of the ants solution for all the iterations

        '''

        #print "Executing ACO"
        #print "ACO_LIST",ACO_list

        while(global_queue.qsize() != 0):
            ACO_list.append(global_queue.get())

        global total_time
        global no_Of_Ants
        global iterations
        global noOfTasks
        self.__initializePheromone();

        global total_time

        temp_ACO_list               = []
        iterations_allocation_list  = []                            # This list stores the allocations for all the iterations
        SLAV_delta_tau_global_lists = []

        for it in range(iterations): 
            ants_allocation_list          = []                         # This list stores the allocation for all the ants
            SLAV_delta_tau_global_list    = []
            SLAV_MI_tau_global_list       = []
            SLAV_deadline_tau_global_list = []
            SLAV_storage_tau_global_list  = []
            energy_list            = []
            for nA in range(no_Of_Ants):
                ACO_list_len=len(ACO_list)
                count = ACO_list_len - 1
                ant_allocation_list = []                           # This list stores the allocation for the ant
                
                del temp_ACO_list[:]
                
                for i in range(ACO_list_len):
                    temp_ACO_list.append(ACO_list[i])

                # below parameters are for global pheromone update------------------------------------------------------------------------------

                SLAV_MI_global_list           = []
                SLAV_storage_global_list      = []
                SLAV_deadline_global_list     = []
                MI_required_global_list       = []
                storage_required_global_list  = []
                deadline_required_global_list = []
                #energy_list                   = []
                
                temp_ACO_list = self.__selectTask(temp_ACO_list)
                ant_position = ACO_list_len-1

                underflow_resources_flag = False

                self.__resetVMs()
                self.__resetHosts()

                for ant_position in range(ant_position,-1,-1):

                    storage_violation_list  =  []
                    MI_violation_list       =  []
                    deadline_violation_list =  []
                    energy_consumption_list =  []
                    VM_outof_resources      =  []

                    for t in range(noOfVMs):
                        if(self.vmList[t].currentAvailableMips <= 0 or self.vmList[t].currentAvailableStorage <= 0):
                            VM_outof_resources.append(t)

                    for vm in self.vmList:
                        #temp_MI_violation      = float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI - vm.currentAvailableMips)
                        #temp_storage_violation = float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).storage - vm.currentAvailableStorage)
                        try:
                            temp_deadline_violation = float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).runtime - self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI / vm.currentAvailableMips)
                        except ZeroDivisionError:
                            temp_deadline_violation = sys.float_info.max
        
                        #MI_violation_list.append( temp_MI_violation )
                        #storage_violation_list.append( temp_storage_violation )
                        deadline_violation_list.append( temp_deadline_violation )
                        #vm.addTask(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])))
                        energy_consumption_list.append(self.__partialEnergyConsumption(vm,self.workflow.taskDict.get(str(temp_ACO_list[ant_position]))))
                        
                    #Heuristic information calculation--------------------------------------------------------------------------------------------
                    
                    length_1 = len(deadline_violation_list)                
                    
                    #cloudletSchedulerUtil.normalize(MI_violation_list)
                    #cloudletSchedulerUtil.normalize(storage_violation_list)
                    cloudletSchedulerUtil.normalize(deadline_violation_list)
                    cloudletSchedulerUtil.normalize(energy_consumption_list)
                    
                    eta_list   = []                                       # list of the eta for all the edges from one task to all VMs
                    W_MI       = 0.2                                          # weightage for MI
                    W_storage  = 0.1                                     # weightage for storage
                    W_deadline = 0.3
                    W_energy = 0.7                                    # weightage for deadline
                    
                    for i in range(length_1):
                        #eta_list.append( ( MI_violation_list[i] * W_MI  +  storage_violation_list[i] * W_storage  +  deadline_violation_list[i] * W_deadline + energy_consumption_list[i] * W_energy) )
                        eta_list.append( deadline_violation_list[i] * W_deadline + energy_consumption_list[i] * W_energy) 
                                    
                    #Heuristic information calculation--------------------------------------------------------------------------------------------

                    alpha_pheromone = 0.6                 # weightage for the pheromone
                    beta_eta        = 0.4                 # weightage for the eta(heuristic information) 
                    alpha_pheromone_mult_beta_eta = 0

                    for i in range(p_column_VM):    
                        alpha_pheromone_mult_beta_eta = alpha_pheromone_mult_beta_eta + ( pheromone_VM_level[temp_ACO_list[ant_position]][i] ** alpha_pheromone ) * (1 - ( eta_list[i] ** beta_eta ) )
                    
                    #----------------------------------------------------------------------------------------------------------------------------
                    
                    #probability calculation for edge selection----------------------------------------------------------------------------------

                    probability_of_selection_list=[]

                    for i in range(p_column_VM):
                        try:
                            probability_of_selection_list.append( ( ( pheromone_VM_level[temp_ACO_list[ant_position]][i] ** alpha_pheromone ) * ( 1-((eta_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
                        except ZeroDivisionError:
                            probability_of_selection_list.append(1)
                    

                    largest_probability_index = 0
                    largest_probability       = 0
                    
                    index = self.__rouletteWheel(probability_of_selection_list, 1.0)
                    
                    if(index not in VM_outof_resources):
                        largest_probability_index = index
                        largest_probability       = probability_of_selection_list[index]
                    
                    if(largest_probability==0 and largest_probability_index==0):
                        underflow_resources_flag = True
                        del ant_allocation_list [:] 
                        break
                    #--------------------------------------------------------------------------------------------------------------------------
                    
                    # Calculations for Global pheromone update---------------------------------------------------------------------------------
                    #SLA_MI_global = float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI - self.vmList[largest_probability_index].currentAvailableMips)

                    #if(SLA_MI_global < 0):
                    #    SLA_MI_global=0
                    
                    #SLA_storage_global = float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).storage - self.vmList[largest_probability_index].currentAvailableStorage)
                    
                    #if(SLA_storage_global < 0):
                    #    SLA_storage_global=0
                    
                    try:
                        SLA_deadline_global = float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).runtime - self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI / self.vmList[largest_probability_index].currentAvailableMips)
                    except ZeroDivisionError:
                        SLA_deadline_global = sys.float_info.max
                    
                    if(SLA_deadline_global<0):
                        SLA_deadline_global=0
                    
                    MI_required_global_list.append(float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI))
                    storage_required_global_list.append(float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).storage))
                    deadline_required_global_list.append(float(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).runtime))
                    #SLAV_MI_global_list.append(SLA_MI_global)
                    #SLAV_storage_global_list.append(SLA_storage_global)
                    SLAV_deadline_global_list.append(SLA_deadline_global)
                    
                    #------------------------------------------------------------------------------------------------------------------------
                            
                    ant_allocation = Allocation(self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).id,self.vmList[largest_probability_index].id,self.vmList[largest_probability_index].globalVMId)
                    
                    ant_allocation_list.append(ant_allocation)                  # puting this allocation in the list
                    count = count-1                                             # decrement the ACO list count

                    #updating the VM capacity (storage)-------------------------------------------------------------------------------------
                    self.vmList[largest_probability_index].currentAvailableMips = (self.vmList[largest_probability_index].currentAvailableMips - self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI) if (self.vmList[largest_probability_index].currentAvailableMips - self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI) >=  0 else 0
                    self.vmList[largest_probability_index].currentAvailableStorage = (self.vmList[largest_probability_index].currentAvailableStorage - self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).storage) if (self.vmList[largest_probability_index].currentAvailableStorage - self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).storage) >=  0 else 0
                    self.vmList[largest_probability_index].currentAllocatedMips = (self.vmList[largest_probability_index].currentAllocatedMips + self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI) if self.vmList[largest_probability_index].mips > (self.vmList[largest_probability_index].currentAllocatedMips + self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).MI) else self.vmList[largest_probability_index].mips
                    self.vmList[largest_probability_index].currentAllocatedStorage = (self.vmList[largest_probability_index].currentAllocatedStorage + self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).storage) if self.vmList[largest_probability_index].storage > (self.vmList[largest_probability_index].currentAllocatedStorage + self.workflow.taskDict.get(str(temp_ACO_list[ant_position])).storage) else self.vmList[largest_probability_index].storage                     
                    
                    #local pheromone update-------------------------------------------------------------------------------------------------
                    
                    self.__localPheromoneUpdateVMLevel(temp_ACO_list[ant_position],largest_probability_index)
                    self.__localPheromoneUpdateTaskLevel(temp_ACO_list[ant_position])
                    #-----------------------------------------------------------------------------------------------------------------------
                    
                    del temp_ACO_list[ant_position]
                
                if(underflow_resources_flag == False):
                    #global pheromone calculation-----------------------------------------------------------------------------------------------
                    
                    temp_SLAV_len = len(SLAV_MI_global_list)
                    SLAV_storage_global = 0.0
                    SLAV_MI_global = 0.0
                    SLAV_deadline_global = 0.0
                    temp_SLAV_MI_global_required = 0.0
                    temp_SLAV_storage_global_required = 0.0
                    temp_SLAV_deadline_global_required = 0.0
                    
                    
                    for i in range(temp_SLAV_len):
                        #SLAV_storage_global = SLAV_storage_global + SLAV_storage_global_list[i] #this can be grerater than 1
                        #SLAV_MI_global = SLAV_MI_global + SLAV_MI_global_list[i]
                        SLAV_deadline_global = SLAV_deadline_global + SLAV_deadline_global_list[i]
                        #temp_SLAV_MI_global_required = temp_SLAV_MI_global_required + MI_required_global_list[i]
                        #temp_SLAV_storage_global_required = temp_SLAV_storage_global_required + storage_required_global_list[i]
                        temp_SLAV_deadline_global_required = temp_SLAV_deadline_global_required + deadline_required_global_list[i]
                    

                    #try:
                    #    SLAV_MI_tau_global_list.append(SLAV_MI_global / temp_SLAV_MI_global_required ) 
                    #except ZeroDivisionError:
                    #    SLAV_MI_tau_global_list.append(sys.float_info.max)
                    
                    #try:                
                    #    SLAV_storage_tau_global_list.append( SLAV_storage_global / temp_SLAV_storage_global_required )
                    #except ZeroDivisionError:
                    #    SLAV_storage_tau_global_list.append(sys.float_info.max)
                        
                    try:
                        SLAV_deadline_tau_global_list.append( SLAV_deadline_global / temp_SLAV_deadline_global_required )
                    except ZeroDivisionError:
                        SLAV_deadline_tau_global_list.append(sys.float_info.max)
                    
                    energy_list.append(self.__calculateEnergyConsumptionOfSchedule(ant_allocation_list))
                            
                    #self.calculateDeltaTau(SLAV_MI_tau_global_list, SLAV_storage_tau_global_list, SLAV_deadline_tau_global_list)
                    #SLAV_delta_tau_global_list.append(delta_tau_SLAV)
                    #cloudletSchedulerUtil.printf("delta_tau_SLAV"+"\t"+str(delta_tau_SLAV))
                    ##cloudletSchedulerUtil.printf("----------------------------------------------")
                    #performing evaporation on VM-task graph------------------------------------------------------------------------------------
                    self.__evaporationVMLevel()
                    self.__evaporationTaskLevel()
                    
                    ants_allocation_list.append(ant_allocation_list)
                    
                    #printing ant allocation list
                    cloudletSchedulerUtil.print_allocations(ant_allocation_list,it,nA)

            #performing global pheromone update---------------------------------------------------------------------------------------------
            
            if(len(SLAV_deadline_tau_global_list) > 0):
                indexMin,minDeltaTau,minDeltaTau_shadow = self.__calculateDeltaTau(SLAV_MI_tau_global_list, SLAV_storage_tau_global_list, SLAV_deadline_tau_global_list,energy_list)
                ant_allocation_list = self.__globalUpdatePheromoneVMLevel(indexMin,minDeltaTau,ants_allocation_list)
                self.__globalUpdatePheromoneTaskLevel(indexMin,minDeltaTau,ants_allocation_list)
                SLAV_delta_tau_global_lists.append(minDeltaTau_shadow)
                iterations_allocation_list.append(ant_allocation_list)

        if(len(SLAV_delta_tau_global_lists)>0):

            total_length = len(ACO_list)
            minDeltaSLAVGlobal = min(SLAV_delta_tau_global_lists)
            final_ant_allocation_list = iterations_allocation_list[SLAV_delta_tau_global_lists.index(minDeltaSLAVGlobal )]
            #final_ant_allocation_list = final_ants_allocation_list[min_SLAV_delta_tau_index_j] 


            self.__resetVMs()
            self.__resetHosts()    


            VM_list_a={}
            for i in range(0,total_length):
                if(VM_list_a.has_key(final_ant_allocation_list[i].assignedVMGlobalId)):
                    VM_list_a[final_ant_allocation_list[i].assignedVMGlobalId] = VM_list_a.get(final_ant_allocation_list[i].assignedVMGlobalId) + self.workflow.taskDict.get(final_ant_allocation_list[i].taskID.split('_')[1]).MI
                else:
                    VM_list_a[final_ant_allocation_list[i].assignedVMGlobalId] = self.workflow.taskDict.get(final_ant_allocation_list[i].taskID.split('_')[1]).MI
            
            time_temp = 0   
            
            for k,v in VM_list_a.items():
                try:
                    time_temp = time_temp + v / self.vmList[k].getMips()
                except ZeroDivisionError:
                    time_temp = sys.float_info.max

            total_time = total_time + time_temp
            #print "total_time:",total_time
            #cloudletSchedulerUtil.printf("total_time::"+str(total_time))
            self.cloudlet.SLAViolationList.append(minDeltaSLAVGlobal)

            #cloudletSchedulerUtil.printf("min_SLAV_delta_tau::"+str(minDeltaSLAVGlobal))

            #cloudletSchedulerUtil.printf("min_SLAV_delta_tau::"+str(minDeltaSLAVGlobal))
            #min_delta_SLAV_list.append(min(SLAV_delta_tau_global_lists))
            #print "----------------------------------------------------------------------------------------------------------"

            print "----------------------------------------------------------------------------------------------------------"
            
            self.cloudlet.energyConsumption = self.cloudlet.energyConsumption + self.__calculateEnergyConsumptionOfSchedule(final_ant_allocation_list)

            self.__resetVMs()
            self.__resetHosts()

        else:
            #serial execution of tasks
            pass
        # Clearing the dependencies----------------------------------------------------------------------------------------------------------
        for i in range(len(ACO_list)):
            for j in range(self.DAG_matrix.DAGRows):
                if(self.DAG_matrix.DAG[j][ACO_list[i]]==1):
                    self.DAG_matrix.dependencyMatrix[j]=self.DAG_matrix.dependencyMatrix[j]-1
                    if(self.DAG_matrix.dependencyMatrix[j]==0):
                        #self.__synchronizedQueue(2, j)
                        global_queue.put(j)
        

        # reset ACO_List
        noOfTasks = noOfTasks + len(ACO_list)
        del ACO_list[:]

        '''
        SLAViolation = (( 0 if SLAVMi < 0 else SLAVMi) / totalMi) * W_mi + ( (0 if SLAVStorage < 0 else SLAVStorage)  / totalStorage) * W_storage + ((0 if SLAVRuntime < 0 else SLAVRuntime) / totalRuntime) * W_deadline
        self.cloudlet.addSLAViolationList(SLAViolation)
            
        for vm in self.vmList:
            energyConsumed = vm.host.getPower()
            self.cloudlet.energyConsumption = self.cloudlet.energyConsumption + energyConsumed
        '''
        if(noOfTasks == self.DAG_matrix.DAGRows):

            print "Total Energy Consumed is ::",self.cloudlet.energyConsumption
            cloudletSchedulerUtil.printf( "Total Energy Consumed is ::"+str(self.cloudlet.energyConsumption))

            sumSLAViolation = 0

            for SLAViolation in self.cloudlet.SLAViolationList:
                sumSLAViolation = sumSLAViolation + SLAViolation

            #averageSLAViolation = sumSLAViolation / len(self.cloudlet.SLAViolationList) 

            #print "Average SLA Violation is ::",averageSLAViolation
            
            #cloudletSchedulerUtil.printf("Average SLA Violation is ::"+str(averageSLAViolation))

            print "Execution Start Time::",self.cloudlet.execStartTime
            
            cloudletSchedulerUtil.printf("Execution Start Time::"+str(self.cloudlet.execStartTime))

            self.cloudlet.finishTime = time.asctime()

            print "Execution finish time::",self.cloudlet.finishTime
            
            cloudletSchedulerUtil.printf("Execution finish time::"+str(self.cloudlet.finishTime))

            print "Makespan::",total_time
            
            cloudletSchedulerUtil.printf("Makespan::"+str(total_time))
        else:
            if(global_queue.qsize() != 0):
                self.__ACOScheduler()


    def execute(self,cloudlet,dataCentre):
        global noOfTasks 
        noOfTasks = 0
        global total_time
        total_time = 0
        self.cloudlet = cloudlet
        self.workflow = self.cloudlet.getWorkFlow()
        self.cloudlet.energyConsumption = 0
        self.cloudlet.setExecStartTime(time.asctime())
        
        self.vmList = copy.deepcopy(dataCentre.getVMList())
        self.DAG_matrix = self.workflow.DAG_matrix
        
        self.dependencyMatrix = self.DAG_matrix.dependencyMatrix
        rootTasksIndexes = cloudletSchedulerUtil.findRootTasks(self.DAG_matrix)
        
        self.__initializeParameters()
        for rootTaskIndex in rootTasksIndexes:
            #self.__synchronizedQueue(2,rootTaskIndex)
            global_queue.put(rootTaskIndex)
            
        #starting_thread = Thread(target = self.__ACOSchedulerUtil(), args = ())
        #starting_thread.start()
	    self.__ACOScheduler()

    def __synchronizedQueue(self,choice,pos):
        '''
        Function:    This function synchronizes 1) the reading the values from global_q and then applying ACO and 2) putting the tasks in the global_q 
        Input:       choice --> (1) ACO operation (2) putting in global queue   and pos --> 0 for the ACO operation and different values for putting 
                     in global_q   
        Output:      none

        '''
        global global_queue
        global rlock
        global noOfTasks

        rlock.acquire()
        try:
            if(choice == 1):
                flag = False
                while(global_queue.qsize() != 0):
                    flag = True
                    ACO_list.append(global_queue.get())
                if(flag == True):
                    self.__resetVMs()
                    self.__resetHosts()
                    self.__ACOScheduler()
            if(choice == 2):
                if(self.dependencyMatrix[pos] == 0):
                    global_queue.put(pos)
        finally:
            rlock.release()

    def __ACOSchedulerUtil(self):
        while(noOfTasks < self.DAG_matrix.DAGRows):
            self.__synchronizedQueue(1,0)
            time.sleep(2)
