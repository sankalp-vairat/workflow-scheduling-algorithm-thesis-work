'''
Created on Mar 16, 2017

@author: student
'''



from generator.randomgenerator.RandomWorkFlowGenerator import RandomWorkFlowGenerator


#randomWorkFlowGenerator = RandomWorkFlowGenerator(8,4,10,20,10,20,10,20,"RandomWorkFlow")

#randomWorkFlowGenerator.randomWorkFlowGenerator()

from generator.syntheticgenerator.SyntheticGenerator import SyntheticGenerator

syntheticGenerator =SyntheticGenerator('CyberShake_30.xml')

syntheticGenerator.generateSyntheticWorkFlow(1000, 10000)