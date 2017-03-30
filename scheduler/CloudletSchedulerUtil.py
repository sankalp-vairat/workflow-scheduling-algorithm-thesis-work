'''
Created on 29-Mar-2017

@author: sankalp
'''
from scheduler.CloudletScheduler import CloudletScheduler


class CloudletSchedulerUtil:
    
    def findRootTasks(self,DAG_Matrix):
        '''
        Function:  find the starting tasks in the DAG
        Input:     Adjecency matrix representation of DAG
        Output:    List of tasks that are starting point of DAG

        '''
        print "finding starting tasks in dependency graph......."

        starting_vertices=[];
        for row in range(DAG_Matrix.DAGRows):
            start_v=True
            for column in range(DAG_Matrix.DAGColumns):
                if(DAG_Matrix.DAG[row][column]==1):
                    start_v=False
                    continue;
            if(start_v==True):
                starting_vertices.append(row)
        
        return starting_vertices
    
    def normalize(self,list):
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
        