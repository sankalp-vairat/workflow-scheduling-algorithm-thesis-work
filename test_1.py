'''
Created on 02-Feb-2017
@author: Sankalp Vairat

'''


import random
#import scipy as sp
import sys
import copy
import math
#import matplotlib.pyplot as plt
#import networkx as nx;
#import numpy as np
#import Task
#import VM
#import Ant
from collections import deque
from threading import Thread
import time
import sys
from Allocation import Allocation
#from queue import *
from multiprocessing import Queue
import threading
from generator import *
from multiprocessing.sharedctypes import _new_value
#import randlevel

#----------------------------------------DECLARE GLOBAL VARIABLES------------------------------------------------
global visited

global tasks

global tasks_temp
tasks_temp=[]

global task_dependency
task_dependency = []

global visited_tasks
visited_tasks = []

#global DAG                              #DAG indicates dependency and precedence between the tasks

global VM                               #Column represents 1->Processing Units 2->Computing Power per PE 3->Storage available per VM

global VM_temp                          #After every travel of ant k we will have temp allocation for the VM
VM_temp = []                        

global graph_vm_mapping                 #graph_vm_mapping indicates the edges between VMs available and the tasks.
graph_vm_mapping=[]

global MI                               #millions instructions for each task

global storage                          #storage required for each task

global deadline                         #time in which task to be completed

global MI_temp                          #millions instructions for each task
MI_temp = []                        

global storage_temp                     #storage required for each task
storage_temp = []

global deadline_temp                    #time in which task to be completed
deadline_temp = []

global pheromone_task_level             #pheromone matrix task level
pheromone_task_level = []

global pheromone_VM_level               #pheromone matrix VM level
pheromone_VM_level = []

global tau_0_task                       #Initial pheromone value task level
tau_0_task = 0

global tau_0_VM                         #Initial pheromone value VM level
tau_0_VM = 0

global rho_task                         #pheromone evaporation rate task level
rho_task = 0

global rho_VM                           #pheromone evaporation rate VM level
rho_VM = 0

global delta_tau_0_task                 #best value for the fitness function task level
delta_tau_0_task = 0

global delta_tau_0_VM                   #best value for the fitness function VM level
delta_tau_0_VM = 0

global SLAV_MIPS                        #SLA violation parameter for MIPS
SLAV_MIPS = 0

global SLAV_storage                     #SLA violation parameter for storage
SLAV_storage = 0

global SLAV_deadline                    #SLA violation parameter for deadline
SLAV_deadline = 0

global W_SLA_MIPS                       #importance paramter for SLA MIPS
W_SLA_MIPS = 0

global W_SLA_storage                    #importance paramter for SLA storage
W_SLA_storage = 0

global W_SLA_deadline                   #importance paramter for SLA deadline
W_SLA_deadline = 0

global eta_task_level                   #heuristic informatio for task level
eta_task_level = 0

global eta_VM_level                     #heuristic informatio for VM level
eta_VM_level = 0

global best_tour_iteration_task         #list of tasks in the best tour . Initially it will be empty.
best_tour_iteration_task = []

global best_tour_iteration_VM           #list of allocation in the best tour . Initially it will be empty.
best_tour_iteration_VM = []

global ant_tour_task
ant_tour_task = []                      #list of tasks in the tour of ant k. Initially it will be empty.

global ant_tour_VM                      #list of allocations in the tour of ant k. Initially it will be empty.
ant_tour_VM = []

global rlock                            #rentrant lock for the synchronized method
rlock = threading.RLock()

global total_time                       #total time taken for the execution of the DAG
total_time = 0

global dependencies                     #dependencies of every task is stored in this.
dependencies = []

global global_q                         #Global queueu which will be accessed by all threads 
global_q = Queue()

global ACO_list                         #this is used to stores the temporary list of independent tasks from the global_q
ACO_list=[]


#-----------------------------------------------------------------------------------------------------------------------------------


