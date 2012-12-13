class Wire:
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def toXML(self):
		return '<wire x1=\"' + str(x1) + '\" y1=\"' + str(y1) + '\" x2=\"' + str(x2) + '\" y2=\"' +  str(y2) + '\"width=\"0.1524\" layer=\"1\"/>' 	

	def __str__(self):
		return self.xml
