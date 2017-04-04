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

global no_Of_Ants
noOfAnts = 15

global iterations
iterations = 10

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
        Output:      none
        
        '''
        print "Initializing parameters......."
        
        global DAG_row
        global DAG_column
        global p_row_task
        global p_column_task
        global p_row_VM
        global p_column_VM
        global noOfVMs
        
        DAG_row = len(self.DAG_matrix.DAGRows)
        DAG_column = len(self.DAG_matrix.DAGColumns)
        noOfVMs = len(len(self.vmList))
        p_row_task = DAG_row
        p_column_task = DAG_column
        p_row_VM = noOfVMs
        p_column_VM = noOfVMs

        graph_vm_mapping=[[1 for i in range(DAG_row)] for j in range(noOfVMs) ]

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
        
        cloudletSchedulerUtil.normalize(SLAV_delta_tau_global_list)
        min_SLAV_delta_tau = min(SLAV_delta_tau_global_list)
        index = SLAV_delta_tau_global_list.index(min_SLAV_delta_tau)
        
        ant_allocation_list = ants_allocation_list[index]
        
        temp_len = len(ant_allocation_list)
        for i in range(temp_len):
            task = ant_allocation_list[i].task
            VM = ant_allocation_list[i].assigned_VM
            pheromone_VM_level[task][VM] = (1 - rho_VM) * pheromone_VM_level[task][VM] + rho_VM * (1 - min_SLAV_delta_tau)

    def __roulette_wheel(self,probability_list,limit):
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
    
    def ACO(self):
        '''
        Function:    Applies ACO on the independent tasks that are present in the ACO_list
        Input:       DAG, ACO_list, 
        Output:      A list of the ants solution for all the iterations

        '''
        
        print "Executing ACO"
        print "ACO_LIST",ACO_list

        global num_of_Ants
        global iterations
        
     
        self.__initialize_pheromone();
        
        global total_time
        #global MI_temp
        #global storage_temp
        #global deadline_temp
        #global VM_temp
        #global dependencies
        #del MI_temp [:]
        #del storage_temp [:]
        #del deadline_temp [:]
        
        
        secondary_temp_ACO_list=[]
        
        for i in range(len(MI)):
            MI_temp.append(MI[i])

        for i in range(len(storage)):
            storage_temp.append(storage[i])

        for i in range(len(deadline)):
            deadline_temp.append(deadline[i])

        

        temp_ACO_list=[]

        iterations_allocation_list = []                            # This list stores the allocations for all the iterations
        SLAV_delta_tau_global_lists=[]
        for it in range(iterations): 
            ants_allocation_list = []                              # This list stores the allocation for all the ants
            SLAV_delta_tau_global_list = []
            for nA in range(num_of_Ants):
                ACO_list_len=len(ACO_list)
                count = ACO_list_len - 1
                ant_allocation_list = []                           # This list stores the allocation for the ant

                for i in range(ACO_list_len):
                    temp_ACO_list.append(ACO_list[i])

                #del VM_temp [:]
                #for i in range(VM_row):
                #    VM_temp.append([ VM[i][0] * VM[i][1], VM[i][2] ])    
                # below parameters are for global pheromone update------------------------------------------------------------------------------

                SLAV_MI_global_list = []
                SLAV_storage_global_list = []
                SLAV_deadline_global_list = []
                MI_required_global_list = []
                storage_required_global_list = []
                deadline_required_global_list = []
                
                temp_ACO_list = select_task(temp_ACO_list)
                ant_position = ACO_list_len-1
                
                for ant_position in range(ant_position,-1,-1):
                    
                    #ant_position = random.randint( 0,count)    #old random task selection implementation

                    storage_violation_list = []
                    MI_violation_list = []
                    deadline_violation_list = []

                    min_MI_violation = sys.float_info.max

                    min_storage_violation = sys.float_info.max
                    min_deadline_violation = sys.float_info.max
                    max_MI_violation = sys.float_info.min
                    max_storage_violation = sys.float_info.min
                    max_deadline_violation = sys.float_info.min
                    
                    VM_outof_resources=[]

                    for t in range(noOfVMs):
                        if(self.vmList[t].currentAvailableMips <= 0 or self.vmList[t].currentAvailableStorage <= 0):
                            VM_outof_resources.append(t)

                    for vm in self.vmList:
                        temp_MI_violation = float(self.workflow.taskDict.get(temp_ACO_list[ant_position]).MI - vm.currentAvailableMips)
                        temp_storage_violation = float(self.workflow.taskDict.get(temp_ACO_list[ant_position]).storage - vm.currentAvailableStorage)
                        try:
                            temp_deadline_violation = float(self.workflow.taskDict.get(temp_ACO_list[ant_position]).runtime - self.workflow.taskDict.get(temp_ACO_list[ant_position]).MI / vm.currentAvailableMips)
                        except ZeroDivisionError:
                            temp_deadline_violation = sys.float_info.max
        
                        MI_violation_list.append( temp_MI_violation )
                        storage_violation_list.append( temp_storage_violation )
                        deadline_violation_list.append( temp_deadline_violation )

                    #Heuristic information calculation--------------------------------------------------------------------------------------------
                    
                    length_1 = len(MI_violation_list)                
                    
                    cloudletSchedulerUtil.normalize(MI_violation_list)
                    cloudletSchedulerUtil.normalize(storage_violation_list)
                    cloudletSchedulerUtil.normalize(deadline_violation_list)
                    
                    eta_list = []                                       # list of the eta for all the edges from one task to all VMs
                    W_MI = 0.2                                          # weightage for MI
                    W_storage = 0.1                                     # weightage for storage
                    W_deadline = 0.4                                    # weightage for deadline
                    
                    for i in range(length_1):    
                        #Q = random.randint(0,9)
                        Q = random.uniform(0,1)                      # random value
                        #eta_list.append( Q *( MI_violation_final_list[i] * W_MI  +  storage_violation_final_list[i] * W_storage  +  deadline_violation_final_list[i] * W_deadline ) )
                        eta_list.append( ( MI_violation_list[i] * W_MI  +  storage_violation_list[i] * W_storage  +  deadline_violation_list[i] * W_deadline ) )
                                    
                    #Normalize eta values---------------------------------------------------------------------------------------------------------
                    
                    #normalize(eta_list)
                    max_eta = eta_list[0]
                    min_eta = eta_list[0]
            
                    for i in range(1,length_1):
                        if(max_eta < eta_list[i]):
                            max_eta = eta_list[i]
                        if(min_eta > eta_list[i]):
                            min_eta = eta_list[i]

                    for i in range(length_1):
                        try:
                            eta_list[i] = (eta_list[i] - min_eta) / (max_eta - min_eta)
                            if(eta_list[i]==0):
                                eta_list[i]=0.1
                        except ZeroDivisionError:
                            eta_list[i] = 1
                    #-----------------------------------------------------------------------------------------------------------------------------

                    #Heuristic information calculation--------------------------------------------------------------------------------------------

                    alpha_pheromone = 0.3                 # weightage for the pheromone
                    beta_eta = 0.4                        # weightage for the eta(heuristic information) 
                    alpha_pheromone_mult_beta_eta = 0
                    for i in range(p_column_VM):    
                        alpha_pheromone_mult_beta_eta = alpha_pheromone_mult_beta_eta + ( pheromone_VM_level[temp_ACO_list[ant_position]][i] ** alpha_pheromone ) * (1 - ( eta_list[i] ** beta_eta ) )
                    
                    #----------------------------------------------------------------------------------------------------------------------------
                    
                    #probability calculation for edge selection----------------------------------------------------------------------------------

                    probability_of_selection_list=[]
                    for i in range(p_column_VM):
                        try:
                            probability_of_selection_list.append( ( ( pheromone_VM_level[temp_ACO_list[ant_position]][i] ** alpha_pheromone ) * ( 1-((eta_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
                        except ZeroDivisionError as err:
                            probability_of_selection_list.append(1)
                    

                    largest_probability_index = 0
                    largest_probability = 0
                    
                    index = self.__roulette_wheel(probability_of_selection_list, 1.0)
                    
                    if(index not in VM_outof_resources):
                        largest_probability_index = index
                        largest_probability = probability_of_selection_list[index]
                    
                    if(largest_probability==0 and largest_probability_index==0):
                        secondary_temp_ACO_list.append(temp_ACO_list[ant_position])
                        
                        for p in range(len(ACO_list)):
                            if(ACO_list[p]==temp_ACO_list[ant_position]):
                                break
                        del ACO_list[p]
                        del temp_ACO_list[ant_position]
                        continue
                    #--------------------------------------------------------------------------------------------------------------------------
                    
                    
                    # Calculations for Global pheromone update---------------------------------------------------------------------------------
                    SLA_MI_global = float(MI[temp_ACO_list[ant_position]] - VM_temp[largest_probability_index][0])
                    
                    if(SLA_MI_global < 0):
                        SLA_MI_global=0
                    
                    SLA_storage_global = float(storage[temp_ACO_list[ant_position]] - VM_temp[largest_probability_index][1])
                    
                    if(SLA_storage_global < 0):
                        SLA_storage_global=0
                    
                    try:
                        SLA_deadline_global = float(deadline[temp_ACO_list[ant_position]] - MI[temp_ACO_list[ant_position]] / VM_temp[largest_probability_index][0])
                    except ZeroDivisionError:
                        SLA_deadline_global = sys.float_info.max
                    
                    if(SLA_deadline_global<0):
                        SLA_deadline_global=0
                    
                    MI_required_global_list.append(float(MI[temp_ACO_list[ant_position]]))
                    storage_required_global_list.append(float(storage[temp_ACO_list[ant_position]]))
                    deadline_required_global_list.append(float(deadline[temp_ACO_list[ant_position]]))
                    SLAV_MI_global_list.append(SLA_MI_global)
                    SLAV_storage_global_list.append(SLA_storage_global)
                    SLAV_deadline_global_list.append(SLA_deadline_global)
                    
                    #------------------------------------------------------------------------------------------------------------------------
                            
                    ant_allocation = Allocation(temp_ACO_list[ant_position],largest_probability_index)
                    ant_allocation_list.append(ant_allocation)                  # puting this allocation in the list
                    count = count-1                                             # decrement the ACO list count

                    #updating the VM capacity (storage)-------------------------------------------------------------------------------------
                    new_storage = VM_temp[largest_probability_index][1] - storage[temp_ACO_list[ant_position]]
                    if(new_storage <= 0):
                        VM_temp[largest_probability_index][1] = 0
                    else:
                        VM_temp[largest_probability_index][1] = new_storage

                    #updating the VM capacity ( computing power )---------------------------------------------------------------------------

                    total_computing_power_before = VM_temp[i][0]
                    new_computing_power_after = total_computing_power_before - MI[temp_ACO_list[ant_position]]
                    if(new_computing_power_after<=0):
                        VM_temp[largest_probability_index][0]
                    else:
                        VM_temp[largest_probability_index][0] = new_computing_power_after
                    
                    #local pheromone update-------------------------------------------------------------------------------------------------
                    
                    local_pheromone_update_VM_level(temp_ACO_list[ant_position],largest_probability_index)
                    local_pheromone_update_task_level(temp_ACO_list[ant_position])
                    #-----------------------------------------------------------------------------------------------------------------------
                    
                    del temp_ACO_list[ant_position]
                
                #global pheromone calculation-----------------------------------------------------------------------------------------------
                temp_SLAV_len = len(SLAV_MI_global_list)
                SLAV_storage_global = 0.0
                SLAV_MI_global = 0.0
                SLAV_deadline_global = 0.0
                temp_SLAV_MI_global_required = 0.0
                temp_SLAV_storage_global_required = 0.0
                temp_SLAV_deadline_global_required = 0.0
                
                cloudletSchedulerUtil.normalize(SLAV_storage_global_list)
                cloudletSchedulerUtil.normalize(SLAV_MI_global_list)
                cloudletSchedulerUtil.normalize(SLAV_deadline_global_list)
                cloudletSchedulerUtil.normalize(MI_required_global_list)
                cloudletSchedulerUtil.normalize(storage_required_global_list)
                cloudletSchedulerUtil.normalize(deadline_required_global_list)
                
                for i in range(temp_SLAV_len):
                    SLAV_storage_global = SLAV_storage_global + SLAV_storage_global_list[i]
                    SLAV_MI_global = SLAV_MI_global + SLAV_MI_global_list[i]
                    SLAV_deadline_global = SLAV_deadline_global + SLAV_deadline_global_list[i]
                    temp_SLAV_MI_global_required = temp_SLAV_MI_global_required + MI_required_global_list[i]
                    temp_SLAV_storage_global_required = temp_SLAV_storage_global_required + storage_required_global_list[i]
                    temp_SLAV_deadline_global_required = temp_SLAV_deadline_global_required + deadline_required_global_list[i]
                
                W_MI_global = 0.2
                W_deadline_global = 0.2
                W_storage_global = 0.2
                #delta_tau_SLAV larger the value larger is the SLA violation
                try:
                    delta_tau_SLAV = ( ( SLAV_MI_global / temp_SLAV_MI_global_required ) * W_MI_global ) 
                except ZeroDivisionError:
                    delta_tau_SLAV = sys.float_info.max

                try:                
                    delta_tau_SLAV = delta_tau_SLAV + ( ( SLAV_storage_global / temp_SLAV_storage_global_required ) * W_storage_global )
                except ZeroDivisionError:
                    delta_tau_SLAV =sys.float_info.max
                    
                try:
                    delta_tau_SLAV = delta_tau_SLAV + ( ( SLAV_deadline_global / temp_SLAV_deadline_global_required ) * W_deadline_global )
                except ZeroDivisionError:
                    delta_tau_SLAV =sys.float_info.max
                
                SLAV_delta_tau_global_list.append(delta_tau_SLAV)
                printf("delta_tau_SLAV"+"\t"+str(delta_tau_SLAV))
                printf("----------------------------------------------")
                #performing evaporation on VM-task graph------------------------------------------------------------------------------------
                evaporation_VM_level()
                
                ants_allocation_list.append(ant_allocation_list)
                
                #printing ant allocation list
                print_allocations(ant_allocation_list,it,nA)
                
            #performing global pheromone update---------------------------------------------------------------------------------------------
            global_update_pheromone_VM_level(SLAV_delta_tau_global_list,ants_allocation_list)
            global_update_pheromone_task_level(SLAV_delta_tau_global_list,ants_allocation_list)
            SLAV_delta_tau_global_lists.append(SLAV_delta_tau_global_list)
            iterations_allocation_list.append(ants_allocation_list)


        #time calculations------------------------------------------------------------------------------------------------------------------
        len_SLAV_lists = len(SLAV_delta_tau_global_lists)
        len_SLAV_list = len(SLAV_delta_tau_global_lists[0])
        min_SLAV_delta_tau = SLAV_delta_tau_global_lists[0][0]
        min_SLAV_delta_tau_index_i = 0
        min_SLAV_delta_tau_index_j = 0
        for i in range(len_SLAV_lists):
            for j in range(len_SLAV_list):
                if(min_SLAV_delta_tau > SLAV_delta_tau_global_lists[i][j]):
                    min_SLAV_delta_tau = SLAV_delta_tau_global_lists[i][j]
                    min_SLAV_delta_tau_index_i = i
                    min_SLAV_delta_tau_index_j = j

        #time_taken=[]

        total_length = len(ACO_list)
        final_ants_allocation_list = iterations_allocation_list[min_SLAV_delta_tau_index_i]
        final_ant_allocation_list = final_ants_allocation_list[min_SLAV_delta_tau_index_j] 
        #max_time_taken=0
        del VM_temp [:]
        for i in range(VM_row):
            VM_temp.append([ VM[i][0] * VM[i][1], VM[i][2] ])
            

        #total_MI_for_VM=[]
        VM_list_a={}
        for i in range(0,total_length):
            if(VM_list_a.has_key(final_ant_allocation_list[i].assigned_VM)):
                VM_list_a[final_ant_allocation_list[i].assigned_VM] = VM_list_a.get(final_ant_allocation_list[i].assigned_VM) + MI[final_ant_allocation_list[i].task]
            else:
                VM_list_a[final_ant_allocation_list[i].assigned_VM] = MI[final_ant_allocation_list[i].task]
        
        time_temp = 0   
        
        for k,v in VM_list_a.items():
            try:
                time_temp = time_temp + v / VM_temp[k][0]
            except ZeroDivisionError as err:
                time_temp = sys.float_info.max
        '''            
        for i in range(0,total_length):
            try:
                time_temp = MI[final_ant_allocation_list[i].task] / VM_temp[final_ant_allocation_list[i].assigned_VM][0]
            except ZeroDivisionError as err:
                time_temp = sys.float_info.max

            temp_MI = VM_temp[final_ant_allocation_list[i].assigned_VM][0] - MI[final_ant_allocation_list[i].task]

            if(temp_MI <= 0):
                VM_temp[final_ant_allocation_list[i].assigned_VM][0] = 0
            else:
                VM_temp[final_ant_allocation_list[i].assigned_VM][0] = temp_MI

            time_taken.append(time_temp)

            if(time_temp > max_time_taken):
                max_time_taken = time_temp
        '''
        total_time = total_time + time_temp
        print "total_time:",total_time
        printf("total_time::"+str(total_time))
        printf("min_SLAV_delta_tau::"+str(min_SLAV_delta_tau))
        min_delta_SLAV_list.append(min_SLAV_delta_tau)
        print "----------------------------------------------------------------------------------------------------------"

        # Clearing the dependencies----------------------------------------------------------------------------------------------------------
        for i in range(len(ACO_list)):
            for j in range(DAG_column):
                if(DAG[j][ACO_list[i]]==1):
                    dependencies[j]=dependencies[j]-1
                    if(dependencies[j]==0):
                        synchronized_queue(2, j)

        # reset ACO_List
        del ACO_list[:]
        printf("total_time"+str(total_time))
        sum=0
        total_required_time=0
        for i in range(len(deadline)):
            total_required_time=total_required_time+deadline[i]
            
        print "total_required_time",total_required_time
        
        for i in range(len(min_delta_SLAV_list)):
            sum=sum + min_delta_SLAV_list[i]
        average_SLAV_delta_tau=sum/len(min_delta_SLAV_list)
        print "average_SLAV_delta_tau",average_SLAV_delta_tau
        printf("-----------------------------------------------------------------------------------------------------------")
        if(len(secondary_temp_ACO_list)!=0):
            for d in range(len(secondary_temp_ACO_list)):
                ACO_list.append(secondary_temp_ACO_list[d])
            del secondary_temp_ACO_list[:]
            ACO()


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
                    ACO_list.append(global_queue.get())
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
