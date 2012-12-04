import numpy as np

class Wire:
	def __init__(self):
		self.pixelLoc = []

	def addPixelLoc(self, pixelloc):
		self.pixelLoc.extend(pixelloc)

	def __str__(self):
		return self.pixelLoc.__str__()

	def getPixelLoc(self):
		return self.pixelLoc
