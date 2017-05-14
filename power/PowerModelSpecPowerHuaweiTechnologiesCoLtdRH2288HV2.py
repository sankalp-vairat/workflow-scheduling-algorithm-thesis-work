'''
Created on 15-May-2017

@author: sankalp
'''
#Intel Xeon E5-2609 4-Core, 2.4GHz --> 8 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerHuaweiTechnologiesCoLtdRH2288HV2(PowerModelSpecPower):
    power = [68.7, 78.3, 84, 88.4, 92.5, 97.3, 104, 111, 121, 131, 137]
    
    def getPowerData(self,index):
        return self.power[index]