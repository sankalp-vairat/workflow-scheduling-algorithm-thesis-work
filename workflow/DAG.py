'''
Created on 16-Mar-2017

@author: itadmin
'''
class DAG_Matrix:
    def __init__(self,DAG_matrix):
        self.DAG_matrix = list()
        self.setDAG_matrix(DAG_matrix)
        
    def setDAG_matrix(self,DAG_matrix):
        noOfRows = len(DAG_matrix)
        noOfColumns = len(DAG_matrix[0])
        for i in range(noOfRows):
            temp_row = []
            for j in range(noOfColumns):
                temp_row.append(DAG_matrix[i][j])
            self.DAG_matrix.append(temp_row)
    
    def getDAG_matrix(self):
        return self.DAG_matrix
        