'''
Created on Mar 16, 2017
sankalp
@author: student
'''



from generator.randomgenerator.RandomWorkFlowGenerator import RandomWorkFlowGenerator
from workflow.WorkFlow import WorkFlow,DAG,MI,storage,deadline
from generator.randomgenerator.RandomGenerator import RandomGenerator
#randomWorkFlowGenerator = RandomWorkFlowGenerator(8,4,10,20,10,20,10,20,"RandomWorkFlow")

#randomWorkFlowGenerator.randomWorkFlowGenerator()

from generator.syntheticgenerator.SyntheticGenerator import SyntheticGenerator
from scheduler.myopic.MyopicScheduler import MyopicScheduler,noOfTasks as mynoOfTasks
from scheduler.minminscheduler.MinMinScheduler import MinMinScheduler,noOfTasks as minnoOfTasks
from scheduler.maxminscheduler.MaxMinScheduler import MaxMinScheduler,noOfTasks as maxnoOfTasks
from core.DataCentre import DataCentre
from scheduler.CloudletScheduler import CloudletScheduler
from core.Cloudlet import Cloudlet
import time
import threading
from scheduler.antcolonyscheduler.AntColonyScheduler import AntColonyScheduler
from power.PowerModelOur import PowerModelOur
from scheduler.CloudletSchedulerUtil import CloudletSchedulerUtil
import os
import multiprocessing
#syntheticGenerator =SyntheticGenerator('Epigenomics_24.xml')
#syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)


cloudletSchedulerUtil =CloudletSchedulerUtil()
dataCentre = DataCentre(1)
powerModelOur = PowerModelOur()
#numberOfHosts,maxStorage(GB --> KB),maxMipsPerPe*1000,maxPesPerHost,powerModel
dataCentre.setUpDatacentre(100,100,20, 5,powerModelOur)
#dataCentre.setUpDefinedDatacentre(5,200)
#noOfTasks, noOfLevels, runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperBound, type 
#randomGenerator = RandomWorkFlowGenerator(100,10,1,10,1,10,1000,10000,'RandomParallelWorkFlow')
#workflow = randomGenerator.randomWorkFlowGenerator()
syntheticGenerator =SyntheticGenerator('CYBERSHAKE.n.100.0.dax')
workflow = syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)

workflow.createTaskDictionary()
myopic = MyopicScheduler()
minMin = MinMinScheduler()
maxMin = MaxMinScheduler()
antColonyScheduler = AntColonyScheduler()



