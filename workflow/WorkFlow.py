'''
Created on 15-Mar-2017

@author: itadmin
'''
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