import threading
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
# local
from imageview import ImageView
from paletteview import PaletteView
import quantizer

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.winfo_toplevel().title("Color Quantizer")
		self.pack()
		self.create_widgets()
		self.update_buttons()

	def create_widgets(self):
		# Source image frame.
		self.source_frame=tk.LabelFrame(self,text="Source image")
		self.source_frame.grid(column=0,row=0)
		self.source_image=ImageView(self.source_frame)
		self.source_image.pack()
		self.source_button=tk.Button(self.source_frame,text="Load image",command=self.load_source)
		self.source_button.pack()
		# Palette frame.
		self.pal_frame=tk.LabelFrame(self,text="Palette")
		self.pal_frame.grid(column=1,row=0)
		self.pal_widget=PaletteView(self.pal_frame)
		self.pal_widget.pack()
		self.pal_button=tk.Button(self.pal_frame,text="Load palette",command=self.load_palette)
		self.pal_button.pack()
		# Result frame.
		self.result_frame=tk.LabelFrame(self,text="Result")
		self.result_frame.grid(column=2,row=0)
		self.result_image=ImageView(self.result_frame)
		self.result_image.pack()
		self.result_button=tk.Button(self.result_frame,text="Generate",command=self.quantize)
		self.result_button.pack(side=tk.LEFT)
		self.save_button=tk.Button(self.result_frame,text="Save",command=self.save)
		self.save_button.pack()
		# Progress bar.
		self.progress=tk.IntVar()
		self.progress_bar=ttk.Progressbar(self,variable=self.progress)
		self.progress_bar.grid(column=0,row=1,columnspan=3,sticky=tk.W+tk.E)

	def load_palette(self):
		filename=tk.filedialog.askopenfilename(defaultextension=".pal",title="Load a palette",filetypes=[("JASC Palette File","*.pal")])
		if not filename:
			return
		if not self.pal_widget.load(filename):
			tk.messagebox.showerror("Error",filename+" is not a valid palette file.")
		self.update_buttons()

	def load_source(self):
		filename=tk.filedialog.askopenfilename(title="Load an image",filetypes=[("Portable Network Graphics","*.png"),("Graphics Interchange Format","*.gif"),("All files","*.*")])
		if not filename:
			return
		if not self.source_image.load(filename):
			tk.messagebox.showerror("Error",filename+" is not a valid image file.")
		self.update_buttons()

	def quantize(self):
		self.thread=threading.Thread(None,quantizer.quantize,"QuantizeThread",(self.source_image.image_get(),self.pal_widget.palette),daemon=True)
		self.thread.start()
		self.result_button["state"]=tk.DISABLED
		self.source_button["state"]=tk.DISABLED
		self.wait_thread()

	def quantize_completed(self):
		result=quantizer.get_result()
		w=self.source_image.image_get().width()
		h=self.source_image.image_get().height()
		self.result_image.image_from_array(w,h,result)			
		self.progress.set(0)
		self.update_buttons()
		self.source_button["state"]=tk.ACTIVE

	def quantize_allowed(self):
		""" Returns True if we have an image and palette. """
		return self.source_image.image_get()!=None and self.pal_widget.palette!=None

	def save(self):
		filename=tk.filedialog.asksaveasfilename(title="Save",filetypes=[("Portable Network Graphics","*.png"),("Graphics Interchange Format","*.gif"),("All files","*.*")])
		if not filename:
			return
		self.result_image.image_get().write(filename)

	def update_buttons(self):
		""" Enable or disable buttons based on application state. """
		self.result_button["state"]=tk.ACTIVE if self.quantize_allowed() else tk.DISABLED
		self.save_button["state"]=tk.ACTIVE if self.result_image.image_get() else tk.DISABLED

	def wait_thread(self):
		if self.thread.is_alive():
			# Update progress.
			self.progress.set(quantizer.get_progress())
			# Wait and check again.
			self.after(250,self.wait_thread)
		else:
			self.quantize_completed()

if __name__=="__main__":
	root = tk.Tk()
	root.resizable(False,False)
	app = Application(master=root)
	app.mainloop()