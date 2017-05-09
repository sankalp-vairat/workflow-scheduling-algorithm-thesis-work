'''
Created on Mar 16, 2017
sankalp
@author: student
'''



from generator.randomgenerator.RandomWorkFlowGenerator import RandomWorkFlowGenerator
from workflow.WorkFlow import WorkFlow
from generator.randomgenerator.RandomGenerator import RandomGenerator
#randomWorkFlowGenerator = RandomWorkFlowGenerator(8,4,10,20,10,20,10,20,"RandomWorkFlow")

#randomWorkFlowGenerator.randomWorkFlowGenerator()

from generator.syntheticgenerator.SyntheticGenerator import SyntheticGenerator
from scheduler.myopic.MyopicScheduler import MyopicScheduler
from scheduler.minminscheduler.MinMinScheduler import MinMinScheduler
from scheduler.maxminscheduler.MaxMinScheduler import MaxMinScheduler
from core.DataCentre import DataCentre
from scheduler.CloudletScheduler import CloudletScheduler
from core.Cloudlet import Cloudlet
import time
import threading
from scheduler.antcolonyscheduler.AntColonyScheduler import AntColonyScheduler
from power.PowerModelOur import PowerModelOur
from scheduler.CloudletSchedulerUtil import CloudletSchedulerUtil
import os
import affinity
import multiprocessing
print "affinity is :",affinity.get_process_affinity_mask(0) 
affinity.set_process_affinity_mask(0,2**multiprocessing.cpu_count()-1)
print "affinity Modified :",affinity.get_process_affinity_mask(0) 
#syntheticGenerator =SyntheticGenerator('CyberShake_30.xml')
#syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)


cloudletSchedulerUtil =CloudletSchedulerUtil()
dataCentre = DataCentre(1)
powerModelOur = PowerModelOur()
#numberOfHosts,maxStorage(GB --> KB),maxMipsPerPe*1000,maxPesPerHost,powerModel
dataCentre.setUpDatacentre(10,200,20, 8,powerModelOur)
#noOfTasks, noOfLevels, runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperBound, type 
#randomGenerator = RandomWorkFlowGenerator(2000,100,1,10,1,10,1000,10000,'RandomForkJoinWorkFlow')
#workflow = randomGenerator.randomWorkFlowGenerator()
syntheticGenerator =SyntheticGenerator('CyberShake_100.xml')
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
