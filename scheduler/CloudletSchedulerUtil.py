'''
Created on 29-Mar-2017

@author: sankalp
'''
from scheduler.CloudletScheduler import CloudletScheduler

global dependencyMatrix 
dependencyMatrix = []

global DAGRows
global DAGColumns

class CloudletSchedulerUtil(CloudletScheduler):
    
    def dependencyfinder(self,DAG):
        '''
        Function:    finds the dependencies count for each task in the DAG
        Input:       Adjecency matrix representation of DAG
        Output:      List of tasks that are starting point of DAG (dependencies)

        ''' 
        print "finding dependencies count for each task ......."

        global DAGRows
        global DAGColumns
        global dependencyMatrix

        DAGRows = len(DAG)
        DAGColumns = len(DAG[0])

        for row in range(DAGRows):
            count=0
            for column in range(DAGColumns):
                if(DAG[row][column]==1):
                    count=count+1
            dependencyMatrix.append(count)
        
        return dependencyMatrix