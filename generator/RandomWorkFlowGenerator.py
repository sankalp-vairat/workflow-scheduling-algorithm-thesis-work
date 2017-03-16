'''
Created on 15-Mar-2017

@author: itadmin
'''
from generator.RandomGenerator import RandomGenerator
import random
import math
from workflow.WorkFlow import WorkFlow
from workflow.Task import Task
from workflow.File import File
from generator.UniformDistribution import UniformDistribution
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

KB = 1024
MB = 1024*KB
GB = 1024*MB
TB = 1024*GB

SECONDS = 1
MINUTES = 60*SECONDS
HOURS = 60*MINUTES

class RandomWorkFlowGenerator(RandomGenerator):
    
    def __init__(self,noOfTasks, noOfLevels, runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperBound):
        self.noOfTasks = noOfTasks
        self.noOfLevels = noOfLevels
        self.runTimeLowerBound = runTimeLowerBound
        self.runTimeUpperBound = runTimeUpperBound
        self.storageLowerBound = storageLowerBound
        self.storageUpperBound = storageUpperBound
        self.miLowerBound = miLowerBound
        self.miUpperBound = miUpperBound
        
    def getNoOfTasks(self):
        return self.noOfTasks
    
    def getNoOfLevels(self):
        return self.noOfLevels
    
    def getRunTimeLowerBound(self):
        return self.runTimeLowerBound
    
    def getRunTimeUpperBound(self):
        return self.runTimeUpperBound
    
    def getStorageLowerBound(self):
        return self.storageLowerBound
    
    def getStorageUpperBound(self):
        return self.storageUpperBound
        
    def getMiLowerBound(self):
        return self.miLowerBound
    
    def getMiUpperBound(self):
        return self.miUpperBound

    def setNoOfTasks(self,noOfTasks):
        self.noOfTasks = noOfTasks
    
    def setNoOfLevels(self,noOfLevels):
        self.noOfLevels = noOfLevels
    
    def setRunTimeLowerBound(self,runTimeLowerBound):
        self.runTimeLowerBound = runTimeLowerBound
    
    def setRunTimeUpperBound(self,runTimeUpperBound):
        self.runTimeUpperBound = runTimeUpperBound
    
    def setStorageLowerBound(self,storageLowerbound):
        self.storageLowerbound = storageLowerbound
    
    def setStorageUpperBound(self,storageUpperbound):
        self.storageUpperbound = storageUpperbound
        
    def setMiLowerBound(self,miLowerBound):
        self.miLowerBound = miLowerBound
    
    def setMiUpperBound(self,miUpperBound):
        self.miUpperBound = miUpperBound
    
    def randomWorkFlowGenerator(self):
        noOfTasks = self.getNoOfTasks()
        noOfLevels = self.getNoOfLevels()
        runTimeLowerBound = self.getRunTimeLowerBound()
        runTimeUpperBound = self.getRunTimeUpperBound()
        storageLowerBound = self.getStorageLowerBound()
        storageUpperBound = self.getStorageUpperBound()
        miLowerBound = self.getMiLowerBound()
        miUpperbound = self.getMiUpperBound()
        workflow = self._genworkflow(noOfTasks, noOfLevels,runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperbound)
        workflow.createDAG()
        

    def _genworkflow(self, noOfTasks, noOfLevels,runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperbound):
        return self.randlevel(noOfTasks, noOfLevels, UniformDistribution(runTimeLowerBound, runTimeUpperBound), UniformDistribution(storageLowerBound, storageUpperBound),UniformDistribution(miLowerBound, miUpperbound))
    
    
    def randlevel(self,N, L, runtimeDist,sizeDist,miDist):
        #    Approximate width of workflow
        W = int(math.ceil(N/float(L)))
    
        # Maximum in degree of a task
        max_id = int(math.floor(W/float(2)))
    
        w = WorkFlow(name="randlevel", description="""Random workflow (Similar to Figure 2c in Rahman et al, but level-oriented)""")
    
        tasks = []
        levels = [list() for l in range(0,L)]
        for i in range(0,N):
            tout = File("task_%d_out.dat"%i, size=sizeDist()*KB)
            t = Task(id="task_%d"%i, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
            w.addJob(t)
            tasks.append(t)
        
            if i < L: # Ensure each level gets one task
                levels[i].append(t)
            else:
                level = random.randint(0,L-1)
                levels[level].append(t)
    
        # Choose random children for root level
        # Make sure each root task gets a child
        for t in levels[0]:
            k = random.randint(1, min(max_id, len(levels[1])))
        
            children = random.sample(levels[1], k)
        
            for c in children:
                for i in t.outputs:
                    c.addInput(i)
    
        # For levels 1..L choose random parents
        for l in range(1,L):
            for t in levels[l]:
                k = random.randint(1, min(max_id, len(levels[l-1])))
            
                # make sure level 1 doesn't get too many connections to level 0
                k = max(0, k - len(t.inputs))
            
                parents = random.sample(levels[l-1], k)
                for p in parents:
                    for o in p.outputs:
                        t.addInput(o)
    
        return w
        
        
        