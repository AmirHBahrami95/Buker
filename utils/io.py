import json

def fread(path,mode='r'):
	res=''
	try:
		with open(path,mode) as fin:
			res+=fin.readall()
	except E:
		print(E)
		return None
	return res

def fwrite(path,content,mode='w+'):
	try:
		with open(path,mode) as fout:
			fout.write(content)
		return True
	except E:
		print(E)
		return False

def get_settings():
	settings=None
	with open('settings.json','r') as fin:
		settings=json.load(fin)
	return settings
