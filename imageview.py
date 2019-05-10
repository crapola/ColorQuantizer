# ImageView widget.

import tkinter as tk

class ImageView(tk.Frame):
	def __init__(self, master=None,**args):
		SIZE=256
		super().__init__(master,**args)
		self.__canvas=tk.Canvas(self,**args)
		self.__canvas.pack()
		self.__image=None
		self.__image_zoomed=None
		self.__zoom_level=1
		# Disable geometry propagation, to keep size fixed.
		#self.pack_propagate(False)
		# Bind mouse wheel to the canvas.
		# X11 systems must bind to Button-4 and Button-5.
		self.__canvas.bind("<MouseWheel>", self.__on_mousewheel)	
		self.__canvas.bind("<Button-4>", self.__on_mousewheel)
		self.__canvas.bind("<Button-5>", self.__on_mousewheel)

	def image_from_array(self,w,h,arr):
		""" Create PhotoImage from array of (r,g,b) values. """
		self.__image=tk.PhotoImage(width=w,height=h)
		rows=[arr[i*w: i*w+w] for i,x in enumerate(arr[::w])]
		a=' '.join( ['{' + ' '.join( [ "#%02x%02x%02x"%x for x in y ] ) + '}' for y in rows] )
		self.__image.put(a)
		self.__update()

	def image_get(self):
		""" Get the image. """
		return self.__image

	def image_set(self,img):
		""" Set the image. """
		self.__image=img
		self.__update()

	def load(self,path):
		""" Load from disk, returns False on failure. """
		try:
			self.__image=tk.PhotoImage(file=path)
			self.__update()
			return True
		except Exception:
			return False

	def zoom(self,zoom):
		if self.__image==None:
			return
		self.__zoom_level=zoom
		self.__image_zoomed=self.__image.zoom(self.__zoom_level)
		self.__canvas.create_image(0,0,image=self.__image_zoomed,anchor=tk.NW)
		self.__canvas.config(width=self.__image_zoomed.width(),height=self.__image_zoomed.height())

	def __on_mousewheel(self,event):
		# Linux uses num.
		# Windows uses delta -+120.
		# MacOs uses delta -+1.
		count=0
		if event.num == 5 or event.delta < 0:
			count -= 1
		if event.num == 4 or event.delta > 0:
			count += 1
		new_zoom=self.__zoom_level+count
		if new_zoom>0 and new_zoom<5:
			self.zoom(new_zoom)

	# TODO: Add drag with mouse left using scrollregion.

	def __update(self):
		""" Draw image on canvas and adapt size. """ 
		self.__canvas.create_image(0,0,image=self.__image,anchor=tk.NW)
		self.__canvas.config(width=self.__image.width(),height=self.__image.height())