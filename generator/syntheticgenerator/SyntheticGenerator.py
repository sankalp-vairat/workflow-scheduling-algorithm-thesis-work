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
    def __init__(self):
        pass
    
    
    def generateSyntheticWorkFlow(self,miLowerBound, miUpperBound):
        workFlowName = self.fileName
        
        w = WorkFlow(name=workFlowName, description="""Synthetic DataSet"""+workFlowName)
        
        tree = ET.parse('CyberShake_30.xml')
        root = tree.getroot()
            
        for job in root.findall('{http://pegasus.isi.edu/schema/DAX}job'):
            files = job.findall('{http://pegasus.isi.edu/schema/DAX}uses')
            t = Task(id=job.get('id'), namespace=job.get('namespace'), name=job.get('name'), runtime=job.get('runtime')*SECONDS, MI=UniformDistribution(miLowerBound, miUpperBound()),storage = None,outputs=None)
            size = 0
            for file in files:
                if(file.get('link') == 'input'):
                    t.addInput(File(file.get('file'),size = file.get('size')))
                if(file.get('link') == 'output'):
                    size = size + int(file.get('size'))
                    t.addOutput(File(file.get('file'),size = file.get('size')))
                t.storage = file.get('size')
