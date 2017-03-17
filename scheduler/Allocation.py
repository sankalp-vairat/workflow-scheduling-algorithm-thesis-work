'''
Created on 02-Feb-2017
@author: Sankalp Vairat
'''
class Allocation:

	def __init__(self,task,assigned_VM):
		self.task = task
		self.assigned_VM = assigned_VM
	
	def setTask(self,task):
		self.task = task
		
	def getTask(self):
		return self.task
	
	def setAssignedVMs(self, assigned_VM):
		self.assigned_VM = assigned_VM
	
	def getAssignedVMs(self):
		return self.assigned_VM
	