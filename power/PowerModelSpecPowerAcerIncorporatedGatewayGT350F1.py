'''
Created on 15-May-2017

@author: sankalp
'''
#Intel Xeon X5675  Six-Core, 3.07 GHz --> 12 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerAcerIncorporatedGatewayGT350F1(PowerModelSpecPower):
    power = [79.5, 131, 143, 154, 166, 182, 200, 217, 232, 247, 264]
    
    def getPowerData(self,index):
        return self.power[index]