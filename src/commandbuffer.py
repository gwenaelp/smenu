class CommandBuffer(object):
	"""handles the text buffer"""

	def __init__(self):
		self.text=""
		self.curpos=0
		self.charwidth = 6

	def add(self, c):
		self.text += c
		self.curpos +=1

	def launch(self):
		pass

	def erase(self):
		if self.curpos > 0:
			self.text = self.text[:self.curpos-1] + self.text[self.curpos:]
			self.curpos -=1

	def delete(self):
		if self.curpos < len(self.text)+1:
			self.text = self.text[:self.curpos] + self.text[self.curpos+1:]

	def moveLeft(self):
		if self.curpos > 0:
			self.curpos -=1

	def moveRight(self):
		if self.curpos < len(self.text)+1:
			self.curpos +=1

	def draw(self, drawManager):
		x = 10
		y = 12
		drawManager.draw_text(x, y, self.text)

		line_x = x + self.charwidth * self.curpos
		drawManager.draw_line(line_x, y - 10, line_x, y + 2)