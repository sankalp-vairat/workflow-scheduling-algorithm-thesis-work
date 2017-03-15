'''
Created on 15-Mar-2017

@author: itadmin
'''
class File:
    def __init__(self, name, size=0):
        self.name = name
        self.size = size
    
    def __repr__(self):
        return "<File %s>" % self.name