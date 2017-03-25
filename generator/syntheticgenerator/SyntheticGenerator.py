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


class SyntheticGenerator():
    def __init__(self,fileName):
        self.fileName = fileName
    

    def generateSyntheticWorkFlow(self,miLowerBound, miUpperBound):
        workFlowName = self.fileName

        workFlow = WorkFlow(name=workFlowName, description="""Synthetic DataSet"""+workFlowName)
        
        tree = ET.parse('CyberShake_30.xml')
        root = tree.getroot()
        dictionaryOfTasks =  {}
        for job in root.findall('{http://pegasus.isi.edu/schema/DAX}job'):
            files = job.findall('{http://pegasus.isi.edu/schema/DAX}uses')
            task = Task(id="task_%s"% job.get('id'), namespace=job.get('namespace'), name=job.get('name'), runtime=job.get('runtime')*SECONDS, MI=UniformDistribution(miLowerBound, miUpperBound))
            size = 0
            for file in files:
                #if(file.get('link') == 'input'):
                    #t.addInput(File(file.get('file'),size = file.get('size')))
                if(file.get('link') == 'output'):
                    size = size + int(file.get('size'))
                    tout = File("task_%s_out.dat"% job.get('id'), size = file.get('size'))
                    task.addOutput(tout)
                    
            task.storage = file.get('size')
            dictionaryOfTasks.update({job.get('id'):task})
            
                
        for child in root.findall('{http://pegasus.isi.edu/schema/DAX}child'):
            parents =  child.findall('{http://pegasus.isi.edu/schema/DAX}parent')
            if(dictionaryOfTasks.has_key(child.get('ref'))):
                task =  dictionaryOfTasks.get(child.get('ref'))
                for parent in parents:
                    task.addInput(File("task_%s_out.dat"% parent.get('ref'), size = None ))
                    
        for taskName, task in dictionaryOfTasks.iteritems():
            workFlow.addJob(task)
        
        workFlow.createDAG()

        return workFlow
