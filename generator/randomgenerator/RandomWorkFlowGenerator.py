'''
Created on 15-Mar-2017

@author: itadmin
'''

import random
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.randomgenerator.RandomGenerator import RandomGenerator
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

class RandomWorkFlowGenerator(RandomGenerator):
    
    def __init__(self,noOfTasks, noOfLevels, runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperBound, type):
        self.noOfTasks = noOfTasks
        self.noOfLevels = noOfLevels
        self.runTimeLowerBound = runTimeLowerBound
        self.runTimeUpperBound = runTimeUpperBound
        self.storageLowerBound = storageLowerBound
        self.storageUpperBound = storageUpperBound
        self.miLowerBound = miLowerBound
        self.miUpperBound = miUpperBound
        self.type = type

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

    def setType(self,type):
        self.type = type

    def getType(self):
        return self.type


    def randomWorkFlowGenerator(self):
        noOfTasks = self.getNoOfTasks()
        noOfLevels = self.getNoOfLevels()
        runTimeLowerBound = self.getRunTimeLowerBound()
        runTimeUpperBound = self.getRunTimeUpperBound()
        storageLowerBound = self.getStorageLowerBound()
        storageUpperBound = self.getStorageUpperBound()
        miLowerBound = self.getMiLowerBound()
        miUpperbound = self.getMiUpperBound()
        type = self.getType()
        workflow = self._genworkflow(noOfTasks, noOfLevels,runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperbound, type)
        workflow.createDAG()
        return workflow


    def _genworkflow(self, noOfTasks, noOfLevels,runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperbound, type):
        if(type == 'RandomWorkFlow'):
            return self.randomLevel(noOfTasks, noOfLevels, UniformDistribution(runTimeLowerBound, runTimeUpperBound), UniformDistribution(storageLowerBound, storageUpperBound),UniformDistribution(miLowerBound, miUpperbound))
        elif(type == 'RandomParallelWorkFlow'):
            return self.randomParallel(noOfTasks, noOfLevels, UniformDistribution(runTimeLowerBound, runTimeUpperBound), UniformDistribution(storageLowerBound, storageUpperBound),UniformDistribution(miLowerBound, miUpperbound))
        elif(type == 'RandomForkJoinWorkFlow'):
            return self.randomForkJoin(noOfTasks, noOfLevels, UniformDistribution(runTimeLowerBound, runTimeUpperBound), UniformDistribution(storageLowerBound, storageUpperBound),UniformDistribution(miLowerBound, miUpperbound))
    
    def __writeJson(self,st):
        f= open("Output.json","a+")
        f.write(st)
        #f.write("\n");
        f.close()

    def randomLevel(self,N, L, runtimeDist,sizeDist,miDist):
        #    Approximate width of workflow
        W = int(math.ceil(N/float(L)))
    
        # Maximum in degree of a task
        max_id = int(math.floor(W/float(2)))
    
        w = WorkFlow(name="randomLevel", description="""Random Level-Oriented Workflow""")
        self.__writeJson("{\n")
        self.__writeJson("\"nodes\": [\n")
        tasks = []
        levels = [list() for l in range(0,L)]
        for i in range(0,N):
            tout = File("task_%d_out.dat"%i, size=sizeDist()*KB)
            t = Task(id="task_%d"%i, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
            w.addJob(t)
            tasks.append(t)
        
            if i < L: # Ensure each level gets one task
                self.__writeJson("{\"id\": \""+t.id+"\", \"group\":"+ str(i)+"},\n")
                levels[i].append(t)
            else:
                level = random.randint(0,L-1)
                if(i <N-1 ):
                    self.__writeJson("{\"id\": \""+t.id+"\", \"group\":"+ str(level)+"},\n")
                else:
                    self.__writeJson("{\"id\": \""+t.id+"\", \"group\":"+ str(level)+"}\n],\n")
                levels[level].append(t)
    
        # Choose random children for root level
        # Make sure each root task gets a child
        self.__writeJson("\"links\": [\n")
        for t in levels[0]:
            k = random.randint(1, min(max_id, len(levels[1])))
            
            children = random.sample(levels[1], k)
        
            for c in children:
                self.__writeJson("{\"source\": \""+t.id+"\", \"target\": \""+c.id+"\", \"value\": 1},\n")
                for i in t.outputs:
                    c.addInput(i)
                    
    
        # For levels 1..L choose random parents
        for l in range(1,L):
            op = len(levels[l])
            o1 = 0
            for t in levels[l]:
                k = random.randint(1, min(max_id, len(levels[l-1])))
            
                # make sure level 1 doesn't get too many connections to level 0
                k = max(0, k - len(t.inputs))
            
                parents = random.sample(levels[l-1], k)
                u = len(parents)
                u1 = 0
                for p in parents:
                    
                    if(l == (L-1) and u1 == (u-1) and o1 == (op-1)):
                        self.__writeJson("{\"source\": \""+p.id+"\", \"target\": \""+t.id+"\", \"value\": 1}\n")
                    else:
                        self.__writeJson("{\"source\": \""+p.id+"\", \"target\": \""+t.id+"\", \"value\": 1},\n")
                    for o in p.outputs:
                        t.addInput(o)
                    u1 = u1 + 1
                o1 = o1 + 1
        self.__writeJson("]\n}")
        return w


    def randomParallel(self,N, L, runtimeDist,sizeDist,miDist):
        # Approximate width of workflow
        W = int(math.ceil(N-2/float(L)))
    
        # Maximum in degree of a task
        max_id = 1
    
        w = WorkFlow(name="randomParallel", description="""Random Parallel Level-Oriented Workflow""")
    
        tasks = []
        levels = [list() for l in range(0,L)]
        
        # Add entry task node in level 0
        tout = File("task_%d_out.dat"%0, size=sizeDist()*KB)
        t = Task(id="task_%d"%0, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
        w.addJob(t)
        tasks.append(t)
        levels[0].append(t)

        # Randomly assign tasks to each level
        for i in range(1,N-1):
            tout = File("task_%d_out.dat"%i, size=sizeDist()*KB)
            t = Task(id="task_%d"%i, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
            w.addJob(t)
            tasks.append(t)
        
            if i < L-1: # Ensure each level gets one task
                levels[i].append(t)
            else:
                level = random.randint(1,L-2)
                levels[level].append(t)

        # Set level 0 task parent for each task in level 1
        for children in levels[1]:
            for i in levels[0][0].outputs:
                children.addInput(i)

        # For levels 2..L-2 choose random parents
        globalAvailableTasks = []
        for l in range(2,L-1):
            for lt in levels[l-1]:
                globalAvailableTasks.append(lt)
            for t in levels[l]:
                
                try:
                    k = random.randint(0,len(globalAvailableTasks)-1)
                except:
                    k = 0
                try:
                    parent = globalAvailableTasks[k]
                except Exception:
                    #print k
                    #print globalAvailableTasks
                    #print len(globalAvailableTasks)
                    continue
                
                del globalAvailableTasks[k]
                
                for o in parent.outputs:
                    t.addInput(o)

        # Add exit task to last level
        tout = File("task_%d_out.dat"%(N-1), size=sizeDist()*KB)
        t = Task(id="task_%d"%(N-1), namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
        w.addJob(t)
        tasks.append(t)
        levels[L-1].append(t)
        
        # Add all the task from the second last level
        for lt in levels[L-2]:
            globalAvailableTasks.append(lt)
        
        # Set level L-2 parent task and all the task which does not have children to level L-1 level task
        for t in globalAvailableTasks:
                for i in t.outputs:
                    levels[L-1][0].addInput(i)
         
        return w


    def randomForkJoin(self,N, L, runtimeDist,sizeDist,miDist):
        #    Approximate width of workflow
        W = int(math.ceil(N/float(L))) - 1 

        # Maximum in degree of a task
        max_id = int(math.floor(W/float(2)))

        w = WorkFlow(name="randlevel", description="""Random workflow (Similar to Figure 2c in Rahman et al, but level-oriented)""")

        tasks = []
        levels = [list() for l in range(0,L)]

        # Add entry task node in level 0
        tout = File("task_%d_out.dat"%0, size=sizeDist()*KB)
        t = Task(id="task_%d"%0, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
        w.addJob(t)
        tasks.append(t)
        levels[0].append(t)


        for i in range(1,N-1):
            tout = File("task_%d_out.dat"%i, size=sizeDist()*KB)
            t = Task(id="task_%d"%i, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
            w.addJob(t)
            tasks.append(t)
        
            if i < L: # Ensure each level gets one task
                levels[i].append(t)
            else:
                level = random.randint(1,L-2)
                levels[level].append(t)

        # Set level 0 task parent for each task in level 1
        for children in levels[1]:
            for i in levels[0][0].outputs:
                children.addInput(i)


        # For levels 2..L-2 choose random parents
        globalAvailableTasks = []
        globalAvailableTasks_dummy = []
        for l in range(2,L-1):
            for lt in levels[l-1]:
                globalAvailableTasks.append(lt)
                globalAvailableTasks_dummy.append(lt)
            
            for t in levels[l]:

                try:
                    k = random.randint(1,min(max_id,len(globalAvailableTasks)-1))
                except:
                    k = 1
                
                #print "len(globalAvailableTasks)",len(globalAvailableTasks)
                #print "k",k
                
                parents = random.sample(globalAvailableTasks, k)
                
                globalAvailableTasks_dummy = list(set(globalAvailableTasks_dummy) - set(parents))

                for p in parents:
                    for o in p.outputs:
                        t.addInput(o)
            del globalAvailableTasks[:]

            for d in globalAvailableTasks_dummy:
                globalAvailableTasks.append(d)

        # Add exit task to last level
        tout = File("task_%d_out.dat"%(N-1), size=sizeDist()*KB)
        t = Task(id="task_%d"%(N-1), namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),storage = sizeDist()*KB,outputs=[tout])
        w.addJob(t)
        tasks.append(t)
        levels[L-1].append(t)

        # Add all the task from the second last level
        for lt in levels[L-2]:
            globalAvailableTasks_dummy.append(lt)

        # Set level L-2 parent task and all the task which does not have children to level L-1 level task
        for t in globalAvailableTasks_dummy:
                for i in t.outputs:
                    levels[L-1][0].addInput(i)
    
        return w