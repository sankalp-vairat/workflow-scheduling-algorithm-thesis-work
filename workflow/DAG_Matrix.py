'''
Created on 16-Mar-2017

@author: itadmin
'''

class DAG_Matrix:
    def __init__(self,DAG):
        self.DAG = list()
        self.setDAG_matrix(DAG)
        self.DAGRows = len(DAG)
        self.DAGColumns = len(DAG[0])
        self.dependencyMatrix = []
        self.dependencyfinder()
        
    def setDAG_matrix(self,DAG):
        noOfRows = len(DAG)
        noOfColumns = len(DAG[0])
        for i in range(noOfRows):
            temp_row = []
            for j in range(noOfColumns):
                temp_row.append(DAG[i][j])
            self.DAG.append(temp_row)

    def dependencyfinder(self):
        '''
        Function:    finds the dependencies count for each task in the DAG
        Input:       Adjecency matrix representation of DAG
        Output:      List of tasks that are starting point of DAG (dependencies)

        ''' 
        print "finding dependencies count for each task ......."

        for row in range(self.DAG.DAGRows):
            count=0
            for column in range(self.DAG.DAGColumns):
                if(self.DAG[row][column]==1):
                    count=count+1
            self.dependencyMatrix.append(count)
        
        return self.dependencyMatrix
        
    def getDAG_matrix(self):
        return self.DAG
        