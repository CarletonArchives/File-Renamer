import sys
import os
from Tkinter import *
from tkFileDialog import *
from operator import itemgetter
import tkFileDialog, Tkinter
import re
import csv

def select_folder(message):
	print message
	root = Tkinter.Tk()
	root.withdraw()
	result = tkFileDialog.askdirectory(parent = root, title = message)
	if not result:
		print '\nError, exiting PDFMerge'
		sys.exit()
	return result

def get_search_replace_inputs(messages):
	root = Tkinter.Tk()
	Boxes=[]
	for message in messages:
		Boxes.append([Tkinter.Label(root,text=message),Tkinter.Entry(root,bd =5)])
	for Box in Boxes:
		Box[0].pack()
		Box[1].pack()
	inputs=[]
	def get_input():
		for Box in Boxes:
			inputs.append(Box[1].get())
	submit = Tkinter.Button(root, text ="Submit", command = get_input)

	submit.pack(side=BOTTOM)
	while(len(inputs)==0):
		try:
			root.update()
		except:
			print "Canceled Operation"
			sys.exit(0)
	return inputs

def get_rename(inFormat,outFormat,name):
	match=inFormat.match(name)
	if(match):
		variables=match.groupdict()
		outFormat=outFormat.split('[')
		for item in outFormat[1:]:
			varName=item[:item.find(']')]
			for variable in variables.keys():
				if(varName.count(variable)*len(variable)==len(varName)):
					while(len(variables[variable])<varName.count(variable)):
						variables[variable]='0'+variables[variable]
					outFormat[outFormat.index(item)]=item.replace(varName+']',variables[variable])
		while(len(outFormat)>1):
			outFormat[0]+=outFormat[1]
			outFormat.pop(1)
		return outFormat[0]
	return ''

def build_search_regex(search):
	searchregex='.*/('
	for char in search:
		if(char=='['):
			searchregex+='(?P<'
		elif(char==']'):
			searchregex+='>[^/]+?)'
		else:
			searchregex+=re.escape(char)
	searchregex+='((\..*$)|$))'
	return re.compile(searchregex)

def load_existing_map():
	output=[]
	if(os.path.isfile("map.csv")):
		fileMap=open("map.csv","r")
		fileMapReader=csv.reader(fileMap)
		for row in fileMapReader:
			output.append(row)
		fileMap.close()
	return output

def get_new_files(fileMap,rootFolder):
	for dirpath,dirname,filename in os.walk(rootFolder):
		for name in filename:
			if(dirpath+'/'+name not in list(map(itemgetter(0),fileMap))):
				fileMap.insert(0,[dirpath+'/'+name,'',-1])
	return fileMap

def do_all_renames(fileMap,search,replace):
	i=0
	while(i<len(fileMap)):
		fileMap[i][2]=int(fileMap[i][2])
		if(fileMap[i][2]>-1):
			break
		if(fileMap[i][2]!=0):
			outName=get_rename(search,replace,fileMap[i][0])
			if(outName!=''):
				fileMap[i][1]=outName
				fileMap[i][2]=0
		i+=1
	return fileMap

def identify_duplicates(fileMap):
	for i in range(0,len(fileMap)):
		if(fileMap[i][2]==0):
			fileMap[i][2]-=list(map(itemgetter(1),fileMap)).count(fileMap[i][1])
			fileMap[i][2]+=1
	return fileMap

try:
	os.chdir(os.path.split(os.getcwd()+"/"+sys.argv[0])[0])
except:
	print "Map not found, exiting"

inputs = get_search_replace_inputs(["Enter format for input","Enter format for output"])
finalsearchregex=build_search_regex(inputs[0])

replace=inputs[1]

rootFolder=select_folder("Choose the folder containing files to rename")
filenames=[]
renames=load_existing_map()

get_new_files(renames,rootFolder)

renames=do_all_renames(renames,finalsearchregex,replace)

renames=identify_duplicates(renames)
renames.sort(key=itemgetter(2))

fullmap=open("map.csv","w")
for rename in renames:
	fullmap.write("\""+rename[0]+"\",\""+rename[1]+"\",\""+str(rename[2])+"\"\n")
fullmap.close()
