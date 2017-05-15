'''
Created on 23-Mar-2017

@author: sankalp
'''


import xml.etree.ElementTree as ET

from workflow.WorkFlow import WorkFlow
from workflow.Task import Task
from workflow.File import File
from generator.UniformDistribution import UniformDistribution

KB = 1024
MB = 1024*KB
GB = 1024*MB
TB = 1024*GB

SECONDS = 1
MINUTES = 60*SECONDS
HOURS = 60*MINUTES
import random

class SyntheticGenerator():
    def __init__(self,fileName):
        self.fileName = fileName
    

    def generateSyntheticWorkFlow(self,miLowerBound, miUpperBound):
        workFlowName = self.fileName

        workFlow = WorkFlow(name=workFlowName, description="""Synthetic DataSet"""+workFlowName)
        
        tree = ET.parse(self.fileName)
        root = tree.getroot()
        dictionaryOfTasks =  {}
        for job in root.findall('{http://pegasus.isi.edu/schema/DAX}job'):
            files = job.findall('{http://pegasus.isi.edu/schema/DAX}uses')
            #mi = random.uniform(miLowerBound, miUpperBound)
            mi = 15000 * float(job.get('runtime'))*SECONDS
            task = Task(id="task_%s"% int(job.get('id')[2:]), namespace=job.get('namespace'), name=job.get('name'), runtime=float(job.get('runtime'))*SECONDS, MI=mi)
            size = 0
            for file in files:
                #if(file.get('link') == 'input'):
                    #t.addInput(File(file.get('file'),size = file.get('size')))
                if(file.get('link') == 'output'):
                    size = size + int(file.get('size'))
                    tout = File("task_%d_out.dat"% int(job.get('id')[2:]), size = int(file.get('size')))
                    task.addOutput(tout)
                    
            task.storage = float(file.get('size'))
            dictionaryOfTasks.update({int(job.get('id')[2:]):task})
            
                
        for child in root.findall('{http://pegasus.isi.edu/schema/DAX}child'):
            parents =  child.findall('{http://pegasus.isi.edu/schema/DAX}parent')
            if(dictionaryOfTasks.has_key(int(child.get('ref')[2:]))):
                task =  dictionaryOfTasks.get(int(child.get('ref')[2:]))
                for parent in parents:
                    task.addInput(File("task_%d_out.dat"% int(parent.get('ref')[2:]), size = None ))
                    
        for taskName, task in dictionaryOfTasks.iteritems():
            workFlow.addJob(task)
        
        workFlow.createDAG()

        return workFlow
