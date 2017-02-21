'''
Created on 16-Feb-2017

@author: itadmin
'''


from Power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerIbmX3250XeonX3480(PowerModelSpecPower):
    power = [42.3, 46.7, 49.7, 55.4, 61.8, 69.3, 76.1, 87, 96.1, 106, 113]
    
    
    def getPowerData(self,index):
        return self.power[index]