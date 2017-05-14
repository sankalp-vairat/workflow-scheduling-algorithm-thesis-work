'''
Created on 15-May-2017

@author: sankalp
'''
#Intel Xeon E5-2660, 2.20 GHz 8 cores --> 16 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerDellIncPowerEdgeR720(PowerModelSpecPower):
    power = [53.8, 77.1, 87.4, 98.4, 112, 122, 140, 160, 177, 199, 230]
    
    def getPowerData(self,index):
        return self.power[index]