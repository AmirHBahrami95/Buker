from db.TradeMeta import TradeMetaTable
from tkinter import ttk # themed tk
from tkinter.messagebox import showinfo
from tkinter import font
import tkinter as tk
import datetime


class MainUI():

	def __stylize(self):
		window_width = 600
		window_height = 600

		# get the screen dimension
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		
		# find the center point
		center_x = int(screen_width/2 - window_width / 2)
		center_y = int(screen_height/2 - window_height / 2)
		
		# set the position of the window to the center of the screen
		self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
		self.root.option_add("*Font", font.Font(family="Helvetica", size=12))
		self.root.configure(bg=self.bg)

	def __initEntries(self):
		keys=TradeMetaTable.getHeaders()
		self.entries=dict()
		self.root.columnconfigure(0, weight=1)
		self.root.columnconfigure(1, weight=3)
		self.r=0
		for k in keys:
			
			# TODO create a frame here and replace it as the two fucker's parents
			# and st the frame's parent to self.root. BUT don't add the frame
			# anywhere
			# frame=ttk.Frame(self.root)
			# frame.pack(padx=10, pady=10, fill='x', expand=True)

			# create label
			ttk.Label(self.root,text=f"{k}:",background=self.bg,foreground=self.fg)\
			.grid(row=self.r,column=0,sticky=tk.W, padx=15,pady=15)
			# .pack(padx=5,side=tk.LEFT,fill',expand=True,bg='white')

			# create entry
			temp=tk.StringVar()
			self.entries[k]=ttk.Entry(self.root,textvariable=temp,background=self.bg)
			self.entries[k].grid(row=self.r,column=1,sticky=tk.E,padx=15)
			# self.entries[k].pack(padx=5,side=tk.RIGHT,fill='x',expand=True)
			self.r+=1
	
	def __findError(self):
		nn=TradeMetaTable.getNonNull()
		ens=TradeMetaTable.getEnums()
		intses=TradeMetaTable.getInts()
		for key in self.entries:
			if key in nn and not len(self.entries[key].get())>0:
				return f"'{key}' field must have at least 3+ characters" # although it technically needs only 1 character!
			elif key in ens and not self.entries[key].get() in ens[key]:
				return f"allowed values for '{key}' are: {ens[key]}"
			elif key in intses and not self.entries[key].get().replace('.','').replace('-','').isnumeric():
				return f"'{key}' must be numeric"
		return None

	def actionAdd(self):
		err=self.__findError() 
		if err is not None:
			showinfo(title='Error',message=err)
			return
		vals=dict()
		for i in self.entries:
			vals[i]=self.entries[i].get()

		# tup=self.__getSanitized()
		print(vals)
		with TradeMetaTable(self.db_path) as cur:
			cur.insert(vals)
			showinfo(title='Info',message='row inserted succesfully')


	def __initBtns(self):
		self.submitBtn=ttk.Button(self.root, text="submit", command=self.actionAdd)
		self.submitBtn\
		.grid(row=self.r,column=1,sticky=tk.W)
		# .pack(fill='x', expand=True, pady=10)

	def __init__(self,title,db_path):
		self.root = tk.Tk()
		self.root.title(title)
		self.db_path=db_path
		self.bg='#f5f5f5'
		self.fg='#c20088'
		self.__stylize()
		self.__initEntries()
		self.__initBtns()

	def run(self):
		self.root.mainloop()
