'''
Created on 23-Mar-2017

@author: sankalp
'''
import xml.etree.ElementTree as ET

class SyntheticGenerator():
    def __init__(self,fileName):
        self.fileName = fileName
    
    
    def generateSyntheticWorkFlow(self):
        workFlowName = self.fileName
        
        tree = ET.parse('CyberShake_30.xml')
        root = tree.getroot()
        rootXmlns = root.get('xmlns')
        
        for i in range(0,N):
            tout = File("task_%d_out.dat"%i, size=sizeDist()*KB)
            t = Task(id="task_%d"%i, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
            w.addJob(t)
            
        for job in root.findall('{http://pegasus.isi.edu/schema/DAX}job'):
            inputs = job.findall('{http://pegasus.isi.edu/schema/DAX}uses')
            for input in inputs:
                print input.get('file'),'-->',input.get('size')
