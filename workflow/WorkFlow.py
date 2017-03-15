'''
Created on 15-Mar-2017

@author: itadmin
'''

global DAG
DAG=[]
global MI
MI=[]
global storage
storage=[]
global deadline
deadline=[]

KB = 1024
MB = 1024*KB
GB = 1024*MB
TB = 1024*GB

SECONDS = 1
MINUTES = 60*SECONDS
HOURS = 60*MINUTES

class WorkFlow:
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
        self.tasks = set()
    
    def addJob(self, task):
        self.tasks.add(task)
    
    def _computeDataDependencies(self):
        """This sets all the parent-child dependencies based on the input and output files of the jobs"""
        # Prepare a mapping of file -> job that generated it
        sources = {}
        for j in self.tasks:
            for k in j.outputs:
                if k in sources:
                    raise Exception("Duplicate source for %s" % k)
                sources[k] = j
        
        # Use source mapping to look up the job that produces 
        # each input for every job, and make the job dependent
        # upon it.
        for j in self.tasks:
            for i in j.inputs:
                if i in sources:
                    j.addParent(sources[i])
                    
    def createDAG(self):
        global DAG
        global MI
        global storage
        global deadline
        
        self._computeDataDependencies()
        
        for j in self.jobs:
            temp_list=[]
            for i in self.jobs:
                temp_list.append(0)
            DAG.append(temp_list)

        for j in self.jobs:
            MI.append(j.MI)
            deadline.append(j.runtime)
            storage.append(j.outputs.pop().size)

        for j in self.jobs:
            for i in j.inputs:
                name=i.name
                task=int(name.split('_')[1])
                parent_task= int(j.id.split('_')[1])
                DAG[parent_task][task]=1
        print DAG