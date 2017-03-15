'''
Created on 15-Mar-2017

@author: itadmin
'''
import random

class UniformDistribution:
    def __init__(self, low, high):
        self.low = low
        self.high = high
    
    def __call__(self):
        return random.uniform(self.low, self.high)
    
    def __repr__(self):
        return "UniformDistribution(%s, %s)" % (self.low, self.high)