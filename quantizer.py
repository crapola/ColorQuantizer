import tkinter as tk
# libs
import PIL
from PIL import Image
from scipy.spatial import KDTree
# local
import palette

_result=None
_progress=0

def get_progress():
	""" Get progress value in range [0,100] """
	return _progress

def get_result():
	""" Get result once the thread is done. """
	return _result

def quantize(photoimage,palette):
	"""
	< photoimage: tkinter.PhotoImage
	< palette: list of 3-tuple RGB values
	"""
	# Use globals.
	global _progress,_result
	
	image_source=_photoimage_to_image(photoimage)

	def clamp(mn,mx,val):
		return max(min(val,mx),mn)

	# https://en.wikipedia.org/wiki/Ordered_dithering
	def dither(color,x,y):
		pattern=((0,2),(3,1))
		k=8.0
		r=color[0]+k*pattern[x%2][y%2]-0.5
		g=color[1]+k*pattern[x%2][y%2]-0.5
		b=color[2]+k*pattern[x%2][y%2]-0.5
		r=int(clamp(0,255,r))
		g=int(clamp(0,255,g))
		b=int(clamp(0,255,b))
		return (r,g,b)
	# KDTree for nearest neighbor queries.
	tree=KDTree(palette)
	newdata=[]
	numpixels=image_source.width*image_source.height
	i=0
	for y in range(image_source.height):
		for x in range(image_source.width):
			p=image_source.getpixel((x,y))
			p=dither(p,x,y)
			c = tree.query(p)[1]
			x = palette[c]
			newdata.append(tuple(x))
			# Update progress.
			i+=1
			_progress=(100*i)/numpixels
	_result=newdata
	_progress=0

# ------------------------------------------------------------------------------

# Convert tk.PhotoImage to PIL.Image pixel by pixel because there's no other way.
def _photoimage_to_image(ph):
	w=ph.width()
	h=ph.height()
	result=Image.new("RGB", (w,h))
	for y in range(h):
		for x in range(w):
			c=ph.get(x,y)
			result.putpixel((x,y),c)
	return result

if __name__=="__main__":
	print("Testing quantizer.py.")
	root=tk.Tk()
	ph=tk.PhotoImage(file="blue_small.png")
	print(_photoimage_to_image(ph))
