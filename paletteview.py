# PaletteView widget.

import math
import tkinter as tk
# local
import palette

class PaletteView(tk.Frame):
	def __init__(self, master=None,**args):
		super().__init__(master,**args)
		SIZE=256
		self.canvas=tk.Canvas(self,width=SIZE,height=SIZE)
		self.canvas.pack()
		self.palette=None

	def load(self,filename):
		try:
			self.palette=palette.load_jasc_pal(filename)
			self.__draw()
			return True
		except Exception:
			return False

	def __draw(self):
		if self.palette==None:
			return
		numcolors=len(self.palette)
		columns=int(math.sqrt(numcolors))
		rows=numcolors//columns + numcolors%columns
		cw=int(self.canvas["width"])//columns
		ch=int(self.canvas["height"])//rows
		index=0
		for y in range(rows):
			for x in range(columns):
				posx=x*cw
				posy=y*ch
				color="#%02x%02x%02x"%self.palette[index]
				r=self.canvas.create_rectangle(posx,posy,posx+cw,posy+ch,fill=color)
				index+=1
				if index>=numcolors:
					return
