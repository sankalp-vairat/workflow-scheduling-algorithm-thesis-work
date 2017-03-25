'''
Created on 15-Mar-2017

@author: itadmin
'''
class Task:
    
    def __init__(self, id, namespace=None, name=None, runtime=0, MI=0,storage=0 ,cores=1, parents=[], inputs=[], outputs = [],):
        self.id = id
        self.name = name
        self.namespace = namespace
        self.runtime = runtime
        self.MI = MI
        self.storage =  storage
        self.cores = cores
        self.inputs = set(inputs)
        self.outputs = set(outputs)
        self.parents = set(parents)
    
    def addInput(self, file_):
        self.inputs.add(file_)
    
    def addOutput(self, file_):
        self.outputs.add(file_)
    
    def addParent(self, parent):
        self.parents.add(parent)    