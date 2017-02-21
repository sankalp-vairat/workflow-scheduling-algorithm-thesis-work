'''
Created on 16-Feb-2017

@author: itadmin
'''



from Power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerIbmX3250XeonX3470(PowerModelSpecPower):
    power = [41.6, 46.7, 52.3, 57.9, 65.4, 73, 80.7, 89.5, 99.6, 105, 113]
    
    
    def getPowerData(self,index):
        return self.power[index]