#------------------------------------INITIALIZE VARIABLES---------------------------------------------------------------------------
'''
DAG=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,1,0,1,0,0,0,0,0,0,0,0,0,0],
     [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
     [0,0,0,1,0,0,1,1,1,1,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]]
'''

VM=[[8,10000,1024],
    [8,10000,2048],
    [4,10000,800],
    [6,8000,1024],
    [7,5000,2048],
    [1,10000,4096]]     

'''
MI=[100000,40000,100000,300000,60000,40000,200000,400000,100000,300000,60000,600000,40000,400000,100000]

storage=[100,200,300,300,400,100,800,900,300,600,500,700,300,1024,1024]

deadline=[120,1,1,1,1,10,180,180,120,120,1,180,10,180,180]

'''

tau_0_task=0.2

tau_0_VM=0.2

rho_task=0.2

rho_VM=0.2

W_SLA_MIPS=0.3

W_SLA_storage=0.4

W_SLA_deadline=0.5


#---------------------------------------------------------------------------------------------------------------------------------


    

def initialize_parameters():
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


    
def set_task_VM_parameters():
    '''
    Function:     Sets the task and VM parameters after each travel of ant k
    Input:        temporary list of the MI, storage, deadline and VM  
    Output:       none
    (SIDE)Effects:the values of the all the temporary list will be reset.
    
    '''
    for i in range(MI):
        MI_temp[i]=MI[i]

    for i in range(storage):
        storage_temp[i]=storage[i]

    for i in range(deadline):
        deadline_temp[i]=deadline[i]

    for i in range(VM_row):
        VM_temp[i][0]=VM[i][0] * VM[i][1]
        VM_temp[i][1]=VM[i][2]



def find_starting_vertices():
    '''
    Function:  find the starting tasks in the DAG
    Input:     Adjecency matrix representation of DAG
    Output:    List of tasks that are starting point of DAG

    '''
    print "finding starting tasks in dependency graph......."
    
    global starting_vertices
    starting_vertices=[];
    for i in range(DAG_row):
        start_v=True
        for j in range(DAG_column):
            if(DAG[i][j]==1):
                start_v=False
                continue;
        if(start_v==True):
            starting_vertices.append(i)

            

def initialize_pheromone():
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
     
    
def evaporation_task_level():
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


def evaporation_VM_level():
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


def local_pheromone_update_task_level(i):
    '''
    FUNCTION:      reinforces the last visited edge by ant k at task level
    INPUT:         pheromone matrix of task level, phi, tau_0_task
    OUTPUT:        none
    (SIDE)EFFECTS: pheromone value is updated on the edge (i,j)
    
    '''         
    print "performing local pheromone update at task level................."
    
    phi=0.2                                                                         #decay coefficient
    pheromone_task_level[i]=(1-phi)*pheromone_task_level[i]+phi*tau_0_task


def local_pheromone_update_VM_level(i,j):
    '''
    FUNCTION:      reinforces the last visited edge by ant k at VM level
    INPUT:         pheromone matrix of VM level, phi, tau_0_VM
    OUTPUT:        none
    (SIDE)EFFECTS: pheromone value is updated on the edge (i,j)
    
    '''
    
    print "performing local pheromone update at VM level................."
                 
    phi=0.2                                                                         #decay coefficient
    pheromone_VM_level[i][j]=(1-phi)*pheromone_VM_level[i][j]+phi*tau_0_VM


def global_update_pheromone_task_level(SLAV_delta_tau_global_list,ants_allocation_list):
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


def global_update_pheromone_VM_level(SLAV_delta_tau_global_list,ants_allocation_list):
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

    
def probability_for_task():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    print "Calculating probability for selection of path................."


    
def probability_for_VM():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    
    print "Calculating probability for selection of path................."    



    
def SLA_violation_for_MIPS():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''   
    sum_of_diff = 0
    sum_of_reqd = 0
    for i in range(len(MI_temp)):
        sum_of_diff=sum_of_diff+MI_temp[i]
        sum_of_reqd=sum_of_reqd+MI[i]

    SLAV_MIPS = sum_of_diff / sum_of_reqd



