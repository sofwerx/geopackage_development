import os
import sqlite3
import string

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import *

win = tk.Tk()
win.title("GeoPackage Info")

tk.Label(win, text='GeoPackage file: ').grid(column=1, row=1)
gpkg_file = filedialog.askopenfilename()
tk.Label(win, text=gpkg_file).grid(column=1, row=2)

#gpkg_file = dialogs.pick_document()
print(gpkg_file)
conn = sqlite3.connect(gpkg_file)
conn.row_factory = sqlite3.Row
c = conn.cursor()

tree = ttk.Treeview(win)
tree.grid(column=1, row=3)

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

tree = ttk.Treeview(win)
tree.grid(column=1, row=4)
#c.execute("select table_name, extension_name from gpkg_extensions order by extension_name asc, table_name asc")
c.execute("select distinct extension_name from gpkg_extensions order by extension_name asc")
print("Extensions:")
top_id = tree.insert('', 'end', 'Extensions', text='Extensions')
for row in c.fetchall():
	print(row[0])
	tree.insert(top_id, 'end', row[0], text=row[0])
print()

tree = ttk.Treeview(win)
tree.grid(column=1, row=5)
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

win.mainloop()

