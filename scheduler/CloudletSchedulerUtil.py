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
        
        '''
        list = []

        for i in range(length_list):
            list.append(list[i])
        '''    
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


#---------------------------------------PRINT UTILITY FUNCTIONS-----------------------------------------------------------------------
    def printf(self,str):
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

    def printf_1D_list(self,list_1D):
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

    def printf_2D_list(self,list_2D):
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

    def print_1D_list(self,list_1D):
        '''
        FUNCTION:      This function prints 1D list
        INPUT:         1D list
        OUTPUT:        1D list
        (SIDE)EFFECTS: 
        
        '''

        for i in range(len(list_1D)):
            print list_1D[i],
        print ""

    def print_2D_list(self,list_2D):
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

    def print_allocations(self,ant_allocation_list,iteration,ant):
        '''
        FUNCTION:      This function prints 1D list
        INPUT:         2D list
        OUTPUT:        2D list
        (SIDE)EFFECTS: 
        
        ''' 
        
        temp_len=len(ant_allocation_list)
        
        self.printf("Iteration::"+str(iteration)+"\t"+"Ant::"+str(ant))
        for i in range(temp_len):
            task = ant_allocation_list[i].taskID
            VM = ant_allocation_list[i].assignedVMId
            self.printf("Task:: "+str(task)+"\t"+"VM:: "+str(VM))

    #-------------------------------------------------------------------------------------------------------------------------------------