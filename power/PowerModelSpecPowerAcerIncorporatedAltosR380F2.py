'''
Created on 15-May-2017

@author: sankalp
'''

# Intel Xeon E5-2660 8 core, 2.20 GHz --> 16 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerAcerIncorporatedAltosR380F2(PowerModelSpecPower):
    power = [63.5, 78.0, 87.0, 96.5, 106, 116, 135, 158, 188, 221, 252]
    
    def getPowerData(self,index):
        return self.power[index]