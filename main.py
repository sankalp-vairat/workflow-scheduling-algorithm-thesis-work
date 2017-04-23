'''
Created on Mar 16, 2017

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
#syntheticGenerator =SyntheticGenerator('CyberShake_30.xml')

#syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)

dataCentre = DataCentre(1)
powerModelOur = PowerModelOur()
dataCentre.setUpDatacentre(10, 10, 20, 5,powerModelOur) 
randomGenerator = RandomWorkFlowGenerator(10,5,1,10,1,10,1000,10000,'RandomWorkFlow')
workflow = randomGenerator.randomWorkFlowGenerator()
workflow.createTaskDictionary()
#myopic = MyopicScheduler()
#minMin = MinMinScheduler()
#maxMin = MaxMinScheduler()
antColonyScheduler = AntColonyScheduler()
cloudletScheduler = CloudletScheduler(antColonyScheduler)
cloudlet = Cloudlet(cloudletId = 1,userId = 'Sankalp',status = "executing", execStartTime = time.asctime(), workFlow = workflow)
cloudletScheduler.executeScheduler(cloudlet,dataCentre)
print "Myopic ended"
print threading.active_count()