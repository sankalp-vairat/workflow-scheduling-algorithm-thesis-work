'''
Created on 16-Feb-2017

@author: itadmin
'''


from Power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerHpProLiantMl110G4Xeon3040(PowerModelSpecPower):
    power = [86, 89.4, 92.6, 96, 99.5, 102, 106, 108, 112, 114, 117]
    
    
    def getPowerData(self,index):
        return self.power[index]