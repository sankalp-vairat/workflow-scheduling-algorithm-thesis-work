'''
Created on 15-May-2017

@author: sankalp
'''
#Intel Xeon E5-2699 v3 2.30GHz 18-Core --> 36 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerFujitsuServerPRIMERGYTX2560M1(PowerModelSpecPower):
    power = [40, 84.3, 99.4, 114, 129, 144, 161, 185, 214, 240, 264]
    
    def getPowerData(self,index):
        return self.power[index]