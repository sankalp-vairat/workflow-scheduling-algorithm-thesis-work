'''
Created on 21-Feb-2017

@author: itadmin
'''
from power.Pe import Pe
from power.PowerHost import PowerHost
from power.PowerModelLinear import PowerModelLinear
from power.PowerModelSpecPowerHpProLiantMl110G3PentiumD930 import PowerModelSpecPowerHpProLiantMl110G3PentiumD930

pe1 = Pe(12000)
pe2 = Pe(8000)
pe3 = Pe(4000)

#powerModel = PowerModelLinear(250,0.7)
powerModel = PowerModelSpecPowerHpProLiantMl110G3PentiumD930()
pe_list_1 = [pe1,pe2,pe3]

ph1 = PowerHost(1,1024,pe_list_1,powerModel)

ph1.setUtilizationMips(1000)
print ph1.getmaxPower()
print ph1.getPower()