'''
Created on 16-Feb-2017

@author: itadmin
'''


from Power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerIbmX3550XeonX5670(PowerModelSpecPower):
    power = [66, 107, 120, 131, 143, 156, 173, 191, 211, 229, 247]
    
    
    def getPowerData(self,index):
        return self.power[index]