cloudletSchedulerUtil.printf("CyberShake_100:"+str(100))
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
cloudletSchedulerUtil.printf("MinMin Started");
cloudletScheduler = CloudletScheduler(minMin)
cloudlet = Cloudlet(cloudletId = 1,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MinMin ended"
cloudletSchedulerUtil.printf("MinMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("max Started");
cloudletScheduler = CloudletScheduler(maxMin)
cloudlet = Cloudlet(cloudletId = 1,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MaxMin ended"
cloudletSchedulerUtil.printf("MaxMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#-------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("Myopic Started");
cloudletScheduler = CloudletScheduler(myopic)
cloudlet = Cloudlet(cloudletId = 1,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
cloudletSchedulerUtil.printf("Myopic ended");
print "Myopic ended"
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("ACO Started");
cloudletScheduler = CloudletScheduler(antColonyScheduler)
cloudlet = Cloudlet(cloudletId = 1,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "ACO ended"
cloudletSchedulerUtil.printf("ACO ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#--------------------------------------------------------------------------------------------------------------------------------

print "****************************************************************************************************************************"

del DAG[:]
del MI[:]
del deadline[:]
del storage[:]

#randomGenerator = RandomWorkFlowGenerator(200,20,1,10,1,10,1000,10000,'RandomParallelWorkFlow')
#workflow1 = randomGenerator.randomWorkFlowGenerator()

syntheticGenerator1 = SyntheticGenerator('CYBERSHAKE.n.200.0.dax')
workflow1 = syntheticGenerator1.generateSyntheticWorkFlow(1000, 10000)

workflow1.createTaskDictionary()
myopic = MyopicScheduler()
minMin = MinMinScheduler()
maxMin = MaxMinScheduler()
antColonyScheduler = AntColonyScheduler()

cloudletSchedulerUtil.printf("CyberShake_100:"+str(100))
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
cloudletSchedulerUtil.printf("MinMin Started");
cloudletScheduler = CloudletScheduler(minMin)
cloudlet = Cloudlet(cloudletId = 2,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow1)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MinMin ended"
cloudletSchedulerUtil.printf("MinMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("max Started");
cloudletScheduler = CloudletScheduler(maxMin)
cloudlet = Cloudlet(cloudletId = 2,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow1)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MaxMin ended"
cloudletSchedulerUtil.printf("MaxMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#-------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("Myopic Started");
cloudletScheduler = CloudletScheduler(myopic)
cloudlet = Cloudlet(cloudletId = 2,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow1)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
cloudletSchedulerUtil.printf("Myopic ended");
print "Myopic ended"
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("ACO Started");
cloudletScheduler = CloudletScheduler(antColonyScheduler)
cloudlet = Cloudlet(cloudletId = 2,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow1)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "ACO ended"
cloudletSchedulerUtil.printf("ACO ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#--------------------------------------------------------------------------------------------------------------------------------
print "*******************************************************************************************************************************"

del DAG[:]
del MI[:]
del deadline[:]
del storage[:]

#randomGenerator = RandomWorkFlowGenerator(300,30,1,10,1,10,1000,10000,'RandomParallelWorkFlow')
#workflow2 = randomGenerator.randomWorkFlowGenerator()

syntheticGenerator = SyntheticGenerator('CYBERSHAKE.n.300.0.dax')
workflow2 = syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)

workflow2.createTaskDictionary()
myopic = MyopicScheduler()
minMin = MinMinScheduler()
maxMin = MaxMinScheduler()
antColonyScheduler = AntColonyScheduler()

cloudletSchedulerUtil.printf("CyberShake_100:"+str(100))
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
cloudletSchedulerUtil.printf("MinMin Started");
cloudletScheduler = CloudletScheduler(minMin)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MinMin ended"
cloudletSchedulerUtil.printf("MinMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("max Started");
cloudletScheduler = CloudletScheduler(maxMin)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MaxMin ended"
cloudletSchedulerUtil.printf("MaxMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#-------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("Myopic Started");
cloudletScheduler = CloudletScheduler(myopic)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
cloudletSchedulerUtil.printf("Myopic ended");
print "Myopic ended"
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("ACO Started");
cloudletScheduler = CloudletScheduler(antColonyScheduler)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "ACO ended"
cloudletSchedulerUtil.printf("ACO ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#--------------------------------------------------------------------------------------------------------------------------------


print "*******************************************************************************************************************************"

del DAG[:]
del MI[:]
del deadline[:]
del storage[:]

#randomGenerator = RandomWorkFlowGenerator(400,40,1,10,1,10,1000,10000,'RandomParallelWorkFlow')
#workflow2 = randomGenerator.randomWorkFlowGenerator()

syntheticGenerator = SyntheticGenerator('CYBERSHAKE.n.400.0.dax')
workflow2 = syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)

workflow2.createTaskDictionary()
myopic = MyopicScheduler()
minMin = MinMinScheduler()
maxMin = MaxMinScheduler()
antColonyScheduler = AntColonyScheduler()

cloudletSchedulerUtil.printf("CyberShake_100:"+str(100))
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
cloudletSchedulerUtil.printf("MinMin Started");
cloudletScheduler = CloudletScheduler(minMin)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MinMin ended"
cloudletSchedulerUtil.printf("MinMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("max Started");
cloudletScheduler = CloudletScheduler(maxMin)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MaxMin ended"
cloudletSchedulerUtil.printf("MaxMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#-------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("Myopic Started");
cloudletScheduler = CloudletScheduler(myopic)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
cloudletSchedulerUtil.printf("Myopic ended");
print "Myopic ended"
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("ACO Started");
cloudletScheduler = CloudletScheduler(antColonyScheduler)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "ACO ended"
cloudletSchedulerUtil.printf("ACO ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#--------------------------------------------------------------------------------------------------------------------------------

print "*******************************************************************************************************************************"

del DAG[:]
del MI[:]
del deadline[:]
del storage[:]

#randomGenerator = RandomWorkFlowGenerator(400,40,1,10,1,10,1000,10000,'RandomParallelWorkFlow')
#workflow2 = randomGenerator.randomWorkFlowGenerator()

syntheticGenerator = SyntheticGenerator('CYBERSHAKE.n.500.0.dax')
workflow2 = syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)

workflow2.createTaskDictionary()
myopic = MyopicScheduler()
minMin = MinMinScheduler()
maxMin = MaxMinScheduler()
antColonyScheduler = AntColonyScheduler()

cloudletSchedulerUtil.printf("CyberShake_100:"+str(100))
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
cloudletSchedulerUtil.printf("MinMin Started");
cloudletScheduler = CloudletScheduler(minMin)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MinMin ended"
cloudletSchedulerUtil.printf("MinMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("max Started");
cloudletScheduler = CloudletScheduler(maxMin)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "MaxMin ended"
cloudletSchedulerUtil.printf("MaxMin ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#-------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("Myopic Started");
cloudletScheduler = CloudletScheduler(myopic)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
cloudletSchedulerUtil.printf("Myopic ended");
print "Myopic ended"
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#------------------------------------------------------------------------------------------------------------------------------
cloudletSchedulerUtil.printf("ACO Started");
cloudletScheduler = CloudletScheduler(antColonyScheduler)
cloudlet = Cloudlet(cloudletId = 3,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow2)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "ACO ended"
cloudletSchedulerUtil.printf("ACO ended");
cloudletSchedulerUtil.printf("-------------------------------------------------------------------------------------------------")
#--------------------------------------------------------------------------------------------------------------------------------
'''
import theano.tensor as T
import numpy
from theano import function
import random
import timeit

x = T.dmatrix('x')

y = T.dmatrix('y')

z = x + y

f = function([x, y], z)
q = 3000
s = timeit.default_timer()
f(numpy.random.rand(q,q), numpy.random.rand(q,q))
c =  numpy.random.rand(q,q)
e = timeit.default_timer()

print e-s


print "-------------------------------------------------"
s = timeit.default_timer()
a =  numpy.random.rand(q,q)
b =  numpy.random.rand(q,q)
c =  numpy.random.rand(q,q)

for i in range(q):
    for j in range(q):
        c[i][j] = a[i][j] + b[i][j]
        
e = timeit.default_timer()

print e-s
'''
