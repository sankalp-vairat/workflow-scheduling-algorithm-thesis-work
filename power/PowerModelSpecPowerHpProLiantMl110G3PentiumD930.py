'''
Created on 16-Feb-2017

@author: itadmin
'''

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerHpProLiantMl110G3PentiumD930(PowerModelSpecPower):
    power = [105, 112, 118, 125, 131, 137, 147, 153, 157, 164, 169]
    
    
    def getPowerData(self,index):
        return self.power[index]