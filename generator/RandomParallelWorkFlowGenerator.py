'''
Created on 20-Mar-2017

@author: itadmin
'''
import random
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.RandomGenerator import RandomGenerator
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

class RandomParallelWorkFlowGenerator(RandomGenerator):

    def __init__(self,noOfTasks, noOfLevels, runTimeLowerBound, runTimeUpperBound, storageLowerBound, storageUpperBound, miLowerBound, miUpperBound):
        self.noOfTasks = noOfTasks
        self.noOfLevels = noOfLevels
        self.runTimeLowerBound = runTimeLowerBound
        self.runTimeUpperBound = runTimeUpperBound
        self.storageLowerBound = storageLowerBound
        self.storageUpperBound = storageUpperBound
        self.miLowerBound = miLowerBound
        self.miUpperBound = miUpperBound