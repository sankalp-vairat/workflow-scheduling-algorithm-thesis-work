'''
Created on 16-Feb-2017

@author: itadmin
'''
from Power.PowerModel import PowerModel
import math
class PowerModelSpecPower(PowerModel):
    
    def getPower(self,utilization):
        if (utilization < 0 or utilization > 1):
            try:
                raise Exception()
            except Exception:
                print "Utilization value must be between 0 and 1"
        if (utilization % 0.1 == 0):
            return self.getPowerData((int) (utilization * 10));

        utilization1 = int(math.floor(utilization * 10))
        utilization2 = int(math.ceil(utilization * 10))
        power1 = self.getPowerData(utilization1);
        power2 = self.getPowerData(utilization2);
        delta = (power2 - power1) / 10;
        power = power1 + delta * (utilization - utilization1 / 10) * 100;
        return power;
    
    def getPowerdata(self,utilization):
        pass