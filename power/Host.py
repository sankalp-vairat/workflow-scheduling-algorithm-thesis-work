'''
Created on 16-Feb-2017

@author: itadmin
'''
from power.Pe import Pe

class Host:
    peList = []
    def __init__(self,id1,storage,peList):
        self.id = id1
        self.storage = storage
        self.setpeList(peList)
        
    def setpeList(self,peList):
        for i in range(len(peList)):
            self.peList.append(peList[i])

    def getpelist(self):
        return self.peList
    
    def getTotalMips(self):
        peList = self.getpelist()
        totalMips = 0;
        lenPeList =  len(peList)
        for i in range(lenPeList):
            totalMips += peList[i].getMips();
        return totalMips;
        