'''
Created on 15-May-2017

@author: sankalp
'''
#Intel Xeon X5675 6 core, 3.07GHz --> 12 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerIBMSystemx3650M3(PowerModelSpecPower):
    power = [56.1, 94.2, 106, 115, 125, 137, 151, 168, 184, 200, 218]
    
    def getPowerData(self,index):
        return self.power[index]