'''
Created on 29-Mar-2017

@author: sankalp
'''
from scheduler.CloudletScheduler import CloudletScheduler


class CloudletSchedulerUtil(CloudletScheduler):
    
    def findRootTasks(self,DAG):
        '''
        Function:  find the starting tasks in the DAG
        Input:     Adjecency matrix representation of DAG
        Output:    List of tasks that are starting point of DAG

        '''
        print "finding starting tasks in dependency graph......."

        starting_vertices=[];
        for row in range(DAG.DAGRows):
            start_v=True
            for column in range(DAG.DAGColumns):
                if(DAG[row][column]==1):
                    start_v=False
                    continue;
            if(start_v==True):
                starting_vertices.append(row)
        
        return starting_vertices