'''
Created on 15-May-2017

@author: sankalp
'''
#Intel Xeon E5-2699 v3 2.30 GHz 18 core 2 chips --> 36 cores

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerDellIncPowerEdgeT630(PowerModelSpecPower):
    power = [48.1, 89.6, 108, 126, 142, 157, 172, 191, 217, 247, 273]
    
    
    def getPowerData(self,index):
        return self.power[index]