'''
Created on 15-May-2017

@author: sankalp
'''

#Intel Xeon L5420 2.50 GHz --> 8 cores, 2 chips


from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerHPProLiantDL160G5(PowerModelSpecPower):
    power = [148, 159, 167, 175, 184, 194, 204, 213, 220, 227, 233]
    
    def getPowerData(self,index):
        return self.power[index]