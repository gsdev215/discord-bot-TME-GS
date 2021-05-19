import json
token = ""
default_prefix = "."
devs_id = ""
support_server = ""
cog = ["cogs.leveling"]

def json_open(f:str=None):
	with open(f,"r") as f:
		n = json.load(f)
	return n
	
def json_dump(f:str=None,n:str=None):
	#f = f"{f}"
	#n = f"{d}"
	with open(f,"w") as f:
		json.dump(n,f)
