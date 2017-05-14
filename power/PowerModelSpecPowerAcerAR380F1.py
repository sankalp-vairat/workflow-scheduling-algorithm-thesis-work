'''
Created on 15-May-2017

@author: sankalp
'''


#Intel Xeon X5670 Six-Core, 2.93 GHz -->12 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerAcerAR380F1(PowerModelSpecPower):
    power = [76.6, 126, 138, 149, 163, 179, 197, 213, 229, 244, 259]
    
    def getPowerData(self,index):
        return self.power[index]