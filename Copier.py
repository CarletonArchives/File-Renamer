import sys
import os
from Tkinter import *
from tkFileDialog import *
import tkFileDialog, Tkinter
import csv
import shutil



def select_folder(message):
	print message
	root = Tkinter.Tk()
	root.withdraw()
	result = tkFileDialog.askdirectory(parent = root, title = message)
	if not result:
		print '\nError, exiting Copier'
		sys.exit()
	return result

try:
	os.chdir(os.path.split(os.getcwd()+"/"+sys.argv[0])[0])
except:
	print "Map not found, exiting"

here=os.getcwd()
resultFolder=select_folder("Choose where to copy the files to")
print resultFolder
filenames=[]

if(os.path.isfile("map.csv")):
	filemap=open("map.csv","r")
	filemapreader=csv.reader(filemap)
	for row in filemapreader:
		filenames.append(row)
	filemap.close()
else:
	print "No file found."

error=0
os.chdir(resultFolder)
for filename in filenames:
	if(int(filename[2])>-1):
		folder=os.path.split(filename[1])[0]
		if(not os.path.isdir(folder) and folder!=""):
			print folder
			os.makedirs(folder)
		try:
			shutil.copy2(filename[0],filename[1])
		except:
			error+=1

if(error==0):
	os.chdir(here)
	os.remove("map.csv")
