import os
import sqlite3
import string

import tkinter as tk
from tkinter import ttk
from tkinter import  *

from tkinter import filedialog as fd
from os import path

def main():
	gpkgapp = gpkgGUI()

	gpkgapp.mainwin.mainloop()


class gpkgGUI:
	def __init__(self):
		self.mainwin = tk.Tk()
		self.mainwin.geometry("800x800")
		self.mainwin.title("GeoPackage Info")
		self.mainframe = ttk.Frame(self.mainwin, padding="5 5 10 10")
		self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		ttk.Label(self.mainframe, text='GeoPackage file: ').grid(column=1, row=1)
		browseBtn = ttk.Button(self.mainframe, text="Browse...", command=self.fileSelect).grid(column=3,row=1)
		exitBtn = ttk.Button(self.mainframe, text="Quit", command=self.quit).grid(column=3,row=2)

	def fileSelect(self):
		fDir  = path.dirname(__file__)
		gpkg_file = fd.askopenfilename()
		ttk.Label(self.mainframe, text=gpkg_file).grid(column=2, row=1)
		self.doTheDatabaseThing(gpkg_file)
		
	def quit(self):
		self.mainwin.destroy()
		
	def doTheDatabaseThing(self, gpkg_file):
		print("Connecting to ", gpkg_file)
		conn = sqlite3.connect(gpkg_file)
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		
		tree = ttk.Treeview(self.mainframe, columns=('GeoTypes'))
		tree.grid(column=1,row=4)
		tree.column('GeoTypes', width=200)
		c.execute("select data_type, table_name from gpkg_contents order by data_type asc")
		print("Geo data types:")
		geotype = None
		top_id = tree.insert('', 'end', 'Geo Data Types', text='Geo Data Types')
		for row in c.fetchall():
			if row[0] != geotype:
				geotype = row[0]
				id = tree.insert(top_id, 'end', geotype, text=geotype)
				print(geotype, ": ")
			tree.insert(id, 'end', text=row[1])
			print("    ", row[1])
		print()
		
		tree = ttk.Treeview(self.mainframe, columns=('GeoTypes'))
		tree.grid(column=2, row=4)
		tree.column('GeoTypes', width=200)
		#c.execute("select table_name, extension_name from gpkg_extensions order by extension_name asc, table_name asc")
		c.execute("select distinct extension_name from gpkg_extensions order by extension_name asc")
		print("Extensions:")
		top_id = tree.insert('', 'end', 'Extensions', text='Extensions')
		for row in c.fetchall():
			print(row[0])
			tree.insert(top_id, 'end', row[0], text=row[0])
		print()
		
		tree = ttk.Treeview(self.mainframe, columns=('GeoTypes'))
		tree.grid(column=1, row=5)
		tree.column('GeoTypes', width=200)
		print("RTE table:")
		top_id = tree.insert('', 'end', 'RTE Table', text='RTE Table')
		c.execute("select * from gpkgext_relations")
		i = 0
		for row in c.fetchall():
			if (i == 0):
				print(row.keys())
				tree.insert(top_id, 'end', 'rte-keys', text=row.keys())
			label = ''
			for k in row.keys():
				label += row[k] + ", "
			print(i, ": ", label)
			i = i + 1;
			tree.insert(top_id, 'end', i, text=label)
		print()


if __name__ == '__main__':
	main()