def SLA_violation_for_Storage():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    sum_of_diff = 0
    sum_of_reqd = 0
    for i in range(len(storage_temp)):
        sum_of_diff=sum_of_diff+storage_temp[i]
        sum_of_reqd=sum_of_reqd+storage[i]

    SLAV_storage = sum_of_diff / sum_of_reqd        



def SLA_violation_for_Deadline():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    sum_of_diff = 0
    sum_of_reqd = 0
    for i in range(len(deadline_temp)):
        sum_of_diff=sum_of_diff+deadline_temp[i]
        sum_of_reqd=sum_of_reqd+deadline[i]

    SLAV_deadline = sum_of_diff / sum_of_reqd




def SLA_Violation_calculation():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''

    print "Calculating SLA violation................."

    SLA_violation_for_MIPS();
    SLA_violation_for_Storage();
    SLA_violation_for_Deadline();


def SLA_violation_for_MIPS_VM():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    sum_of_diff = 0
    sum_of_reqd = 0
    for i in range(len(MI_temp)):
        sum_of_diff=sum_of_diff+MI_temp[i]
        sum_of_reqd=sum_of_reqd+MI[i]

    SLAV_MIPS = sum_of_diff / sum_of_reqd



def SLA_violation_for_Storage_VM():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''    
    sum_of_diff = 0
    sum_of_reqd = 0
    for i in range(len(storage_temp)):
        sum_of_diff=sum_of_diff+storage_temp[i]
        sum_of_reqd=sum_of_reqd+storage[i]

    SLAV_storage = sum_of_diff / sum_of_reqd        



def SLA_violation_for_Deadline_VM():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    sum_of_diff = 0
    sum_of_reqd = 0
    for i in range(len(deadline_temp)):
        sum_of_diff=sum_of_diff+deadline_temp[i]
        sum_of_reqd=sum_of_reqd+deadline[i]

    SLAV_deadline = sum_of_diff / sum_of_reqd




def SLA_Violation_calculation_VM():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''

    print "Calculating SLA violation................."

    SLA_violation_for_MIPS_VM();
    SLA_violation_for_Storage_VM();
    SLA_violation_for_Deadline_VM();



def calculation_of_heuristic_info_eta_task():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    
    print "calculating heuristic info eta task"
    
def calculation_of_heuristic_info_eta_VM():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    
    print "calculating heuristic info eta VM"
  

  
def check_dependency(pos):
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    for i in range(DAG_row):
        if(DAG[pos][i] == 1 and visited[i] == 0):
            return False;
    return True;



def get_feasible_tasks(position):
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    feasible_tasks=[]
    for l in range(DAG_column):
        if(visited_tasks[l] == 0 and DAG[l][position] == 1 and check_dependency(l) == True):
            feasible_tasks.append(l)


#------------------------------------TOPOLOGICAL ORDERING OF DAG-------------------------------------


def initialize_parameters_for_topo_sort():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''

    global t_DAG
    t_DAG = [[0 for i in range(DAG_row)] for j in range(DAG_column)]

    global t_visited
    t_visited = [0 for i in range(DAG_row)]

    global topological_order
    topological_order = []

    global t_queue
    t_queue = deque([])


def find_task_without_dependency():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''

    for i in range(DAG_row):
        if(t_visited[i] == 1):
            continue
        else:
            flag = True
            for j in range(DAG_column):
                if(t_DAG[i][j] == 1):
                    flag = False
                    break
            if(flag == True and t_visited[i] == 0):
                topological_order.append(i)
                t_queue.append(i)
                t_visited[i] = 1


