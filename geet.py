
print('Initiating geet')
import os
from os import listdir,path,walk
from time import ctime 
import json
import shutil

pathJoin=os.path.join

#################################################################
#			USER DEFINED CONSTANTS
#################################################################

database = '/home/stark/Desktop/JSON DATA/Geet_files/'
workingDir = '/home/stark/Desktop/college'
lstrip_path = workingDir.rstrip(os.path.basename(workingDir))

#################################################################


def index(direc_loc,workingDir):
	core_dir = listdir(workingDir)
	for direc in core_dir:
		if os.path.isfile(os.path.abspath(direc)):
			core_dir.remove(direc)
	for i in range(len(core_dir)):
		core_dir[i] = os.path.join(workingDir,core_dir[i])


	for root,dirs,files in os.walk(workingDir):
		if os.path.basename(root).startswith('.'):
			continue
		elif root == workingDir :
			json_data = []
			cwd = os.path.basename(root)


		elif root in core_dir and cwd != os.path.basename(root):
			with open(os.path.join(direc_loc,cwd+'.json'),'w') as outfile:
				json.dump(json_data,outfile,indent=4)
				outfile.close()

			cwd = os.path.basename(root)
			json_data = []
				
		json_data= json_data + jsonify_data(root,dirs,files)




def jsonify_data(root,dirs,files):
	obj = []
	root_strip = root.lstrip(lstrip_path)
	for filename in files :
		meta = {
			"path" : root_strip + '/' + filename,
			"abspath" : pathJoin(root,filename),
			"name" : filename,
			"date" : ctime(path.getmtime(root + '/' + filename)),
			"DIR" : "false"
		}
		obj.append(meta)

	for directories in dirs :
		meta = {
			"path" : pathJoin(root_strip,directories),
			"abspath" : pathJoin(root,directories),
			"name" : directories,
			"date" : ctime(path.getmtime(root + '/' + directories)),
			"DIR" : "true"
		}
		obj.append(meta) 
	return obj

def create_temp_files():
	temp = os.path.join(database,'..','temp')
	try:
		os.mkdir(temp)
		os.chdir(temp)
		temp = os.getcwd()
	except OSError,e:
		print str(e)
	except e: 
		print str(e)
	index(temp,workingDir)

	comparator(temp)

	shutil.rmtree(temp)


def comparator(temp_loc):

	original = listdir(database)
	temp = listdir(temp_loc)

	for filename in temp :
		print '\nReading File : ' + filename
		if filename  in original:

			with open(os.path.join(database,filename),'r') as org_out:
				with open(os.path.join(temp_loc,filename),'r') as temp_out:
					org_data = json.load(org_out)
					temp_data = json.load(temp_out)
					

					diff(org_data,temp_data)
					temp_out.close()
				org_out.close()

def diff(org,temp):
	exceptions = []
	deletions = []
	modification = []
	addition = []
	delet = []
	for i in range(len(temp)) :
		if temp[i] in org :
			continue
		else:
			exceptions.append(temp[i])
	for obj in org :
		if obj in temp:
			continue;
		else:
			deletions.append(obj)
	
	if isnotempty_util(exceptions):
		print "exceptions : "
		print_util(exceptions)
	
	

	for i in range(len(exceptions)) :
		flag = 0 
		for j in range(len(org)):
			if exceptions[i]['path']  == org[j]['path'] :
				modification.append(exceptions[i])
				flag = 1
				try:
					deletions.remove(org[j])
					break
				except:
					break
		if flag != 1:
			addition.append(exceptions[i])
	
	if isnotempty_util(addition):
		print "addition list :"
		print_util(addition)
		record_change(addition,'a')

	if isnotempty_util(modification):
		print "modification : "
		print_util(modification)
		record_change(modification,'m')

	for i in range(len(deletions)):
		flag = 0
		for j in range(len(temp)):
			if deletions[i]['name'] == temp[i]['name']:
				print "\n\n do something \n\n"
				flag = 1
				break
		if flag != 1:
			delet.append(deletions)
	if isnotempty_util(deletions):
		print "   deletions : "
		print_util(delet)
		record_change(delet,'d')



def main():
	try:
	 	with open(os.path.join(database,'css.json'),'r') as outfile:
	 		outfile.close()
	except IOError,e :
		print str(e)
		print 'Running geet.py for fist time'
		index(database,workingDir)


	#deleting temporary files
	#shutil.rmtree(os.path.join(database,'..','temp2'))

def print_util(lol):
	for x in lol:
		print x

def isnotempty_util(list):
	if not list:
		return False
	else: 
		return True

def record_change(List,x):
	temp2 = os.path.join(database,'..','temp2')
	if x == 'm':
		JSON_file = 'modified.json'
	elif x == 'd':
		JSON_file = 'deleted.json'
	else:
		JSON_file = 'added.json'

	try:
		os.chdir(temp2)
	except OSError,e:
		os.mkdir(temp2)
		os.chdir(temp2)
		temp2 = os.getcwd()
	except e:
		print str(e)

	try:
		outfile = open(JSON_file,'r+')
		try:
			filedata = json.load(outfile)
		except ValueError:
			filedata = []
		outfile.close()
	except IOError:
		
		filedata = []
	outfile = open(JSON_file,'w')	
	filedata = filedata + List
	json.dump(filedata,outfile,indent = 4)
	outfile.close()



main()

####################################################
#			HELPER FUNCTIONS
####################################################

def readfile(fileName):
	filename = os.path.join(database,'..','temp2',fileName+'.json')
	try :
		outfile = open(filename,'r')
		return json.load(outfile)
	except IOError,e:
		print "file error"
		print str(e)
		return

def clean_temp2():
	filename = os.path.join(database,'..','temp2')
	try:
		shutil.rmtree(filename)
	except OSError,e:
		print ''
	update
def update():
	index(database,workingDir)