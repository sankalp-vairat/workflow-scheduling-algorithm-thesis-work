'''
Created on 15-May-2017

@author: sankalp
'''

#Intel(R) Xeon(R) CPU X5570 Quad-Core, 2.93GHz --> 8 cores, 2 chips

from power.PowerModelSpecPower import PowerModelSpecPower
class PowerModelSpecPowerAppleIncXserve31(PowerModelSpecPower):
    power = [173, 187, 200, 214, 228, 244, 258, 273, 293, 313, 334]
    
    def getPowerData(self,index):
        return self.power[index]