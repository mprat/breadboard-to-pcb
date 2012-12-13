import component_utils as cu

class Wire:
	def __init__(self, x1, y1, x2, y2):
		self.x1 = cu.roundInt(x1)
		self.y1 = cu.roundInt(y1)
		self.x2 = cu.roundInt(x2)
		self.y2 = cu.roundInt(y2)

	def toXML(self):
		return '<wire x1=\"' + str(self.x1) + '\" y1=\"' + str(self.y1) + '\" x2=\"' + str(self.x2) + '\" y2=\"' +  str(self.y2) + '\" width=\"0.1524\" layer=\"91\"/>' 	

	def __str__(self):
		return self.toXML()