def topological_ordering_util():
    '''
    FUNCTION:      
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''

    for i in range(DAG_row):
        for j in range(DAG_column):
            t_DAG[i][j]=DAG[i][j]

    find_task_without_dependency()
    while(len(t_queue) != 0):
        pos=t_queue.popleft()
        for k in range(DAG_column):
            t_DAG[k][pos]=0
        find_task_without_dependency()

#-------------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------PRINT UTILITY FUNCTIONS-----------------------------------------------------------------------
def printf(str):
    '''
    FUNCTION:      This function prints output to a file
    INPUT:         
    OUTPUT:        
    (SIDE)EFFECTS: 
    
    '''
    f= open("Output.txt","a+")
    f.write(str)
    f.write("\n")
    f.close()

def printf_1D_list(list_1D):
    '''
    FUNCTION:      This function prints 1D list
    INPUT:         1D list
    OUTPUT:        1D list
    (SIDE)EFFECTS: 
    
    '''
    f= open("Output.txt","a+")
    for i in range(len(list_1D)): 
        f.write(str(list_1D[i])+" ")
    f.write("\n")
    f.write("----------------------------------------------------")
    f.write("\n")
    f.close()

def printf_2D_list(list_2D):
    '''
    FUNCTION:      This function prints 1D list
    INPUT:         2D list
    OUTPUT:        2D list
    (SIDE)EFFECTS: 
    
    '''
    f= open("Output.txt","a+")
    for i in range(len(list_2D)):
        for j in range(len(list_2D[0])):
            f.write(str(list_2D[i])+" ")
        f.write("\n")
    f.write("----------------------------------------------------")
    f.write("\n")
    f.close()

def print_1D_list(list_1D):
    '''
    FUNCTION:      This function prints 1D list
    INPUT:         1D list
    OUTPUT:        1D list
    (SIDE)EFFECTS: 
    
    '''

    for i in range(len(list_1D)):
        print list_1D[i],
    print ""

def print_2D_list(list_2D):
    '''
    FUNCTION:      This function prints 1D list
    INPUT:         2D list
    OUTPUT:        2D list
    (SIDE)EFFECTS: 
    
    '''

    for i in range(len(list_2D)):
        for j in range(len(list_2D[0])):
            print list_2D[i][j],
    print ""

def print_allocations(ant_allocation_list,iteration,ant):
    '''
    FUNCTION:      This function prints 1D list
    INPUT:         2D list
    OUTPUT:        2D list
    (SIDE)EFFECTS: 
    
    ''' 
    
    temp_len=len(ant_allocation_list)
    
    printf("Iteration::"+str(iteration)+"\t"+"Ant::"+str(ant))
    for i in range(temp_len):
        task = ant_allocation_list[i].task
        VM = ant_allocation_list[i].assigned_VM
        printf("Task:: "+str(task)+"\t"+"VM:: "+str(VM))

#-------------------------------------------------------------------------------------------------------------------------------------



def find_dependencies():
    '''
    Function:    finds the dependencies count for each task in the DAG
    Input:       Adjecency matrix representation of DAG
    Output:      List of tasks that are starting point of DAG (dependencies)

    '''
    print "finding dependencies count for each task ......."
    
    for i in range(DAG_row):
        count=0
        for j in range(DAG_column):
            if(DAG[i][j]==1):
                count=count+1
        dependencies.append(count)

def merge(probability_list,temp_ACO_list,l,m,r):
    '''
    Function:    Utility merge function for merge sort
    Input:       
    Output:      

    '''
    n1 = m - l +1
    n2 = r - m
    
    L = [0] * (n1)
    R = [0] * (n2)
    
    L_temp = [0] * (n1)
    R_temp = [0] * (n2)

    for i in range(0 , n1):
        L[i] = probability_list[l + i]
        L_temp[i] = temp_ACO_list[l + i]
 
    for j in range(0 , n2):
        R[j] = probability_list[m + 1 + j]
        R_temp[j] = temp_ACO_list[m + 1 + j]
 
    i = 0
    j = 0
    k = l    

    while i < n1 and j < n2 :
        if L[i] <= R[j]:
            probability_list[k] = L[i]
            temp_ACO_list[k] = L_temp[i]
            i += 1
        else:
            probability_list[k] = R[j]
            temp_ACO_list[k] = R_temp[j]
            j += 1
        k += 1
 
    while i < n1:
        probability_list[k] = L[i]
        temp_ACO_list[k] = L_temp[i]
        i += 1
        k += 1

    while j < n2:
        probability_list[k] = R[j]
        temp_ACO_list[k] = R_temp[j]
        j += 1
        k += 1


def merge_sort(probability_list,temp_ACO_list,l,r):
    '''
    Function:    Sorts the ACO list with the probability values
    Input:       
    Output:      

    '''
    if(l<r):
        m = (l+(r-1)) / 2
        
        merge_sort(probability_list, temp_ACO_list, l, m)
        merge_sort(probability_list, temp_ACO_list, m+1, r)
        merge(probability_list,temp_ACO_list,l,m,r)



def roulette_wheel(probability_list,limit):
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


def normalize(list):
    '''
    Function:    Normalizes the list values using min-max scalar
    Input:       
    Output:      

    '''
    length_list = len(list)
    max = list[0]
    min = list[0]
                
    for i in range(1,length_list):
        if(max < list[i]):
            max = list[i]
        if(min > list[i]):
            min = list[i]

    for i in range(length_list):
        try:
            list[i] = (list[i] - min) / (max - min)
            #if(eta_list[i]==0):
            #eta_list[i]=0.1
        except ZeroDivisionError:
            if(max==0 and min==0):
                list[i]=0
            else:
                list[i] = 1
        

def select_task(temp_ACO_list):
    '''
    Function:    Applies ACO on the independent tasks that are present in the ACO_list
    Input:       DAG, ACO_list, 
    Output:      A list of the ants solution for all the iterations

    '''
    
    print "Selecting task......................................"    
    
    temp_len = len(temp_ACO_list)
    temp_MI_list = []
    temp_storage_list = []
    temp_deadline_list = []
    for i in range(temp_len):
        temp_MI_list.append(float(MI[temp_ACO_list[i]]))
        temp_storage_list.append(float(storage[temp_ACO_list[i]]))
        temp_deadline_list.append(float(deadline[temp_ACO_list[i]]))
    
    min_MI = temp_MI_list[0]
    max_MI = temp_MI_list[0]
    min_storage = temp_storage_list[0]
    max_storage = temp_storage_list[0]
    min_deadline = temp_deadline_list[0]
    max_deadline = temp_deadline_list[0]
    
    for i in range(1,temp_len):
        
        if(temp_MI_list[i] > max_MI):
            max_MI = temp_MI_list[i]
        
        if(temp_MI_list[i] < min_MI):
            min_MI = temp_MI_list[i]
            
        if(temp_storage_list[i] > max_storage):
            max_storage = temp_storage_list[i]
        
        if(temp_storage_list[i] < min_storage):
            min_storage = temp_storage_list[i]
            
        if(temp_deadline_list[i] > max_deadline):
            max_deadline = temp_deadline_list[i]
        
        if(temp_deadline_list[i] < min_deadline):
            min_deadline = temp_deadline_list[i]
        
    lambda_Mi_list = []
    lambda_storage_list = []
    lambda_deadline_list = []
    
    for i in range(temp_len):
        
        try:
            lambda_Mi_list.append((temp_MI_list[i] - min_MI) / (max_MI - min_MI ))
        except ZeroDivisionError:
            lambda_Mi_list.append(sys.float_info.max)
        
        try:
            lambda_storage_list.append((temp_storage_list[i] - min_storage) / (max_storage - min_storage ))
        except ZeroDivisionError:
            lambda_storage_list.append(sys.float_info.max)
            
        try:
            lambda_deadline_list.append((temp_deadline_list[i] - min_deadline) / (max_deadline - min_deadline ))
        except ZeroDivisionError:
            lambda_deadline_list.append(sys.float_info.max)
    
    normalize(lambda_Mi_list)     
    normalize(lambda_storage_list)
    normalize(lambda_deadline_list)
       
    eta_task_list=[]
    W_MI = 0.2                                          # weightage for MI
    W_storage = 0.1                                     # weightage for storage
    W_deadline = 0.4                                    # weightage for deadline
        
    for i in range(temp_len):    
        #Q = random.randint(0,9)
        Q = random.uniform(0,1)                      # random value
        eta_task_list.append (  (lambda_Mi_list[i] * W_MI  +  lambda_storage_list[i] * W_storage  +  lambda_deadline_list[i] * W_deadline ))
        
    max_eta = eta_task_list[0]
    min_eta = eta_task_list[0]
        
    for i in range(1,temp_len):
        if(max_eta < eta_task_list[i]):
            max_eta = eta_task_list[i]
        if(min_eta > eta_task_list[i]):
            min_eta = eta_task_list[i]

    for i in range(temp_len):
        try:
            eta_task_list[i] = (eta_task_list[i] - min_eta) / (max_eta - min_eta)
            if(eta_task_list[i]==0):
                eta_task_list[i]=0.1
        except ZeroDivisionError:
            eta_task_list[i] = 1

    #Heuristic information calculation--------------------------------------------------------------------------------------------
                
    alpha_pheromone = 0.3                 # weightage for the pheromone
    beta_eta = 0.4                        # weightage for the eta(heuristic information) 
    alpha_pheromone_mult_beta_eta = 0
        
    for i in range(temp_len):    
        alpha_pheromone_mult_beta_eta = alpha_pheromone_mult_beta_eta + (pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * (1 - ( eta_task_list[i] ** beta_eta ))
        
    #----------------------------------------------------------------------------------------------------------------------------



    #probability calculation for edge selection----------------------------------------------------------------------------------
    '''
    flag_above_threshold=False
    for i in range(temp_len):
        if(pheromone_task_level[temp_ACO_list[i]]>tau_0_task):
            flag_above_threshold=True
    
    probability_of_selection_list=[]
    if(flag_above_threshold==True):
        for i in range(temp_len):
            try:
                if(pheromone_task_level[temp_ACO_list[i]] > tau_0_task ):
                    Q = random.uniform(0,1)
                    probability_of_selection_list.append( ( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( 1-((Q*eta_task_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
                else:
                    probability_of_selection_list.append(0)
            #probability_of_selection_list.append( random.betavariate( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) , ( eta_task_list[i] ** beta_eta )  ) *( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( eta_task_list[i] ** beta_eta )  ) / ( alpha_pheromone_mult_beta_eta ) )
            except ZeroDivisionError as err:
                probability_of_selection_list.append(1)
    if(flag_above_threshold==False):
        for i in range(temp_len):
            try:
                Q = random.uniform(0,1)
                probability_of_selection_list.append( ( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( 1-((Q*eta_task_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
            #probability_of_selection_list.append( random.betavariate( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) , ( eta_task_list[i] ** beta_eta )  ) *( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( eta_task_list[i] ** beta_eta )  ) / ( alpha_pheromone_mult_beta_eta ) )
            except ZeroDivisionError as err:
                probability_of_selection_list.append(1)
    '''
    probability_of_selection_list = []
    for i in range(temp_len):
        try:
            probability_of_selection_list.append( ( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( 1-((eta_task_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
        except ZeroDivisionError as err:
            probability_of_selection_list.append(1)

    '''
    sum = 0
    for i in range(temp_len):
        sum = sum + probability_of_selection_list[i]
    
    print sum
    '''

    temp_probability_of_selection_list = []

    for i in range(temp_len):
        temp_probability_of_selection_list.append(probability_of_selection_list[i])

    limit = 1.0
    temp_ACO_list_1 = []
    for  i in range(temp_len):
        index = roulette_wheel(temp_probability_of_selection_list, limit)
        temp_ACO_list_1.append(temp_ACO_list[index])
        temp_probability = temp_probability_of_selection_list[index]
        old_limit = limit
        limit = limit - temp_probability
        del temp_probability_of_selection_list[index]
        del temp_ACO_list[index]
        recalculate_probability(temp_probability_of_selection_list, limit, old_limit)
    
    #temp_ACO_list = list(temp_ACO_list_1)
    return temp_ACO_list_1
        
        
          
    #merge_sort(probability_of_selection_list, temp_ACO_list,0,temp_len-1)



def recalculate_probability( list, new_limit ,old_limit):
    '''
    Function:    recalculates the probability out of new limit 
    Input:       
    Output:      

    '''
    temp_len = len(list)
    for i in range(temp_len):
        new_value = (list[i] / old_limit) * new_limit
        list[i] = new_value 
    
                            
global min_delta_SLAV_list
min_delta_SLAV_list=[]    

def ACO():
    '''
    Function:    Applies ACO on the independent tasks that are present in the ACO_list
    Input:       DAG, ACO_list, 
    Output:      A list of the ants solution for all the iterations

    '''
    
    print "Executing ACO"
    print "ACO_LIST",ACO_list

    num_Ants=15
    iterations=10
    
 
    initialize_pheromone();
    
    global total_time
    global MI_temp
    global storage_temp
    global deadline_temp
    global VM_temp
    global dependencies
    del MI_temp [:]
    del storage_temp [:]
    del deadline_temp [:]
    
    
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
        for nA in range(num_Ants):
            ACO_list_len=len(ACO_list)
            count = ACO_list_len-1
            ant_allocation_list = []                           # This list stores the allocation for the ant
            for i in range(ACO_list_len):
                temp_ACO_list.append(ACO_list[i])
            del VM_temp [:]
            for i in range(VM_row):
                VM_temp.append([ VM[i][0] * VM[i][1], VM[i][2] ])    
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
                for t in range(VM_row):
                    if(VM_temp[t][0] <= 0 or VM_temp[t][1] <= 0):
                        VM_outof_resources.append(t)
                for k in range(VM_row):
                    temp_MI_violation = float(MI[temp_ACO_list[ant_position]] - VM_temp[k][0])
                    temp_storage_violation = float(storage[temp_ACO_list[ant_position]] - VM_temp[k][1])
                    try:
                        temp_deadline_violation = float(deadline[temp_ACO_list[ant_position]] - MI[temp_ACO_list[ant_position]] / VM_temp[k][0])
                    except ZeroDivisionError:
                        temp_deadline_violation = sys.float_info.max
    
                    MI_violation_list.append( temp_MI_violation )
                    storage_violation_list.append( temp_storage_violation )
                    deadline_violation_list.append( temp_deadline_violation )

                #Heuristic information calculation--------------------------------------------------------------------------------------------
                
                length_1 = len(MI_violation_list)                
                
                normalize(MI_violation_list)
                normalize(storage_violation_list)
                normalize(deadline_violation_list)
                
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
                '''
                flag_above_threshold=False
                probability_of_selection_list=[]
                if(flag_above_threshold==True):
                    for i in range(p_column_VM):
                        try:
                            if(pheromone_VM_level[temp_ACO_list[i]] > tau_0_task ):
                                Q = random.uniform(0,1)
                                probability_of_selection_list.append( ( ( pheromone_VM_level[temp_ACO_list[ant_position]][i] ** alpha_pheromone ) * ( 1-((eta_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
                            else:
                                probability_of_selection_list.append(0)
                                #probability_of_selection_list.append( random.betavariate( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) , ( eta_task_list[i] ** beta_eta )  ) *( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( eta_task_list[i] ** beta_eta )  ) / ( alpha_pheromone_mult_beta_eta ) )
                        except ZeroDivisionError as err:
                            probability_of_selection_list.append(1)
    
                if(flag_above_threshold==False):
                    for i in range(p_column_VM):
                        try:
                            Q = random.uniform(0,1)
                            probability_of_selection_list.append( ( ( pheromone_VM_level[temp_ACO_list[ant_position]][i] ** alpha_pheromone ) * ( 1-((eta_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
                            #probability_of_selection_list.append( random.betavariate( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) , ( eta_task_list[i] ** beta_eta )  ) *( ( pheromone_task_level[temp_ACO_list[i]] ** alpha_pheromone ) * ( eta_task_list[i] ** beta_eta )  ) / ( alpha_pheromone_mult_beta_eta ) )
                        except ZeroDivisionError as err:
                            probability_of_selection_list.append(1)
                            
                '''
                probability_of_selection_list=[]
                for i in range(p_column_VM):
                    try:
                        probability_of_selection_list.append( ( ( pheromone_VM_level[temp_ACO_list[ant_position]][i] ** alpha_pheromone ) * ( 1-((eta_list[i]) ** beta_eta ))  ) / ( alpha_pheromone_mult_beta_eta ) )
                    except ZeroDivisionError as err:
                        probability_of_selection_list.append(1)
                

                largest_probability_index = 0
                largest_probability = 0
                
                '''
                temp_len_prob = len(probability_of_selection_list)
                for i in range(temp_len_prob):
                    if(largest_probability < probability_of_selection_list[i] and i not in VM_outof_resources):
                        largest_probability = probability_of_selection_list[i]
                        largest_probability_index = i
                '''
                index = roulette_wheel(probability_of_selection_list, 1.0)
                
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
            
            normalize(SLAV_storage_global_list)
            normalize(SLAV_MI_global_list)
            normalize(SLAV_deadline_global_list)
            normalize(MI_required_global_list)
            normalize(storage_required_global_list)
            normalize(deadline_required_global_list)
            
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

def start_new_thread(pos):
    '''
    Function:    Utility function to execute the ACO on the ACO_list
    Input:       
    Output:      none

    '''
    starting_thread = Thread(target=put_in_global_queue, args=(pos,))
    starting_thread.start()


def put_in_global_queue(pos):
    '''
    Function:    Utility function to execute the ACO on the ACO_list
    Input:       
    Output:      none

    '''
    print "put_in_global_queue"
    
    global dependencies
    global rlock
    global global_q
    
    while(dependencies[pos]==0):
        time.sleep(2)

    synchronized_queue(2, pos)


def ACO_utility():
    '''
    Function:    Utility function to execute the ACO on the ACO_list
    Input:       
    Output:      none

    '''
    while True:
        synchronized_queue(1,0)
        time.sleep(5)
    
def synchronized_queue(choice,pos):
    '''
    Function:    This function synchronizes 1) the reading the values from global_q and then applying ACO and 2) putting the tasks in the global_q 
    Input:       choice --> (1) ACO operation (2) putting in global queue   and pos --> 0 for the ACO operation and different values for putting 
                 in global_q   
    Output:      none

    '''
    global global_q
    global rlock
    global ACO_list
    
    rlock.acquire()
    try:
        if(choice==1):
            flag=False
            while(global_q.qsize() != 0):
                flag=True
                ACO_list.append(global_q.get())
            if(flag==True):
                print dependencies
                ACO()
                print dependencies
        if(choice==2):
            if(dependencies[pos]==0):
                global_q.put(pos)
    finally:
        rlock.release()


   

def Main_test_1():
    '''
    FUNCTION:      This function is the starting point of the code execution
    INPUT:         DAG,pheromone,VM 
    OUTPUT:        none
    
    '''

    m_obj=Main()
    
    m_obj.main("-D","sankalp.xml")
    
    initialize_parameters()

    find_starting_vertices();

    find_dependencies()
    
    printf_1D_list(MI)
    printf_1D_list(storage)
    printf_1D_list(deadline)
    printf_2D_list(DAG)
    starting_vertices_len=len(starting_vertices)
    
    total_time = 0
    
    starting_thread = Thread(target=ACO_utility, args=())
    #starting_thread.daemon = True
    starting_thread.start()

    for j in range(starting_vertices_len):
        synchronized_queue(2, starting_vertices[j])

    
    print "total_time",total_time




Main_test_1()