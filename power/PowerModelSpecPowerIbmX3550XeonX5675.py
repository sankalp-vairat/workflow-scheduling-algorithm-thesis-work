'''
Created on 16-Feb-2017

@author: itadmin
'''
from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerIbmX3550XeonX5675(PowerModelSpecPower):
    power = [58.4, 98, 109, 118, 128, 140, 153, 170, 189, 205, 222]
    
    
    def getPowerData(self,index):
        return self.power[index]