'''
Created on 16-Feb-2017

@author: itadmin
'''

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerHpProLiantMl110G5Xeon3075(PowerModelSpecPower):
    power = [93.7, 97, 101, 105, 110, 116, 121, 125, 129, 133, 135]
    
    
    def getPowerData(self,index):
        return self.power[index]